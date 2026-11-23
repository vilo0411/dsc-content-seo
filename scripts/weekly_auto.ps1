# Weekly auto-run for Windows Task Scheduler (Monday morning).
# 1) check Claude login (fail fast)
# 2) refresh the live snapshot + registry (deterministic, no agent)
# 3) headless Claude Code runs the measurement part of /weekly (read-only on articles, writes only the ledger via scripts)
# 4) report -> knowledge/5-analytics/weekly/<date>.md, log -> scratch/weekly-auto/<date>.log, Windows notification
#
# Register once:   powershell -ExecutionPolicy Bypass -File scripts\weekly_auto.ps1 -Register [-At 08:30]
# Run now (test):  powershell -ExecutionPolicy Bypass -File scripts\weekly_auto.ps1
# Remove:          Unregister-ScheduledTask -TaskName "DSC weekly review" -Confirm:$false
#
# Auth: the interactive claude.ai login has a hard end date, so unattended runs use a long-lived token:
#   claude setup-token  -> paste the printed token into .agents/config/claude-token.txt (gitignored).
# Without the file the script falls back to the interactive login and warns when it is about to end.
#
# Failure handling: not logged in -> stop before doing anything; login lost mid-run -> stop; transient errors
# (rate limit, overload, network) -> retry once after 15 min; MCP down -> report still written, flagged on top.
# Every failure: report file starts with "THẤT BẠI" + cause + fix, and a Windows notification pops up.
param([switch]$Register, [string]$At = "07:00")

$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
$TaskName = "DSC weekly review"

if ($Register) {
    $action = New-ScheduledTaskAction -Execute "powershell.exe" `
        -Argument ('-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "' + $PSCommandPath + '"') `
        -WorkingDirectory $Root
    $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At $At
    # StartWhenAvailable: machine off at run time -> run as soon as the user is logged on again
    $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Hours 2)
    $principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited
    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings `
        -Principal $principal -Force | Out-Null
    Write-Output "Registered '$TaskName': Monday $At (runs late if the machine was off)."
    exit 0
}

Set-Location $Root
$env:PYTHONIOENCODING = "utf-8"
$Today = Get-Date -Format "yyyy-MM-dd"
$ReportDir = Join-Path $Root "knowledge\5-analytics\weekly"
$LogDir = Join-Path $Root "scratch\weekly-auto"
New-Item -ItemType Directory -Force $ReportDir, $LogDir | Out-Null
$Report = Join-Path $ReportDir "$Today.md"
$Log = Join-Path $LogDir "$Today.log"

function Write-Log($msg) { Add-Content -Path $Log -Value ("[" + (Get-Date -Format "HH:mm:ss") + "] " + $msg) -Encoding UTF8 }

function Show-Toast($title, $body) {
    try {
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        $xml = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent(
            [Windows.UI.Notifications.ToastTemplateType]::ToastText02)
        $t = $xml.GetElementsByTagName("text")
        $t.Item(0).AppendChild($xml.CreateTextNode($title)) | Out-Null
        $t.Item(1).AppendChild($xml.CreateTextNode($body)) | Out-Null
        $app = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe'
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($app).Show(
            [Windows.UI.Notifications.ToastNotification]::new($xml))
    } catch {
        & msg.exe $env:USERNAME "$title - $body" 2>$null   # fallback popup
    }
}

function Stop-WithError($cause, $fix) {
    $body = @(
        "# ⚠️ Weekly review THẤT BẠI $Today", "",
        "**Nguyên nhân:** $cause", "",
        "**Cách sửa:** $fix", "",
        'Sửa xong chạy lại: `powershell -ExecutionPolicy Bypass -File scripts\weekly_auto.ps1`', "",
        "Log: scratch/weekly-auto/$Today.log"
    )
    $body | Out-File -FilePath $Report -Encoding utf8
    Write-Log "FAILED: $cause"
    Show-Toast "Weekly review THẤT BẠI" $cause
    exit 1
}

Write-Log "start"

# --- 1. Preflight: Claude login. Fail now rather than after a 4-minute sync. ---
$TokenFile = Join-Path $Root ".agents\config\claude-token.txt"
$UsingToken = $false
if (Test-Path $TokenFile) {
    $tok = (Get-Content $TokenFile -Raw -Encoding UTF8).Trim()
    if ($tok) { $env:CLAUDE_CODE_OAUTH_TOKEN = $tok; $UsingToken = $true }   # this process only
}
$auth = $null
try { $auth = (& claude auth status 2>$null | Out-String) | ConvertFrom-Json } catch {}
if (-not $auth) {
    Stop-WithError "Không chạy được lệnh claude (chưa cài, hoặc không có trong PATH khi chạy từ Task Scheduler)." `
        'Mở terminal, gõ `claude --version`. Lỗi thì cài lại Claude Code.'
}
if (-not $auth.loggedIn) {
    Stop-WithError "Claude Code chưa đăng nhập hoặc phiên đăng nhập đã hết hạn." `
        'Mở terminal, chạy `claude setup-token`, dán token vào `.agents/config/claude-token.txt` (hoặc `claude auth login`), rồi chạy lại script.'
}
Write-Log "auth ok ($($auth.authMethod), token file: $UsingToken, expires $($auth.loginExpiresAt))"
if (-not $UsingToken -and $auth.loginExpiresAt) {
    $left = ([datetime]$auth.loginExpiresAt - (Get-Date)).TotalDays
    if ($left -lt 7) {
        Show-Toast "Claude sắp hết hạn đăng nhập" ("Còn {0:N0} ngày. Chạy: claude setup-token, lưu vào .agents\config\claude-token.txt" -f $left)
    }
}

# --- 2. Live snapshot + registry ---
foreach ($cmd in @("scripts/sync_live.py", "scripts/registry.py refresh")) {
    Write-Log "python $cmd"
    $p = Start-Process python -ArgumentList $cmd -NoNewWindow -Wait -PassThru `
        -RedirectStandardOutput "$LogDir\$Today.step.out" -RedirectStandardError "$LogDir\$Today.step.err"
    Get-Content "$LogDir\$Today.step.out", "$LogDir\$Today.step.err" -Encoding UTF8 -ErrorAction SilentlyContinue |
        Select-Object -Last 15 | ForEach-Object { Write-Log "  $_" }
    Write-Log "  exit $($p.ExitCode)"   # non-zero: keep going, the old snapshot is still usable
}

# --- 3. Headless /weekly ---
$Prompt = @'
Chạy /weekly ở CHẾ ĐỘ TỰ ĐỘNG (không có người ngồi trước máy, không hỏi lại).
sync_live và registry refresh đã chạy xong, không chạy lại. Property: sc-domain:dsc.com.vn.
Dùng meta.totals của MCP, không tự cộng dòng. Không lưu cache (dashboard_cache save), không gọi get_cannibalization (quá lớn).

Làm:
1. python scripts/weekly_review.py (đọc kỹ mục 0, 3, 3b, 3c).
2. Bối cảnh site: get_data_freshness; get_overview days 7 compare prev_period; get_google_updates since 45 ngày trước.
3. Review tuần trước: mục 0 của script + `python scripts/revision_log.py brief --since <ngày mục 0>`. Có báo cáo tuần trước (đường dẫn ở mục 0) thì đọc riêng phần "Cần làm tuần này" của nó, đối chiếu với sổ + sync_live để đánh dấu: đã xong / còn tồn / không đo được.
4. Before → After cho bài đến hạn (nhóm 3b): query_search_analytics dimensions ["page"], page_match equals URL bài, 2 lần với start_date/end_date: before = khung script in ra; after = từ ngày script in ra đến latest_data_date, cắt bằng số ngày của before. Thêm 1 lần dimensions ["query"] cho khung after (limit 5) để biết query chính. Bài mới nhóm 3: chỉ khung after (days 14).
   Ghi sổ từng bài: python scripts/weekly_review.py --done gsc <slug> --result "before <clicks/imp/pos> → after <clicks/imp/pos> · <kết luận>".
   Khung before/after trùng Google core update (bước 2) → ghi rõ, không kết luận bài tệ đi chỉ vì số giảm; so thêm với cả site cùng kỳ (get_overview cùng 2 khung).
5. Nội dung đang giảm: get_content_decay days 90 limit 150 → chỉ giữ URL /kien-thuc/ có total_clicks ≥ 150, lấy 10 bài giảm mạnh nhất. Thêm query_search_analytics dimensions ["page"], page_value "/kien-thuc/", days 28, compare_mode prev_period, sort_by click_change, sort_dir asc, limit 10.
   Mỗi bài: python scripts/topic_status.py <slug> (trạng thái) và xem sổ (vừa optimize trong 30 ngày → ghi "đang chờ đo", không đề xuất lại). Đề xuất tối đa 5 bài cho /optimize, kèm lý do (mất vị trí ở query nào / mất CTR / cả site cùng giảm do core update).
5b. Thay đổi trên site (annotations): list_annotations limit 100 → chỉ annotation có date trong 14 ngày qua.
   - Cảnh báo (ưu tiên cao): Title thành tiêu đề chung/chuyên mục (vd "Kiến thức cơ bản và nâng cao…"), 2 URL có Title giống nhau,
     Title nói về mã/chủ đề khác slug (vd slug vre mà Title VIC), cùng 1 URL bị đổi rồi đổi ngược.
   - Annotation có date + window_days ≤ latest_data_date và chưa có trong báo cáo tuần trước → get_annotation_impact → bảng tác động.
   - Thay đổi không có trong sổ (publish-ledger) = có người sửa CMS ngoài quy trình → liệt kê.
   - Bài optimize/publish trong sổ 7 ngày qua mà không có annotation → nhắc user thêm annotation tay trên dashboard (MCP chỉ đọc).
6. AI visibility 1 lần cho cả site (get_ai_visibility, get_ai_traffic) — tóm tắt ≤ 4 dòng.
7. python scripts/fact_consistency.py --due (exit 1 = có fact cần review, không phải lỗi).
8. Đối thủ: python scripts/competitor_watch.py run rồi report.

KHÔNG làm: sửa bài, tạo/sửa link plan, xoá hay chuyển file, rotate log, publish. Nhóm 1 và 2 chỉ liệt kê.

Nếu SEO Dashboard MCP không gọi được (chưa kết nối / hết hạn OAuth / lỗi): dòng ĐẦU TIÊN của output phải là
"LỖI_MCP: <thông báo lỗi>"; vẫn làm các bước không cần MCP rồi in báo cáo như dưới. Không ghi --done gsc cho bài chưa đo được.

Output (chỉ in báo cáo markdown tiếng Việt có dấu, không lời dẫn; mục nào không có gì ghi "không có"):
# Weekly review <ngày> (dữ liệu GSC đến <latest_data_date>)
## Tóm tắt (≤ 3 dòng: site tuần này so tuần trước, Google update đang chạy, điều quan trọng nhất)
## Cần làm tuần này (việc → lệnh/skill cụ thể, ưu tiên cao trước, ≤ 8 mục)
## Tuần trước: đã làm / còn tồn (bảng: việc · trạng thái · ghi chú)
## Before → After (bảng: bài · loại mới/optimize lần N · khung before · khung after · clicks · imp · vị trí · query chính · kết luận · đề xuất: OK / theo dõi / /optimize Title-Meta / /optimize nội dung / kiểm index)
## Sắp đến hạn đo (7 ngày tới, từ mục 3c)
## Thay đổi trên site (annotations): cảnh báo · tác động các thay đổi đã đủ khung đo · sửa ngoài quy trình · annotation cần thêm tay
## Nội dung đang giảm (bảng: bài · clicks 28d so kỳ trước · vị trí · nguyên nhân khả dĩ · trạng thái sổ · đề xuất)
## Chờ publish / backfill link (chỉ danh sách)
## AI visibility
## Brand facts quá hạn
## Đối thủ tuần này (≤ 8 dòng)
## Lỗi khi chạy
'@

$Allowed = @(
    "Bash(python scripts/*)", "Bash(python .agents/skills/*)",
    "PowerShell(python scripts/*)", "PowerShell(python .agents/skills/*)",
    "Read", "Grep", "Glob", "Skill",
    "mcp__plugin_seo-dashboard_gsc-dashboard"
)
$Denied = @("Edit", "Write", "NotebookEdit", "WebSearch", "WebFetch")

# Prompt via a UTF-8 file on stdin, stdout/stderr to separate files: raw bytes, no PS 5.1 encoding or quoting issues,
# and CLI warnings on stderr never end up inside the report.
$PromptFile = "$LogDir\$Today.prompt.txt"; $OutFile = "$LogDir\$Today.out.md"; $ErrFile = "$LogDir\$Today.err.txt"
[IO.File]::WriteAllText($PromptFile, $Prompt, (New-Object System.Text.UTF8Encoding $false))
$cliArgs = (@("-p", "--output-format", "text", "--allowedTools") + $Allowed + @("--disallowedTools") + $Denied |
    ForEach-Object { '"' + $_ + '"' }) -join " "

$AuthPattern = "Invalid API key|Please run /login|authentication_error|OAuth token (has )?(expired|revoked)|not logged in|\b401\b"
$TransientPattern = "rate.?limit|overloaded|\b529\b|usage limit|ECONNRESET|ETIMEDOUT|ENOTFOUND|fetch failed|network"

$out = ""
for ($attempt = 1; $attempt -le 2; $attempt++) {
    Write-Log "claude -p /weekly (attempt $attempt)"
    $p = Start-Process claude -ArgumentList $cliArgs -NoNewWindow -Wait -PassThru `
        -RedirectStandardInput $PromptFile -RedirectStandardOutput $OutFile -RedirectStandardError $ErrFile
    $code = $p.ExitCode
    $out = [IO.File]::ReadAllText($OutFile, [Text.Encoding]::UTF8)
    $err = [IO.File]::ReadAllText($ErrFile, [Text.Encoding]::UTF8)
    Write-Log "  exit $code, $($out.Length) chars"
    if ($err.Trim()) { Add-Content -Path $Log -Value ("  stderr: " + $err.Trim()) -Encoding UTF8 }
    if ($code -eq 0 -and $out.Trim().Length -ge 200) { break }

    Add-Content -Path $Log -Value $out -Encoding UTF8
    $all = $err + "`n" + $out
    $head = if ($all.Length -gt 1500) { $all.Substring(0, 1500) } else { $all }
    if ($head -match $AuthPattern) {
        Stop-WithError "Claude Code mất đăng nhập (token/phiên đã hết hạn)." `
            'Mở terminal, chạy `claude setup-token`, dán token mới vào `.agents/config/claude-token.txt`, rồi chạy lại script.'
    }
    if ($attempt -eq 1 -and $head -match $TransientPattern) {
        Write-Log "  transient error -> retry in 15 min"
        Start-Sleep -Seconds 900
        continue
    }
    $cause = (($head -split "`n" | Where-Object { $_.Trim() } | Select-Object -First 3) -join " / ")
    if (-not $cause) { $cause = "không có output" }
    Stop-WithError "Claude chạy lỗi (exit $code): $cause" `
        "Xem log. Hết quota: chờ reset rồi chạy lại. Lỗi mạng: kiểm tra mạng / VPN / Kaspersky rồi chạy lại."
}

# --- 4. Report + notification ---
$out | Out-File -FilePath $Report -Encoding utf8
$mcp = [regex]::Match($out, '(?m)^\s*LỖI_MCP:\s*(.+)$')
if ($mcp.Success) {
    $mcpErr = $mcp.Groups[1].Value.Trim()
    Write-Log "MCP error: $mcpErr"
    $top = @(
        "> ⚠️ **Thiếu số GSC — SEO Dashboard MCP lỗi:** $mcpErr",
        '> Cách sửa: mở `claude`, gõ `/mcp`, chọn seo-dashboard → Authenticate; xong chạy lại script.', ""
    )
    ($top + (Get-Content $Report -Encoding UTF8)) | Out-File -FilePath $Report -Encoding utf8
    Show-Toast "Weekly review: thiếu số GSC" "SEO Dashboard MCP lỗi. Mở báo cáo để xem cách sửa."
} else {
    Show-Toast "Weekly review đã xong" "knowledge\5-analytics\weekly\$Today.md"
}
Write-Log "done"
