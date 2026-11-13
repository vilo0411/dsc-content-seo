"""Curated anchor keys (reviewed by hand from the GSC draft of 2026-11-10-anchor-keys.gen.py).

Rule (user 2026-11-10): 1 key chính / bài, nhiều key phụ + ngữ nghĩa; ưu tiên key chính, đa dạng key phụ / ngữ nghĩa.
Removed from the draft: typos ("chứng khoáng", "rủi do"), fragments ("phân tích kỹ", "chủ sở"), off-topic queries
(forex/mt4, other tickers), bare tickers / single broad words, queries that only make sense typed in Google.
Run: python <this file>  -> knowledge/3-pipeline/internal-links/anchor-keys.csv
"""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]

K = {
 # ── pillars
 "cach-dau-tu-chung-khoan-cho-nguoi-moi-bat-dau": ("cách chơi chứng khoán cho người mới", ["cách chơi chứng khoán", "chơi chứng khoán như thế nào", "hướng dẫn chơi chứng khoán", "cách đầu tư chứng khoán cho người mới"], ["chơi chứng khoán", "bắt đầu đầu tư chứng khoán"]),
 "cach-mo-tai-khoan-chung-khoan": ("cách mở tài khoản chứng khoán", ["mở tài khoản chứng khoán online", "đăng ký tài khoản chứng khoán", "hướng dẫn mở tài khoản chứng khoán"], ["mở tài khoản chứng khoán", "tạo tài khoản chứng khoán"]),
 "phan-tich-ky-thuat-la-gi": ("phân tích kỹ thuật", ["phân tích kỹ thuật chứng khoán", "phân tích kỹ thuật là gì", "phương pháp phân tích kỹ thuật"], ["PTKT", "đọc biểu đồ kỹ thuật"]),
 "phan-tich-co-ban-la-gi": ("phân tích cơ bản", ["phân tích cơ bản chứng khoán", "phân tích cơ bản là gì", "phương pháp phân tích cơ bản"], ["phân tích cơ bản doanh nghiệp", "phân tích nền tảng doanh nghiệp"]),
 "cac-chien-luoc-dau-tu-chung-khoan-pho-bien-tren-thi-truong": ("chiến lược đầu tư chứng khoán", ["các chiến lược đầu tư chứng khoán", "phương pháp đầu tư chứng khoán", "chiến lược đầu tư dài hạn"], ["chiến lược đầu tư", "phong cách đầu tư"]),
 "chung-chi-quy-la-gi": ("chứng chỉ quỹ", ["chứng chỉ quỹ là gì", "đầu tư chứng chỉ quỹ", "giao dịch chứng chỉ quỹ"], ["đầu tư qua quỹ", "quỹ đầu tư chứng khoán"]),
 "chung-khoan-phai-sinh-la-gi-huong-dan-dau-tu-cho-nguoi-moi-bat-dau": ("chứng khoán phái sinh", ["chứng khoán phái sinh là gì", "giao dịch phái sinh", "đầu tư chứng khoán phái sinh"], ["thị trường phái sinh", "phái sinh"]),
 "phan-tich-vi-mo-trong-dau-tu-chung-khoan-la-gi": ("phân tích vĩ mô", ["phân tích kinh tế vĩ mô", "phân tích vĩ mô trong đầu tư chứng khoán"], ["yếu tố vĩ mô", "bối cảnh vĩ mô"]),
 "co-tien-nen-dau-tu-gi-luc-nay": ("có tiền nên đầu tư gì", ["nên đầu tư gì thời điểm này", "có tiền nên đầu tư vào đâu", "tiền nhàn rỗi nên đầu tư vào đâu"], ["đầu tư gì lúc này", "phân bổ tiền nhàn rỗi"]),
 "cach-dau-tu-vang": ("cách đầu tư vàng", ["cách đầu tư vàng sinh lời", "đầu tư vàng như thế nào", "cách đầu tư vàng cho người mới"], ["đầu tư vàng", "kênh đầu tư vàng"]),
 "trai-phieu-la-gi": ("trái phiếu là gì", ["đầu tư trái phiếu", "cách đầu tư trái phiếu", "mua trái phiếu"], ["trái phiếu", "kênh trái phiếu"]),
 "dau-tu-bac-co-nen-khong": ("đầu tư bạc", ["có nên đầu tư bạc", "đầu tư bạc ở Việt Nam"], ["kênh đầu tư bạc", "mua bạc tích trữ"]),
 # ── hubs
 "nen-mo-tai-khoan-chung-khoan-o-dau": ("nên mở tài khoản chứng khoán ở đâu", ["mở tài khoản chứng khoán ở đâu tốt nhất", "công ty chứng khoán uy tín"], ["chọn công ty chứng khoán", "chọn nơi mở tài khoản"]),
 "cac-quy-dinh-giao-dich-chung-khoan-quan-trong-ma-nguoi-moi-can-biet": ("quy định giao dịch chứng khoán", ["các quy định giao dịch chứng khoán", "quy định thời gian giao dịch chứng khoán"], ["quy định giao dịch", "luật giao dịch chứng khoán"]),
 "cach-mua-co-phieu-online-cho-nguoi-moi-bat-dau": ("cách mua cổ phiếu online", ["cách mua cổ phiếu", "hướng dẫn mua cổ phiếu", "mua cổ phiếu như thế nào"], ["mua cổ phiếu online", "đặt lệnh mua cổ phiếu"]),
 "cac-kinh-nghiem-dau-tu-chung-khoan-cho-nguoi-moi-bat-dau": ("kinh nghiệm đầu tư chứng khoán", ["kinh nghiệm chơi chứng khoán", "kinh nghiệm đầu tư chứng khoán cho người mới", "cách đầu tư chứng khoán hiệu quả"], ["bài học đầu tư", "kinh nghiệm cho nhà đầu tư mới"]),
 "lenh-ato-atc-lo-mp-la-gi": ("lệnh ATO, ATC, LO, MP", ["lệnh ATO", "lệnh ATC", "lệnh LO", "lệnh MP"], ["các loại lệnh", "các lệnh giao dịch"]),
 "chi-so-chung-khoan-la-gi": ("chỉ số chứng khoán", ["chỉ số chứng khoán là gì", "các chỉ số chứng khoán"], ["chỉ số thị trường", "chỉ số giá chứng khoán"]),
 "cac-chi-bao-xac-dinh-xu-huong-dang-tin-cay-trong-phan-tich-ky-thuat": ("chỉ báo xác định xu hướng", ["các chỉ báo xu hướng", "chỉ báo xu hướng", "xác định xu hướng"], ["nhận diện xu hướng", "chỉ báo theo xu hướng"]),
 "phuong-phap-dau-tu-theo-dong-tien-hieu-qua": ("đầu tư theo dòng tiền", ["dòng tiền chứng khoán", "dòng tiền trong chứng khoán", "phương pháp đầu tư theo dòng tiền"], ["dòng tiền thị trường", "theo dõi dòng tiền"]),
 "tu-dien-30-mo-hinh-nen-pho-bien-tren-thi-truong-chung-khoan": ("các mô hình nến", ["mô hình nến", "các mẫu hình nến trong chứng khoán", "các loại nến trong chứng khoán"], ["mẫu hình nến", "nến Nhật"]),
 "cac-mo-hinh-gia-trong-chung-khoan": ("các mô hình giá", ["mô hình giá", "các mô hình giá trong chứng khoán", "mẫu hình giá"], ["mô hình giá cơ bản", "mô hình đảo chiều"]),
 "chi-bao-ky-thuat": ("chỉ báo kỹ thuật", ["các chỉ báo kỹ thuật chứng khoán", "chỉ báo phân tích kỹ thuật"], ["công cụ chỉ báo kỹ thuật", "bộ chỉ báo kỹ thuật"]),
 "cach-phan-tich-bao-cao-tai-chinh": ("cách phân tích báo cáo tài chính", ["phân tích báo cáo tài chính", "phân tích báo cáo tài chính doanh nghiệp"], ["phân tích BCTC", "đọc số liệu báo cáo tài chính"]),
 "cac-chi-so-phan-tich-bao-cao-tai-chinh": ("các chỉ số phân tích báo cáo tài chính", ["chỉ số tài chính doanh nghiệp", "các chỉ số tài chính", "phân tích chỉ số tài chính"], ["nhóm chỉ số tài chính", "chỉ số tài chính"]),
 "cach-dinh-gia-co-phieu-cho-nguoi-moi-bat-dau": ("cách định giá cổ phiếu", ["định giá cổ phiếu", "phương pháp định giá cổ phiếu", "công thức định giá cổ phiếu"], ["giá trị hợp lý của cổ phiếu", "định giá doanh nghiệp"]),
 "co-tuc-la-gi": ("cổ tức là gì", ["chia cổ tức", "cách tính cổ tức", "nhận cổ tức"], ["tiền cổ tức", "cổ tức tiền mặt"]),
 "phan-tich-doanh-nghiep-trong-dau-tu-chung-khoan-la-gi": ("phân tích doanh nghiệp", ["phân tích doanh nghiệp trong đầu tư chứng khoán", "phân tích hoạt động kinh doanh"], ["đánh giá doanh nghiệp", "phân tích định tính"]),
 "top-5-co-phieu-ngan-hang-dinh-gia-hop-ly-tiem-nang-but-pha-manh": ("cổ phiếu ngân hàng", ["cổ phiếu ngành ngân hàng", "các mã cổ phiếu ngân hàng", "cổ phiếu ngân hàng tiềm năng"], ["nhóm ngân hàng", "ngành ngân hàng"]),
 "top-5-co-phieu-bat-dong-san-co-the-buoc-vao-song-tang-giai-doan-cuoi-nam": ("cổ phiếu bất động sản", ["mã cổ phiếu bất động sản", "cổ phiếu ngành bất động sản", "cổ phiếu BĐS"], ["nhóm bất động sản", "ngành bất động sản"]),
 "top-5-co-phieu-nganh-thep-co-co-ban-tot-sap-buoc-vao-chu-ky-tang-truong-moi": ("cổ phiếu ngành thép", ["cổ phiếu thép", "mã cổ phiếu ngành thép"], ["ngành thép", "nhóm thép"]),
 "co-phieu-nganh-nang-luong": ("cổ phiếu ngành năng lượng", ["cổ phiếu năng lượng", "cổ phiếu dầu khí", "cổ phiếu ngành điện"], ["ngành năng lượng", "ngành dầu khí"]),
 "co-phieu-nganh-ban-le": ("cổ phiếu ngành bán lẻ", ["cổ phiếu bán lẻ", "mã cổ phiếu ngành bán lẻ"], ["ngành bán lẻ", "nhóm bán lẻ"]),
 "top-5-co-phieu-nganh-chung-khoan-dang-dau-tu-nhat": ("cổ phiếu ngành chứng khoán", ["cổ phiếu chứng khoán", "cổ phiếu công ty chứng khoán"], ["nhóm chứng khoán", "ngành chứng khoán"]),
 "top-co-phieu-cang-bien-nen-dau-tu": ("cổ phiếu cảng biển", ["cổ phiếu ngành cảng biển", "cổ phiếu cảng", "cổ phiếu vận tải biển"], ["ngành cảng biển", "nhóm cảng biển"]),
 "co-phieu-nganh-nong-nghiep": ("cổ phiếu ngành nông nghiệp", ["cổ phiếu nông nghiệp"], ["ngành nông nghiệp", "nhóm nông nghiệp"]),
 "co-phieu-nganh-cong-nghe": ("cổ phiếu ngành công nghệ", ["cổ phiếu công nghệ", "các cổ phiếu công nghệ"], ["ngành công nghệ", "nhóm công nghệ"]),
 "huong-dan-phan-tich-nganh-trong-dau-tu-chung-khoan": ("phân tích ngành", ["phân tích ngành chứng khoán", "phân tích ngành là gì", "cách phân tích ngành"], ["triển vọng ngành", "chu kỳ ngành"]),
 "co-phieu-la-gi-cac-loai-co-phieu-tren-thi-truong-chung-khoan-viet-nam": ("cổ phiếu là gì", ["các loại cổ phiếu", "đầu tư cổ phiếu"], ["phân loại cổ phiếu", "loại cổ phiếu"]),
 "top-co-phieu-hang-khong-nen-dau-tu": ("cổ phiếu hàng không", ["cổ phiếu ngành hàng không", "cổ phiếu hàng không Việt Nam"], ["ngành hàng không", "nhóm hàng không"]),
 "co-phieu-nganh-hoa-chat": ("cổ phiếu ngành hóa chất", ["cổ phiếu hóa chất", "cổ phiếu phân bón"], ["ngành hóa chất", "ngành phân bón"]),
 "co-phieu-nganh-det-may": ("cổ phiếu ngành dệt may", ["cổ phiếu dệt may", "cổ phiếu may mặc"], ["ngành dệt may", "nhóm dệt may"]),
 "top-5-co-phieu-dang-dau-tu": ("cổ phiếu đáng đầu tư", ["nên mua cổ phiếu nào", "nên đầu tư cổ phiếu nào", "cổ phiếu tiềm năng"], ["cổ phiếu tốt", "danh sách cổ phiếu"]),
 "quan-tri-rui-ro-la-gi-2": ("quản trị rủi ro", ["quản lý rủi ro", "quản trị rủi ro là gì", "quản trị rủi ro trong đầu tư"], ["kiểm soát rủi ro", "phòng ngừa rủi ro"]),
 "thien-kien-nhan-thuc-la-gi": ("thiên kiến nhận thức", ["thiên kiến nhận thức là gì", "các loại thiên kiến"], ["thiên kiến", "bẫy tâm lý"]),
 "so-sanh-chinh-sach-tai-khoa-va-chinh-sach-tien-te": ("chính sách tài khóa và chính sách tiền tệ", ["chính sách tài khóa và tiền tệ", "so sánh chính sách tài khóa và chính sách tiền tệ"], ["chính sách kinh tế vĩ mô", "chính sách vĩ mô"]),
 "can-can-thanh-toan-bop-la-gi": ("cán cân thanh toán", ["cán cân thanh toán quốc tế", "cán cân thanh toán là gì"], ["BOP", "dòng tiền quốc tế"]),
 "kinh-te-hoc-vi-mo-la-gi-y-nghia-trong-dau-tu-chung-khoan": ("kinh tế học vi mô", ["kinh tế vi mô", "kinh tế vi mô là gì"], ["hành vi doanh nghiệp và người tiêu dùng", "cung cầu"]),
 "khung-hoang-tai-chinh-la-gi-cac-giai-doan-cua-khung-hoang-tai-chinh": ("khủng hoảng tài chính", ["khủng hoảng tài chính là gì", "khủng hoảng kinh tế"], ["cuộc khủng hoảng", "suy sụp tài chính"]),
 "lai-suat-gui-tiet-kiem-ngan-hang-nao-cao-nhat": ("lãi suất gửi tiết kiệm ngân hàng nào cao nhất", ["gửi tiết kiệm ngân hàng nào cao nhất", "ngân hàng nào có lãi suất tiết kiệm cao nhất", "so sánh lãi suất tiết kiệm"], ["lãi suất tiết kiệm các ngân hàng", "lãi suất tiết kiệm"]),
 "trai-phieu-la-gi#hub": None,
 # ── sub-hubs (topic)
 "app-dau-tu-chung-khoan": ("app đầu tư chứng khoán", ["ứng dụng chứng khoán", "app chứng khoán", "ứng dụng giao dịch chứng khoán"], ["app giao dịch", "ứng dụng đầu tư"]),
 "phi-giao-dich-chung-khoan": ("phí giao dịch chứng khoán", ["các loại phí giao dịch chứng khoán", "chi phí giao dịch chứng khoán"], ["phí giao dịch", "biểu phí giao dịch"]),
 "margin-la-gi": ("margin", ["margin là gì", "giao dịch ký quỹ", "vay margin"], ["ký quỹ", "đòn bẩy margin"]),
 "cac-chi-so-chung-khoan-viet-nam-hieu-ro-ve-vn-index-vn-30-hnx-index-va-nhieu-chi-so-khac": ("các chỉ số chứng khoán Việt Nam", ["chỉ số chứng khoán Việt Nam", "các chỉ số thị trường chứng khoán"], ["VN-Index, VN30, HNX-Index", "chỉ số trong nước"]),
 "cac-chi-so-chung-khoan-chau-a-noi-bat": ("chỉ số chứng khoán châu Á", ["chứng khoán châu Á", "các chỉ số chứng khoán châu Á"], ["thị trường châu Á", "chỉ số khu vực"]),
 "thi-truong-tai-chinh-la-gi": ("thị trường tài chính", ["thị trường tài chính là gì", "cấu trúc thị trường tài chính", "vai trò của thị trường tài chính"], ["hệ thống tài chính", "thị trường vốn và tiền tệ"]),
 "cac-thuat-ngu-trong-chung-khoan": ("thuật ngữ chứng khoán", ["các thuật ngữ trong chứng khoán", "thuật ngữ trong chứng khoán"], ["thuật ngữ đầu tư", "từ ngữ chuyên ngành"]),
 "macd-la-gi": ("MACD", ["MACD là gì", "chỉ báo MACD", "đường MACD"], ["MACD histogram", "chỉ số MACD"]),
 "duong-ma-la-gi": ("đường MA", ["đường MA là gì", "đường trung bình động", "đường MA trong chứng khoán"], ["trung bình động", "chỉ báo MA"]),
 "chi-so-rsi-la-gi": ("chỉ số RSI", ["chỉ báo RSI", "RSI là gì", "cách tính chỉ số RSI"], ["RSI", "sức mạnh tương đối"]),
 "duong-ho-tro-va-khang-cu-la-gi": ("hỗ trợ và kháng cự", ["đường hỗ trợ và kháng cự", "vùng hỗ trợ và kháng cự", "cách xác định hỗ trợ và kháng cự"], ["ngưỡng kháng cự", "vùng hỗ trợ"]),
 "giao-dich-theo-xu-huong-trend-following-la-gi": ("giao dịch theo xu hướng", ["trend following", "chiến lược theo xu hướng"], ["đi theo xu hướng", "thuận xu hướng"]),
 "bieu-do-chung-khoan-la-gi-cach-xem-bieu-do-chung-khoan": ("biểu đồ chứng khoán", ["cách xem biểu đồ chứng khoán", "đồ thị chứng khoán", "biểu đồ cổ phiếu"], ["đọc biểu đồ", "biểu đồ giá"]),
 "chi-tieu-loi-nhuan-cua-doanh-nghiep": ("chỉ tiêu lợi nhuận", ["chỉ tiêu lợi nhuận của doanh nghiệp", "các chỉ tiêu lợi nhuận"], ["lợi nhuận doanh nghiệp", "các loại lợi nhuận"]),
 "huong-dan-cach-doc-bao-cao-tai-chinh-nhung-thong-tin-quan-trong": ("cách đọc báo cáo tài chính", ["hướng dẫn đọc báo cáo tài chính", "đọc hiểu báo cáo tài chính"], ["đọc BCTC", "đọc báo cáo tài chính"]),
 "dcf-la-gi": ("DCF", ["DCF là gì", "phương pháp DCF", "chiết khấu dòng tiền"], ["định giá chiết khấu dòng tiền", "mô hình DCF"]),
 "don-bay-tai-chinh-la-gi-uu-va-nhuoc-diem-cach-su-dung": ("đòn bẩy tài chính", ["đòn bẩy tài chính là gì", "hệ số đòn bẩy tài chính"], ["sử dụng nợ vay", "đòn bẩy"]),
 "he-so-thanh-toan-la-gi": ("hệ số thanh toán", ["hệ số thanh toán hiện hành", "hệ số thanh toán nhanh", "hệ số khả năng thanh toán"], ["khả năng thanh toán", "khả năng trả nợ ngắn hạn"]),
 "niem-yet-chung-khoan-ipo-la-gi-nhung-dieu-can-biet": ("niêm yết chứng khoán", ["IPO chứng khoán", "niêm yết là gì", "điều kiện niêm yết chứng khoán"], ["lên sàn", "IPO"]),
 "so-sanh-co-phieu-thuong-va-co-phieu-uu-dai": ("cổ phiếu thường và cổ phiếu ưu đãi", ["cổ phiếu phổ thông và cổ phiếu ưu đãi", "cổ phiếu ưu đãi"], ["loại cổ phần", "cổ phần ưu đãi"]),
 "von-chu-so-huu-la-gi": ("vốn chủ sở hữu", ["vốn chủ sở hữu là gì", "vốn điều lệ và vốn chủ sở hữu"], ["vốn của cổ đông", "nguồn vốn chủ"]),
 "trading-trong-chung-khoan-la-gi": ("trading chứng khoán", ["trading là gì", "trading trong đầu tư chứng khoán"], ["giao dịch ngắn hạn", "lướt sóng"]),
 "ty-le-risk-reward-la-gi": ("tỷ lệ risk/reward", ["tỷ lệ R:R", "tỷ lệ rủi ro trên lợi nhuận", "risk reward"], ["tỷ lệ lời lỗ", "R:R"]),
 "danh-muc-dau-tu-hieu-qua-la-gi": ("danh mục đầu tư hiệu quả", ["danh mục đầu tư tối ưu", "đa dạng hóa danh mục đầu tư"], ["danh mục đầu tư", "phân bổ danh mục"]),
 "rui-ro-la-gi": ("rủi ro là gì", ["các loại rủi ro", "rủi ro đầu tư", "phân loại rủi ro"], ["rủi ro trong đầu tư", "mức độ rủi ro"]),
 "etf-la-gi": ("ETF là gì", ["quỹ ETF", "đầu tư ETF", "quỹ ETF là gì"], ["chứng chỉ quỹ ETF", "quỹ hoán đổi danh mục"]),
 "quy-mo-la-gi-tong-quan-ve-quy-mo-tren-thi-truong-chung-khoan-viet-nam": ("quỹ mở", ["quỹ mở là gì", "đầu tư quỹ mở", "chứng chỉ quỹ mở"], ["quỹ mở tại Việt Nam", "đầu tư qua quỹ mở"]),
 "lam-phat-la-gi": ("lạm phát", ["lạm phát là gì", "nguyên nhân lạm phát", "hậu quả của lạm phát"], ["mức lạm phát", "trượt giá"]),
 "chu-ky-kinh-te-la-gi-cach-van-dung-chu-ky-kinh-te-de-dau-tu-co-phieu-hieu-qua": ("chu kỳ kinh tế", ["chu kỳ kinh tế là gì", "chu kỳ kinh tế và chứng khoán"], ["giai đoạn của nền kinh tế", "chu kỳ tăng trưởng và suy thoái"]),
 "gdp-la-gi": ("GDP", ["GDP là gì", "cách tính GDP", "tổng sản phẩm quốc nội"], ["tăng trưởng GDP", "quy mô nền kinh tế"]),
 "lai-suat-la-gi": ("lãi suất", ["lãi suất là gì", "các loại lãi suất"], ["mặt bằng lãi suất", "chi phí vốn"]),
 "chinh-sach-tai-khoa-la-gi": ("chính sách tài khóa", ["chính sách tài khóa là gì", "chính sách tài khóa mở rộng"], ["chi tiêu công", "thuế và chi tiêu chính phủ"]),
 "chinh-sach-tien-te-la-gi": ("chính sách tiền tệ", ["chính sách tiền tệ là gì", "chính sách tiền tệ mở rộng", "mục tiêu của chính sách tiền tệ"], ["điều hành tiền tệ", "nới lỏng tiền tệ"]),
 "canh-tranh-la-gi": ("cạnh tranh", ["cạnh tranh là gì", "khái niệm cạnh tranh"], ["tính cạnh tranh", "mức độ cạnh tranh"]),
 "khoa-hoc-chung-khoan": ("khóa học chứng khoán", ["khóa học đầu tư chứng khoán", "học đầu tư chứng khoán", "lớp học chứng khoán"], ["học chứng khoán", "học đầu tư"]),
 "nhung-cuon-sach-hay-ve-dau-tu-chung-khoan": ("sách đầu tư chứng khoán", ["sách hay về đầu tư chứng khoán", "sách chứng khoán"], ["sách đầu tư", "đầu sách"]),
 "chung-chi-tai-chinh": ("chứng chỉ tài chính", ["các chứng chỉ tài chính", "chứng chỉ tài chính quốc tế"], ["bằng cấp tài chính", "chứng chỉ nghề"]),
 "co-nen-dau-tu-vang-thoi-diem-nay": ("có nên đầu tư vàng thời điểm này", ["có nên đầu tư vàng", "có nên đầu tư vàng lúc này", "có nên mua vàng"], ["thời điểm mua vàng", "mua vàng lúc này"]),
 "dau-tu-vang-nen-mua-loai-nao": ("đầu tư vàng nên mua loại nào", ["nên mua vàng loại nào để tích trữ", "nên mua vàng gì để tích trữ"], ["các loại vàng", "chọn loại vàng"]),
 "chung-quyen-la-gi-chung-quyen-co-bao-dam-la-gi-tim-hieu-chung-quyen-tai-viet-nam": ("chứng quyền", ["chứng quyền là gì", "chứng quyền có bảo đảm", "giao dịch chứng quyền"], ["CW", "chứng quyền có đảm bảo"]),
}

# ticker overview pages: cổ phiếu XXX (+ tên DN)  |  mã cổ phiếu XXX  |  ngữ nghĩa: phân tích / đánh giá cổ phiếu XXX
NAMES = {"ACB": "ACB", "BID": "BIDV", "BVH": "Bảo Việt", "CTG": "VietinBank", "DIG": "DIC Corp", "FPT": "FPT", "FRT": "FPT Retail",
         "GAS": "PV Gas", "GVR": "Tập đoàn Cao su", "HDB": "HDBank", "HPG": "Hòa Phát", "HVN": "Vietnam Airlines", "LPB": "LPBank",
         "LTG": "Lộc Trời", "MBB": "MB", "MWG": "Thế Giới Di Động", "NTP": "Nhựa Tiền Phong", "PC1": "PC1", "PLX": "Petrolimex",
         "PNJ": "PNJ", "PVD": "PV Drilling", "REE": "REE", "SAB": "Sabeco", "SHB": "SHB", "SSI": "SSI", "STB": "Sacombank",
         "TCB": "Techcombank", "TPB": "TPBank", "VCB": "Vietcombank", "VHM": "Vinhomes", "VIB": "VIB", "VIC": "Vingroup",
         "VJC": "Vietjet", "VNM": "Vinamilk", "VPB": "VPBank", "VRE": "Vincom Retail"}

reg = json.loads((ROOT / "knowledge/3-pipeline/internal-links/link-clusters.json").read_text(encoding="utf-8"))
role = {}
for c in reg["clusters"]:
    for g in c["groups"]:
        for b in g.get("branches", []):
            if b.get("subhub"):
                role.setdefault(b["subhub"], "sub-hub")
    for g in c["groups"]:
        if g.get("hub"):
            role[g["hub"]] = "hub"
    if c.get("pillar"):
        role[c["pillar"]] = "pillar"
title = {r["slug"]: r["title"] for r in csv.DictReader(open(ROOT / "knowledge/3-pipeline/page-groups.csv", encoding="utf-8-sig"))}

rows, todo = [], []
for t in sorted(role, key=lambda x: (["pillar", "hub", "sub-hub"].index(role[x]), x)):
    if t in K and K[t]:
        main, sub, sem = K[t]
        src = "gsc+review"
    elif t.startswith("co-phieu-"):
        tk = t.split("-")[2].replace("npt", "ntp").upper() if t.split("-")[2] != "pc" else "PC1"
        n = NAMES.get(tk, tk)
        main = f"cổ phiếu {tk}"
        sub = [f"mã cổ phiếu {tk}", f"cổ phiếu {n}" if n != tk else f"cổ phiếu {tk} là gì"]
        sem = [f"phân tích cổ phiếu {tk}", f"đánh giá cổ phiếu {tk}"]
        src = "ticker"
    else:
        todo.append(t)
        continue
    rows.append({"target": t, "role": role[t], "title": title.get(t, ""), "source": src,
                 "key_chinh": main, "key_phu": " | ".join(sub), "ngu_nghia": " | ".join(sem)})

out = ROOT / "knowledge/3-pipeline/internal-links/anchor-keys.csv"
with open(out, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(out.name, len(rows), "missing:", todo)
