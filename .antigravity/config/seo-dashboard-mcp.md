# Kết nối SEO Dashboard MCP

Playbook dùng tool trong pipeline: `.antigravity/skills/seo-dashboard/SKILL.md`.

## Claude Code / claude.ai

Đã có sẵn qua connector claude.ai (tool `mcp__claude_ai_SEO_Dashboard__*`). Không cần cấu hình trong repo.
Kiểm tra: trong session, gọi `list_properties` phải thấy `sc-domain:dsc.com.vn`.

## Google Antigravity

MCP của Antigravity cấu hình **theo máy** (không theo repo) tại:

```
%USERPROFILE%\.gemini\config\mcp_config.json        <- bản mới (agy.exe) — file đang dùng
%USERPROFILE%\.gemini\antigravity\mcp_config.json   <- bản cũ
```

Trang **Settings → MCP Tools** (Allow + ô nhập tên tool) chỉ là danh sách phân quyền, không phải nơi thêm server.

Hoặc mở trong IDE: panel Agent → `...` → **MCP Servers** → **Manage MCP Servers** → **View raw config**.

Server: `https://tool.nguyenvietloc.com/api/mcp` — OAuth 2.1 chuẩn MCP (401 + `resource_metadata`, đăng ký client tự động tại `/api/register`, PKCE S256, scope `read`). Không cần token tĩnh, không cần Node.

```json
{
  "mcpServers": {
    "seo-dashboard": {
      "serverUrl": "https://tool.nguyenvietloc.com/api/mcp"
    }
  }
}
```

Lần đầu agent gọi tool, Antigravity mở trình duyệt để đăng nhập + cấp quyền `read`.

**Nếu Antigravity báo 401 mà không mở trang đăng nhập** (bản cũ chưa hỗ trợ OAuth cho server remote): cập nhật Antigravity, hoặc dùng cầu nối `mcp-remote` (cần cài Node.js LTS — máy công ty có Kaspersky, cân nhắc trước):

```json
{
  "mcpServers": {
    "seo-dashboard": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://tool.nguyenvietloc.com/api/mcp"]
    }
  }
}
```

Sau khi lưu file: reload MCP trong Antigravity. Kiểm tra bằng prompt: *"gọi list_properties của seo-dashboard"*.

> Token OAuth do Antigravity tự lưu trên máy — không bao giờ chép token vào repo.

## Agent không có MCP

Không cần cấu hình. Đọc cache do agent khác lưu:

```bash
python scripts/dashboard_cache.py status
python scripts/dashboard_cache.py report <slug>
```
