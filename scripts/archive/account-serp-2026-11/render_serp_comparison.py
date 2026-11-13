import json,html
from pathlib import Path
e=html.escape
data=[json.loads((Path("knowledge/raw/serp")/(n+".json")).read_text(encoding="utf-8")) for n in ["mo-tai-khoan-chung-khoan","nen-mo-tai-khoan-chung-khoan-o-dau"]]
body="""<h1>DSC vs VFS: DataForSEO SERP</h1><p>Ngày phân tích: 04/11/2026 · Tổng phí hai API call: $0.004.</p>
<section><h2>Phạm vi và giới hạn</h2><p>Google Việt Nam (2704), tiếng Việt, desktop, depth=10. Script lọc Google, mạng xã hội và video; mỗi truy vấn còn 4 organic URL. Dùng rank_group gốc, không đánh số lại. Cache không giữ toàn bộ phản hồi gốc nên không biết đầy đủ những kết quả đã bị lọc.</p><p>Không thấy VFS/DSC trong tập organic giữ lại. Không suy ra mất hạng hoặc phủ nhận kết quả người dùng thấy. Chưa có dữ liệu mobile và lịch sử SERP để kiểm chứng biến động.</p><p>GSC DSC 05/10–01/11/2026: từ khóa chính, bài Nên mở ở đâu có 161 impressions, vị trí 17,06; bài Cách mở có 97 impressions, vị trí 41,55. GSC đi trước snapshot nội dung 03/11, chưa đánh giá được tác động sửa mới.</p></section>"""
for d in data:
 body+="<section><h2>"+e(d["keyword"])+"</h2><p>Thời điểm script ghi: "+e(d["fetched_at"])+"</p><table><tr><th>Rank gốc</th><th>URL / tiêu đề</th></tr>"
 for r in d["organic"]: body+="<tr><td>"+str(r["rank"])+"</td><td><a href='"+e(r["url"],quote=True)+"'>"+e(r["title"])+"</a><br><small>"+e(r["url"])+"</small></td></tr>"
 body+="</table><p>Không có PAA / featured snippet trong phản hồi đã lưu.</p></section>"
body+="""<section><h2>Competitor Gap Synthesis</h2><h3>Đối chiếu từng đối thủ</h3><ul>
<li>Vietcombank: trang dịch vụ kết nối hướng dẫn và hành động. DSC cần lối đi rõ từ bài đọc sang đăng ký.</li>
<li>SSI: bài hành trình đầu tư có bước mở tài khoản. DSC giữ phần sau đăng ký ngắn và dẫn bài chuyên sâu.</li>
<li>TCBS: landing page có quyền lợi, thao tác và FAQ. DSC cần chứng minh lợi ích và hướng dẫn thực tế; không sao chép ưu đãi.</li>
<li>Chungkhoanonline: bài hỏi về số lượng tài khoản xuất hiện trong tập giữ lại. DSC đã có bài tương ứng; chưa cần tạo bản trùng.</li>
<li>VCBS: trình bày chọn kênh, mở tài khoản, đặt lệnh. DSC có thể làm rõ bước tiếp theo sau đăng ký.</li>
<li>VPBankS: bài chọn app dùng tiêu chí phí, bảo mật, công nghệ. DSC có tiêu chí tương ứng; cần tăng nguồn kiểm chứng và khả năng so sánh.</li>
<li>Smarttrader: đáp ứng nhu cầu chọn công ty. DSC nên có bảng so sánh và ngày kiểm tra thông tin.</li></ul>
<h3>Khoảng trống và góc khác biệt</h3><p>Chưa đủ bằng chứng nói tất cả/hầu hết đối thủ thiếu một nội dung. Extraction giới hạn khoảng 2.000 từ và có thể chọn sai container. Không dùng độ dài/heading làm mục tiêu SEO.</p><p>Góc đề xuất cho DSC: ảnh thao tác trên giao diện hiện hành, đầu vào/kết quả từng bước, lỗi thực tế và kênh hỗ trợ. Đây là đề xuất, không phải nguyên nhân ranking đã chứng minh.</p>
<h3>Format, Featured Snippet và PAA</h3><p>Bài chọn công ty: bảng so sánh có nguồn. Bài hướng dẫn: danh sách bước và ảnh thật. Chưa quan sát thấy PAA/featured snippet nên chưa có block cụ thể để nhắm chiếm. FAQ lấy từ GSC và hỗ trợ thực, không gắn nhãn PAA khi chưa có dữ liệu.</p>
<h3>Related searches</h3><p>App/online hỗ trợ bài hướng dẫn; phí dẫn bài chi phí hiện có. Nhóm thương hiệu ngân hàng là intent riêng, không nhồi vào bài DSC hoặc tự động tạo bài mới.</p></section>
<section><h2>Quyết định triển khai</h2><ol>
<li>Bảo vệ bài Nên mở ở đâu; cải thiện bảng tiêu chí, nguồn và liên kết sang bài hướng dẫn.</li>
<li>Kiểm tra index/canonical và render của bài Cách mở, rồi tối ưu câu trả lời sớm và thao tác thực tế.</li>
<li>Phân vai anchor theo nhu cầu. Không tăng link hàng loạt hoặc gộp/redirect/canonical chéo chỉ vì hai URL có cùng query.</li>
<li>Ghi ngày thay đổi. Theo dõi GSC query × URL × thiết bị; đánh giá sau khi Google crawl lại, khoảng 4–6 tuần. Không hứa thời hạn lên top.</li></ol></section>"""
doc="<!doctype html><html lang='vi'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>DSC — DataForSEO SERP 04/11/2026</title><style>body{font:15px/1.65 system-ui;background:#f5f7fa;color:#183044;max-width:1200px;margin:auto;padding:25px}section{background:white;border:1px solid #dae2eb;border-radius:12px;padding:22px;margin:18px 0}table{width:100%;border-collapse:collapse}th,td{padding:12px;text-align:left;border-bottom:1px solid #dae2eb}a{color:#155eb4;overflow-wrap:anywhere}small{color:#697888}li{margin:10px 0}</style>"+body+"</html>"
out=Path("knowledge/raw/competitors/vfs/serp-dsc-comparison-2026-11-04.html")
out.write_text(doc,encoding="utf-8")
assert "kiểm chứng" in doc
print("Saved UTF-8 HTML:",out)

