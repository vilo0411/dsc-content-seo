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

## 1-brand/ — nền cho mọi kênh
| File | Dùng để |
|---|---|
| `profile.md`, `icp.md`, `personas.md`, `service-operations.md` | Doanh nghiệp, khách hàng, quy trình nghiệp vụ thật |
| `brand-facts.json` | **Nguồn duy nhất** cho số liệu DSC (phí, margin, eKYC…) — `qa_lint` `CL5-fact` đọc |
| `anti-ai-rules.md` + `anti-ai-rules-blacklist.md`, `glossary.md`, `source-whitelist.md` | Rule văn, cụm cấm, tên chuẩn, nguồn ngoài được link |
| `DESIGN.md` + `brand.json` (nhận diện chuẩn v1.0, ảnh gốc ở `guideline/`), `image-design-system.md`, `visual-brand-guidelines.md`, `assets/`, `writers/`, `archive/` | Nhận diện hình ảnh cho mọi thiết kế, ảnh blog, writer profile, rule cũ |

## 2-market/
| File / thư mục | Nội dung | Sinh bởi |
|---|---|---|
| `market-landscape.md`, `account-opening-comparison.md` | Bức tranh ngành, so sánh sản phẩm | `/market-research` |
| `research/` | Nghiên cứu theo chủ đề (insight có độ tin cậy + nguồn) | `/market-research` |
| `competitors/competitors.json` | Đối thủ đang theo dõi (domain, hub bài) | `competitor_watch.py discover --add` / sửa tay |
| `competitors/watch/<YYYY-Www>.md`, `velocity.csv` | Bài mới tuần này, nhịp đăng 12 tuần, chủ đề DSC chưa có | `competitor_watch.py report` |
| `competitors/profiles/` | Hồ sơ sâu từng đối thủ | `/competitor-profile` |

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
