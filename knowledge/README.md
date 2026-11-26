# knowledge/ — dữ liệu và sản phẩm

Chia theo **một câu hỏi / thư mục**, không chồng nhau:
nền tảng (`1-brand`, `2-market`) → kênh (`3-seo` là kênh lõi, `4-channels` các kênh còn lại) → đo lường (`5-analytics`) · `raw/` = đầu vào thô · `0-dashboard/` = view sinh tự động.
Cột "Ai ghi": **người** = sửa tay · **agent** = skill viết · **script** = sinh tự động, không sửa tay.

| Thư mục | Trả lời câu hỏi | Ai ghi |
|---|---|---|
| `0-dashboard/` | Đang có việc gì, tới bước nào? | script (`python scripts/build_content_index.py`) |
| `1-brand/` | DSC là ai, bán gì, cho ai, **viết thế nào** (mọi kênh) | người + `/setup`, `/learn` |
| `2-market/` | Thị trường và đối thủ ra sao, tuần này đối thủ làm gì? | agent + script (`/market-research`, `/competitor-*`) |
| `3-seo/` | Mọi thứ của kênh SEO: chiến lược, bài viết, link, log | agent + script |
| `4-channels/` | Bản nháp kênh khác: ads, email, landing, social | agent (`/ads-*`, `/email-sequence`, `/copy-landing`, `/syndicate`) |
| `5-analytics/` | Kết quả đa kênh (KPI, báo cáo tháng) | agent (`/analytics-report`) |
| `6-campaigns/` | Job chiến dịch đa kênh `CMP-YYMMDD-slug/` (brief, social, ads, landing, creatives, approved/) | agent (`scripts/campaign.py`, `/campaign-brief`) |
| `raw/` | Dữ liệu thô: snapshot site live, cache SERP, export GSC, snapshot đối thủ | script |

## 1-brand/ — nền cho mọi kênh (Internal Truth & Prescriptive Rules)
| Nhóm MECE | File | Dùng để |
|---|---|---|
| **1. Định vị & Thương hiệu** | `profile.md` | Định vị nội dung (§0), tổng quan & bằng chứng tin cậy (Proof Points), 3 mảng dịch vụ, USP, giọng văn |
| **2. Sản phẩm, Số liệu & Nghiệp vụ** | `brand-facts.json`, `service-operations.md`, `confirm-with-leadership.md` | **`brand-facts.json` = Nguồn duy nhất** cho số liệu DSC (phí, margin, eKYC… — `qa_lint` `CL5-fact` đọc) · `service-operations.md` = quy trình kỹ thuật step-by-step · `confirm-with-leadership.md` = sổ quyết định & mục chờ xác nhận |
| **3. Tập khách hàng mục tiêu** | `icp.md`, `personas.md` | Trọng tâm phân bổ nguồn lực (`icp.md`) và ma trận 4 Persona P1–P4 (`personas.md`, tra qua `python scripts/persona.py`) |
| **4. Hệ thống Ngôn từ & Nguồn** | `anti-ai-rules.md` + `anti-ai-rules-blacklist.md`, `glossary.md`, `source-whitelist.md`, `writers/` | Rule văn, cụm cấm, từ điển thuật ngữ + tiếng lóng (Slang), nguồn ngoài được phép link, writer profile |
| **5. Hệ thống Thị giác** | `DESIGN.md` + `brand.json` (nhận diện chuẩn v1.0, ảnh gốc ở `guideline/`), `image-design-system.md`, `visual-brand-guidelines.md`, `assets/`, `fanpage-refs/`, `archive/` | Nhận diện hình ảnh cho mọi thiết kế (`DESIGN.md` / `brand.json`), component PIL vẽ infographic (`image-design-system.md`), quy tắc ghép logo & khổ ảnh blog (`visual-brand-guidelines.md`) |

## 2-market/ — bức tranh bên ngoài (External Reality & Intelligence)
| Nhóm MECE | File / thư mục | Nội dung | Sinh bởi |
|---|---|---|---|
| **1. Toàn cảnh Ngành & Mùa vụ** | `market-landscape.md` | Quy mô thị trường, bản đồ đối thủ 2 tầng (Thị phần/Ads vs. SEO Content), khoảng trống thị trường, **Lịch mùa vụ chứng khoán 4 quý** | `/market-research` |
| **2. Tình báo Đối thủ** | `account-opening-comparison.md`, `competitors/competitors.json`, `competitors/watch/<YYYY-Www>.md`, `velocity.csv`, `competitors/profiles/` | So sánh mở tài khoản/phí/margin 6 CTCK (`account-opening-comparison.md`) · Danh sách theo dõi (`competitors.json`) · Nhịp đăng tuần (`watch/`) · Hồ sơ sâu (`profiles/`) | `competitor_watch.py`, `/competitor-profile`, `/market-research` |
| **3. Nghiên cứu Khách hàng & VoC** | `research/voc-objections.md`, `research/<chu-de>-YYYY-MM.md` | **Voice of Customer (VoC) & 5 rào cản chuyển đổi (Objections)** trích từ dữ liệu SERP PAA + GSC thật · Báo cáo nghiên cứu theo chủ đề/quý | `/market-research` |

## 3-seo/ — toàn bộ kênh SEO
| Thư mục | Nội dung | Sinh bởi |
|---|---|---|
| `strategy/` | **`pages.csv` = registry**: 1 dòng / URL (cluster, subgroup, role pillar/hub/spoke, trạng thái bài, anchor, key chính/phụ, slug live ↔ slug file) · `taxonomy.json` = kiến trúc link · `gsc-`/`serp-opportunities.md` · `page-groups*.csv`, `page-audit.csv`, `group-performance.md` (nhóm bài + GSC/GA4) · `topical-map.html` · `sprint-backlog.md` | `registry.py`, `page_groups.py`, `process_gsc.py`, `serp_opportunities.py`, `topical_map.py` |
| `content/` | `0-sources/` → `1-outlines/` → `2-drafts/` → `3-finalized/` → `4-cms/` · `archive/<slug>/` · `images/` · `audits/<đợt>/` | `/write`, `/optimize`, `/approve` |
| `links/` | `plans/` (đợt sửa link: `.json` spec + `.html` bản dán CMS) · `dashboard.md` + `link-graph.html` (audit) · `archive/` (đợt đã xong, file legacy) | `link_plan.py`, `link_audit.py` |
| `logs/` | `revision-log.md` (+ quý cũ), `qa-score-log.csv`, `qa-check-log.csv`, `publish-ledger.csv`, `slop-baseline.csv` | `revision_log.py`, `qa_lint --log`, `article_snapshot.py` — **không sửa tay** |

Trạng thái bài và internal link cùng đọc **một** nguồn `strategy/pages.csv` qua `topic_status.py` / `find_links.py` / `registry.py show` (không mở file 400 KB).

## Thuật ngữ chiến lược (1 khái niệm = 1 tên = 1 nơi lưu)
Thuật ngữ Koray / Semantic SEO ↔ tên dùng trong repo. Skill và script chỉ dùng cột "Tên trong repo".

| Khái niệm (Koray) | Tên trong repo | Lưu ở (duy nhất) | Xem nhanh |
|---|---|---|---|
| Source Context | Định vị nội dung | `1-brand/profile.md` §0 | dashboard → Bản đồ chiến lược |
| Central Entity | Thực thể trung tâm | `1-brand/profile.md` §0 | như trên |
| Topical cluster | Cụm (mã `1`–`14`), nhóm con (`1a`…) | `3-seo/strategy/taxonomy.json` → `topics` | `registry.py cluster` |
| Core / Outer section | `section`: `core` / `outer` / `off` (lệch định vị) | `taxonomy.json` → `topics.<mã>.section` | `registry.py suggest-core` |
| Khu vực site (toàn dsc.com.vn) | `site.sections`: `core` / `outer` / `trust` / `off` / `topics` | `taxonomy.json` → `site` | Topical map → Bản đồ site |
| Entity của cụm | `entity` | `taxonomy.json` → `topics.<mã>.entity` | `registry.py cluster <mã>` |
| Contextual bridge | `bridge_to` (bài Core mà bài Outer phải link về) | `taxonomy.json` → `topics.<mã>.bridge_to` | `registry.py cluster <mã>` |
| Attribute (EAV, cấp cụm) | `attributes` (`fact` = id `brand-facts.json` hoặc `market`) | `taxonomy.json` → `topics.<mã>.attributes` | `registry.py cluster <mã>` (gap) |
| EAV (cấp bài) | khối `EAV:` trong outline | YAML đầu file outline | `outline_lint.py` |
| Giá trị (Value) của DSC / thị trường | fact | `1-brand/brand-facts.json` / `market_facts.py` | `fact_consistency.py` |
| Pillar / hub / spoke | cụm link (`clusters`, mỗi cụm có `topic` = mã cụm) | `taxonomy.json` → `clusters` | `topical-map.html` |
| Hành động cho bài cũ | `action`: refresh / bridge / prune? / keep | `page-audit.csv` (script sinh) | dashboard → Queue |
| Chuyển đổi | Lead / micro-conversion, trọng số | `5-analytics/kpi-definitions.md` | — |

Cụm trên SEO Dashboard MCP (vd "Tài khoản & Giao dịch") là cấu hình riêng của tool, không đồng bộ tự động — đổi tên trong tool cho khớp bảng `topics`.

## Quy ước
- File script sinh ra: không sửa tay, chạy lại script.
- Audit mới: `3-seo/content/audits/<ten>-YYYY-MM-DD/`. Đợt sửa link: `3-seo/links/plans/YYYY-MM-DD-<ten>.json` + `.html`; xong thì chuyển vào `links/archive/`.
- Sau `sync_live.py` / `page_groups.py build`: chạy `python scripts/registry.py refresh` (nhận bài mới live, kể cả khi CMS đổi slug).
