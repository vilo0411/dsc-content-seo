# Continuous Learning: Instincts (Bản năng rút gọn)

> **Bắt buộc:** Mọi agent/skill đọc file này trước khi viết. Bản đầy đủ (nguồn, feedback gốc) ở `.antigravity/memory/instincts-archive.md`.
> **Sinh tự động** bởi `scripts/optimize_instincts.py` — không sửa tay. Sau `/learn`, ghi vào archive rồi chạy lại script.

> **Bản năng theo topic:** `instincts-by-scope/vi-mo.md` — chỉ load khi bài thuộc topic đó.

## Văn phong & Ngôn từ (Style & Tone)

### Loại bỏ mốc thời gian máy móc và gượng ép
- Tuyệt đối không chèn máy móc hoặc lặp đi lặp lại cụm từ "Tính đến tháng M/Y," ở đầu câu khi giải thích lý thuyết. Chỉ chèn mốc thời gian (như "năm 2026", "tháng 9/2026") một cách tự nhiên và đúng thời điểm thực tế (hiện tại là tháng 9/2026) khi thực sự dẫn chứng số liệu thống kê biến động thực tế.

### Thỏa mãn Search Intent kỹ thuật trong bài phân tích
- Đối với các bài viết về báo cáo tài chính hoặc công cụ kỹ thuật, ngoài việc phân tích chiến lược cho nhà đầu tư, cần bổ sung các kiến thức nền tảng như 'Phương pháp lập' hoặc 'Cấu tạo chi tiết'. Điều này giúp thỏa mãn các truy vấn tìm kiếm mang tính học thuật mà không làm loãng ảnh hưởng chiến lược của DSC.

### Tuân thủ độ dài đoạn và cấu trúc Heading chuẩn
- Khi chuyển từ Outline sang Draft, luôn sử dụng Markdown Headings tiêu chuẩn (`#`, `##`, `###`) thay vì giữ nguyên các chuỗi định dạng của Outline (`### H2:`). Điều này đảm bảo Script QA hoạt động chính xác khi cắt block nội dung.

### Bắt buộc có Sapo và Link CTA
- Mọi bài viết phải có đoạn Sapo (Mở bài) ngay dưới tiêu đề H1. Trong phần Kết bài (CTA), phải luôn chèn link trực tiếp đến trang mở tài khoản chứng khoán hoặc bài hướng dẫn tương ứng, không được để lời kêu gọi suông.

### Ràng buộc từ khóa Sapo, Bridge hỗ trợ tư vấn và Miễn trừ trách nhiệm
- 1. Luôn bảo đảm đoạn Sapo đầu bài viết chứa từ khóa chính xác dạng truy vấn (như "có nên mua cổ phiếu LAS không") một cách tự nhiên. 2. Phần dẫn dắt dịch vụ DSC (Product Bridge) bắt buộc phải tích hợp rõ ràng thông tin "hỗ trợ tư vấn đầu tư" từ chuyên gia Môi giới 1:1. Đồng thời, nên gộp thông tin này thành một điểm liệt kê (bullet point) đồng nhất thay vì tách riêng thành hộp Tip để liền mạch với hệ sinh thái. 3. (…xem archive)

### Tối ưu hóa cầu nối sản phẩm chuyển dịch dòng vốn và trực quan hóa các yếu tố vĩ mô
- 1. Khi viết các yếu tố tác động vĩ mô (ví dụ: yếu tố tác động đến giá vàng, giá dầu), luôn trình bày dưới dạng danh sách gạch đầu dòng có in đậm tiêu đề để tăng tính trực quan và dễ skim ý chính cho người đọc. 2. Phần dẫn dắt chuyển dịch dòng tiền (Product Bridge) từ các kênh phòng thủ (như vàng, gửi tiết kiệm) sang kênh cổ phiếu tăng trưởng/chứng chỉ quỹ của DSC phải được lập luận bằng logic tài chính (rủi ro mua đuổi vùng đỉnh, chênh lệch sprea… (xem archive)

### Bảng so sánh định nghĩa & Chi tiết hóa Product Bridge
- 1. Khi viết các mục phân biệt hoặc đối chiếu giữa hai hay nhiều khái niệm tài chính quan trọng (ví dụ: Vốn chủ sở hữu vs Vốn hóa thị trường), hãy chuyển đổi cấu trúc dạng văn xuôi thành bảng so sánh đối chuẩn trực quan (Table) để tối ưu khả năng đọc lướt (scannability) cho người đọc di động. 2. Phần giới thiệu giải pháp/sản phẩm của DSC (Product Bridge) cần được chi tiết hóa đầy đủ, tránh viết chung chung. (…xem archive)

### Phân nhóm H2 cho bài viết từ điển/glossary và Đặt dấu câu ngoài thẻ bold *(gộp: Đặt dấu câu FAQ ngoài thẻ bold)*
- Đối với các bài viết glossary dạng tổng hợp thuật ngữ, bắt buộc phải chia nhỏ danh sách phẳng thành 5 nhóm chuyên đề H2 rõ ràng để tăng scannability. Các câu hỏi FAQ hoặc list-item in đậm kết thúc bằng dấu chấm hỏi `?` hoặc dấu chấm `.` phải đặt dấu câu đó ra ngoài thẻ bold `**` (ví dụ: `**Câu hỏi**?`) để script QA tách câu chính xác và không đếm gộp nhãn in đậm vào câu trả lời gây lỗi câu quá dài (>30 từ).

### Bản chất NAV và Đính chính Thuật ngữ Lãi suất CCQ
- Đối với các bài viết về chứng chỉ quỹ nhắm đến tệp Người tiết kiệm thận trọng (P1), phải chủ động đính chính thuật ngữ "lãi suất" (vốn là cách gọi quen thuộc nhưng không đúng bản chất của chứng chỉ quỹ) và chuyển đổi sang hiệu suất sinh lời hoặc sự tăng trưởng giá trị tài sản ròng (NAV) để đảm bảo tính chính xác và uy tín chuyên môn. (…xem archive)

### Phân tích chỉ số tài chính theo ngành và xử lý lỗi ngoặc kép "Số cuối kỳ"
- Khi phân tích các chỉ số cơ cấu tài chính (như DAR), luôn đính kèm so sánh định lượng đặc thù từng nhóm ngành cụ thể (như Ngân hàng 88%-92%, Bất động sản 55%-75%, Công nghệ 20%-35%). Tránh dùng dấu ngoặc kép bọc quanh tên các chỉ mục báo cáo tài chính (ví dụ: dùng "cột Số cuối kỳ" thay vì "cột 'Số cuối kỳ'") để tránh trigger lỗi emphatic quotes của QA script.

## Cấu trúc & Định dạng (Structure & Formatting)

### Bảng đối sánh Cờ đuôi nheo vs Lá cờ vs Tam giác & Volume Profile 3 giai đoạn
- Luôn lồng ghép Bảng đối sánh Cờ đuôi nheo (Pennant) vs Mô hình lá cờ (Flag) vs Mô hình tam giác (Triangle) kết hợp quy luật biến động thanh khoản Volume Profile 3 giai đoạn (Cột cờ - Thân cờ cạn vol - Breakout bùng nổ 1,5–2 lần MA20) và phương pháp xử lý bẫy breakout giả khi viết/tối ưu các mô hình giá tiếp diễn cho Active Trader (P3).

### Trình bày trực quan bằng List/Table
- Khi trình bày các số liệu so sánh, mức phí, hoặc quy trình từng bước, ưu tiên sử dụng Bảng (Table) hoặc Danh sách (Bullet list) để bài viết trực quan, dễ đọc, tránh các đoạn văn bản (text) quá dài.

### Tách biệt hoàn toàn visual elements để pass check đoạn văn liên tiếp
- Trong bài viết, các danh sách liệt kê (bullet points, numbered lists) hoặc bảng biểu khi đứng ngay sau một đoạn giới thiệu ngắn (ví dụ: "Các mốc tiến độ bao gồm:") phải được ngăn cách bằng 2 dòng trống (`\n\n`) thay vi viết liền kề. Việc này ngăn chặn script QA tự động đếm gộp đoạn văn và danh sách thành một khối không trực quan dài dòng, đồng thời tạo nhịp đọc thông thoáng cho người dùng.

### Tải cấu trúc đoạn văn theo ngữ nghĩa thay vì chia câu cơ học
- Khi tối ưu cấu trúc đoạn văn để đáp ứng chuẩn Mobile-First (tối đa 3 câu/đoạn, câu dưới 25 từ), phải gộp và ngắt đoạn dựa trên sự liên kết ngữ nghĩa (semantic grouping) của nội dung thay vì bẻ câu hay gộp câu một cách máy móc. Các câu thuộc cùng một khía cạnh giải thích phải nằm chung trong một đoạn (tối đa 3 câu) để đảm bảo mạch văn trôi chảy và tự nhiên.

### Trực quan hóa danh sách để tối ưu độ cô đọng
- Đối với các bài viết tài chính cho F0, tránh lạm dụng các khối văn bản lớn (text-heavy). Hãy cấu trúc lại thông tin thành các danh sách gạch đầu dòng có tiêu đề in đậm làm mốc phân cấp để tăng tính cô đọng và scannable. Các câu chuyện minh họa thực tế nên được trình bày thành các điểm dữ liệu ngắn gọn thay vì viết thành đoạn văn miêu tả dài dòng.

### Cách đặt dấu câu trong list-item/FAQ để tối ưu tách câu
- Khi viết câu hỏi FAQ hoặc list-item bắt đầu bằng thẻ in đậm `**`, hãy đặt dấu chấm `. ` hoặc dấu chấm hỏi `? ` ngay bên ngoài thẻ in đậm (ví dụ: `* **Nhóm hàng hóa tỷ trọng lớn nhất**. Hàng ăn...` thay vì `* **Nhóm hàng hóa tỷ trọng lớn nhất?** Hàng ăn...`). Điều này giúp regex phân tách câu của script QA nhận diện dấu câu chính xác và ngăn chặn hiện tượng gộp đầu dòng thành câu dài quá 25 từ.

### Bỏ qua tạo ảnh fallback khối vuông khi gặp lỗi Quota
- Khi công cụ sinh ảnh AI (`generate_image`) bị báo lỗi Quota (429 RESOURCE_EXHAUSTED), tuyệt đối không sinh các hình ảnh fallback khối vuông 3D bằng script Python PIL. Hãy bỏ qua việc tạo ảnh mới, bảo toàn 100% hình ảnh gốc của bài viết và trình bày bài viết chuẩn văn bản/bảng biểu trực quan.

### Sử dụng dấu chấm ở cuối câu dẫn dắt danh sách liền kề
- Khi viết câu dẫn dắt vào danh sách (bullet points/ordered lists) nằm liền kề (không có dòng trống phân cách), hãy kết thúc câu dẫn dắt bằng dấu chấm `.` thay vì dấu hai chấm `:` để script QA nhận diện và phân tách câu giới thiệu với mục đầu tiên của danh sách, tránh lỗi đếm gộp câu dài quá giới hạn.

### Bảng so sánh đa chiều các loại giá trị cổ phiếu
- Đối với các bài viết giải thích khái niệm dễ gây nhầm lẫn (như Thị giá cổ phiếu - P2/F0), bắt buộc phải tích hợp một Bảng đối sánh đa chiều (Mệnh giá vs Giá trị sổ sách vs Thị giá) để triệt tiêu hoàn toàn sự mơ hồ. Hãy luôn duy trì 100% liên kết tuyệt đối khớp với sitemap live của DSC và đặt dấu hai chấm `:` ở cuối nhãn in đậm trong danh sách để tuân thủ định dạng.

### Bảng phân nhóm LLR và Loại bỏ LaTeX
- Đối với các bài viết về chỉ số tài chính chuyên sâu (như Tỷ lệ bao phủ nợ xấu - LLR), bắt buộc phải có Bảng phân nhóm trực quan các ngưỡng an toàn của chỉ số và ý nghĩa đầu tư thực tế cho từng nhóm. Không sử dụng ký tự LaTeX (như $ hoặc $$) cho công thức tính toán mà hãy sử dụng định dạng chữ in đậm thông thường để tránh lỗi hiển thị trên CMS. (…xem archive)

### Định dạng số thập phân bằng dấu phẩy và Hướng dẫn thực hành cho Active Trader (P3)
- 1. **Định dạng số thập phân tiếng Việt:** Bắt buộc sử dụng dấu phẩy `,` thay vì dấu chấm `.` cho số thập phân khi viết bài tiếng Việt (ví dụ: `T+1,5` thay vì `T+1.5`, phí `0,1%` thay vì `0.1%`, margin `13,5%` thay vì `13.5%`). Điều này vừa giúp tuân thủ chính xác quy tắc chính tả tiếng Việt của brand, vừa tránh lỗi QA script nhận diện nhầm dấu chấm thập phân là dấu chấm hết câu gây tách câu sai lệch. 2. (…xem archive)

### Tiết giảm mốc thời gian động và bổ sung quy định NFC/CCCD
- 1. Tránh lạm dụng mốc thời gian động (ví dụ: "Tính đến tháng 8/2026,") ở đầu mọi tiêu đề H2 hoặc phần quy định pháp luật chung. Chỉ dùng mốc thời gian động ở những câu thực sự chứa số liệu/thống kê biến động (như biểu phí, số lượng tài khoản, lãi suất). Đa dạng hóa cách viết tự nhiên (ví dụ: "Theo quy chế hiện hành...", "Thống kê nội bộ tháng 8/2026 cho thấy...", "Theo thông tin dịch vụ cập nhật tháng 8/2026..."). 2. (…xem archive)

### Phân tách câu hỏi và câu trả lời trong mục FAQs
- Phân tách câu hỏi và câu trả lời trong mục FAQs bằng dòng trống để script QA không đếm gộp thành câu dài.

### Ma trận 2D kết hợp QoQ x YoY và Bóc tách bẫy mùa vụ cho chỉ số kết quả kinh doanh quý
- Đối với các bài viết về chỉ số tài chính kết quả kinh doanh quý (như QoQ), luôn tích hợp Ma trận 2D kết hợp giữa QoQ và YoY (4 kịch bản: Tăng tốc, Phục hồi, Cảnh báo, Suy thoái) và phân tích chiều sâu về bẫy mùa vụ (Seasonality) trong các ngành đặc thù (bán lẻ Q4, bất động sản) để nâng cao tính định lượng thực chiến cho nhà đầu tư (P3 & P2).

### Mô phỏng lộ trình thặng dư và chuyển dịch dòng tiền cho bài viết quản lý nợ cá nhân
- Đối với các chủ đề về phương pháp tài chính cá nhân/trả nợ (như Quả cầu tuyết), luôn kết hợp cơ sở tâm lý học hành vi (Small Wins) với bảng mô phỏng lộ trình dòng tiền thực tế từng tháng và lộ trình chuyển dịch thặng dư sang kênh đầu tư tích lũy DSC.

### Phân rã Target word count cho dạng Toplist và Đối sánh rủi ro pháp lý tài sản số
- Khi viết các bài thuộc dạng Toplist đánh giá sản phẩm/dịch vụ tài chính hoặc tiền điện tử, luôn phân rã target word count chi tiết cho từng mục H3 trong outline để script QA đếm chính xác, đồng thời tích hợp Bằng chứng dự trữ (Proof of Reserves) và bảng đối sánh rủi ro ngắt kết nối pháp lý giữa thị trường tiền điện tử và kênh đầu tư chứng khoán chính thống được UBCKNN bảo hộ.

## Sản phẩm & Thương hiệu (Products & Brand Context)

### Ưu tiên Môi giới 1:1 trong Product Bridge
- Khi viết bài về phân tích kỹ thuật chuyên sâu cho Active Traders, hãy ưu tiên dẫn dắt về dịch vụ Môi giới 1:1 và Mở tài khoản eKYC thay vì các công cụ Tư vấn số tự động, để tạo sự tin cậy và cá nhân hóa.

### Ràng buộc về năng lực sản phẩm thực tế của thương hiệu
- Trước khi viết bất kỳ Product Bridge hay ví dụ thực tiễn nào liên quan đến sản phẩm tài chính, luôn kiểm tra chéo năng lực sản phẩm và dịch vụ thực tế của định chế. Nếu định chế không cung cấp sản phẩm đó (ví dụ: DSC không hỗ trợ giao dịch phái sinh), tuyệt đối không kêu gọi mở tài khoản phái sinh hay đề cập tỷ lệ ký quỹ tại đây. (…xem archive)

### Phân tích liên thị trường và tác động chuỗi cung ứng cho chỉ số chứng khoán quốc tế
- Khi phân tích các chỉ số chứng khoán quốc tế (như KOSPI, Nikkei 225, Dow Jones), luôn tích hợp góc nhìn Phân tích liên thị trường (Intermarket Analysis) kết nối với thị trường Việt Nam (tác động chuỗi cung ứng, dòng vốn FDI, độ lệch múi giờ giao dịch) và các cơ chế quản trị rủi ro hạ nhiệt thị trường (Circuit Breaker) để cung cấp giá trị thực chiến vượt trội cho Active Trader (P3).

## ✅ Đã tự động hoá bởi `scripts/qa_lint.py` (vẫn phải tuân thủ khi viết)

| Bản năng | Check |
|---|---|
| Tránh mở bài vĩ mô | `CL2-blacklist` |
| Loại bỏ ngoặc kép nhấn mạnh (Emphatic Quotes) | `CL2-quotes` |
| Sử dụng từ Chiến lược thay cho Thủ thuật hoặc Chiêu trò | `CL2-softban` |
| Tránh sử dụng thuật ngữ "cơ chế truyền dẫn" | `CL2-softban` |
| Loại bỏ công thức LaTeX và tối ưu đếm câu list-item | `FMT-latex + CL6-list-item` |
| Thống nhất thời gian đăng ký eKYC DSC và loại bỏ từ dạng xương máu | `CL5-fact + CL2-softban` |
| Hợp nhất các danh sách liên tiếp để tránh đứt đoạn mạch đọc | `CL6-lists` |
| Tránh sử dụng callout box không tương thích | `FMT-callout` |
| Tách biệt list-item chứa nhiều câu và loại bỏ từ trigger "rõ ràng" | `CL6-list-item + CL2-softban` |
| Tránh sử dụng dấu ngoặc kép trong YAML front matter | `FM-quotes` |
| Tuyệt đối không dùng lưu đồ Code Block (ASCII Art) cho CMS | `FMT-codeblock` |
| Bắt buộc có Internal Link dẫn về trang Mở tài khoản chứng khoán DSC | `LINK-cta` |
| Tiêu đề SEO (Title) Bắt buộc Tối đa 59 Ký tự | `CL1-title` |
| Bắt buộc dùng Đường dẫn Tuyệt đối (Absolute URLs & Absolute Paths) | `LINK-relative / LINK-local` |
| Viết đoạn văn ngữ cảnh tự nhiên cho Internal Link (Không dùng "Xem thêm") | `LINK-anchor` |
| Định dạng nhãn in đậm trong danh sách (Sử dụng dấu hai chấm) | `FMT-bold-label` |
| Không sử dụng đường kẻ ngang giữa các phần/heading | `FMT-hr` |
| Đối soát Internal Link với Sitemap Live từ nguồn chính thức | `LINK-sitemap` |
