# Continuous Learning: Instincts Archive (Kho lưu trữ Bản năng đầy đủ)

> **Mô tả:** Đây là kho lưu trữ lịch sử đầy đủ của các bản năng đã học, bao gồm thông tin chi tiết về nguồn, feedback của user, trạng thái và phạm vi.
> **Mục đích:** Dùng cho skill `/learn` để đối chiếu, phân tích và tránh trùng lặp. Các agent viết bài thông thường không cần đọc file này để tiết kiệm token.

---

> **Bắt buộc:** Mọi agent, skill, và workflow đều phải đọc file này trước khi thực thi.
> **Cập nhật:** Được auto-append sau mỗi `/approve` hoặc thủ công qua `/learn`.

File này lưu trữ những "bản năng" mà hệ thống AI học được qua quá trình sửa bài cùng người dùng.
Mỗi khi người dùng đưa ra phản hồi chỉnh sửa, hãy trích xuất nguyên lý và lưu vào đây.

---

## Format chuẩn cho mỗi bản năng

```
### [Tên ngắn gọn]
- **Trạng thái:** ACTIVE / DEPRECATED
- **Nguồn:** [Tên bài viết hoặc "Global feedback"]
- **Phản hồi từ User:** "[Quote phản hồi gốc]"
- **Bản năng:** [Quy tắc hành động cụ thể]
- **Phạm vi:** [Global / Chỉ topic: X]
```

---

## Bản năng Active

### Tránh mở bài vĩ mô
- **Trạng thái:** ACTIVE
- **Nguồn:** Feedback chung
- **Phản hồi từ User:** "Đừng bao giờ mở bài bằng cụm 'Trong kỷ nguyên số ngày nay...'"
- **Bản năng:** Mở bài đi thẳng vào vấn đề cụ thể của người dùng. Không dạo đầu bằng bối cảnh vĩ mô (kỷ nguyên số, thế giới công nghệ, thị trường biến động...).
- **Phạm vi:** Global

### Loại bỏ ngoặc kép nhấn mạnh (Emphatic Quotes)
- **Trạng thái:** ACTIVE
- **Nguồn:** adx-la-gi
- **Phản hồi từ User:** "sao tôi thấy đang sử dụng các ngoặc kép. Loại bỏ kiểu trình bày nài, AI quá"
- **Bản năng:** Tuyệt đối không sử dụng dấu ngoặc kép cho các cụm từ ẩn dụ, ví von hoặc thuật ngữ thông thường (ví dụ: đu đỉnh, vùng kiếm tiền). Viết thẳng và trực diện để tránh cảm giác máy móc.
- **Phạm vi:** Global

### Ưu tiên Môi giới 1:1 trong Product Bridge
- **Trạng thái:** ACTIVE
- **Nguồn:** adx-la-gi
- **Phản hồi từ User:** "dẫn về dịch vụ môi giới chứng khoán hoặc mở tài khoản chứng khoán DSC thay vì tư vấn số nhé"
- **Bản năng:** Khi viết bài về phân tích kỹ thuật chuyên sâu cho Active Traders, hãy ưu tiên dẫn dắt về dịch vụ Môi giới 1:1 và Mở tài khoản eKYC thay vì các công cụ Tư vấn số tự động, để tạo sự tin cậy và cá nhân hóa.
- **Phạm vi:** Global

### Thỏa mãn Search Intent kỹ thuật trong bài phân tích
- **Trạng thái:** ACTIVE
- **Nguồn:** bao-cao-luu-chuyen-tien-te
- **Phản hồi từ User:** (Tham khảo AI Overview)
- **Bản năng:** Đối với các bài viết về báo cáo tài chính hoặc công cụ kỹ thuật, ngoài việc phân tích chiến lược cho nhà đầu tư, cần bổ sung các kiến thức nền tảng như 'Phương pháp lập' hoặc 'Cấu tạo chi tiết'. Điều này giúp thỏa mãn các truy vấn tìm kiếm mang tính học thuật mà không làm loãng ảnh hưởng chiến lược của DSC.
- **Phạm vi:** Global

### Tuân thủ độ dài đoạn và cấu trúc Heading chuẩn
- **Trạng thái:** ACTIVE
- **Nguồn:** phi-giao-dich-chung-khoan
- **Phản hồi từ User:** QA script `count_words.py` báo sai lệch khi dùng sai thẻ Heading.
- **Bản năng:** Khi chuyển từ Outline sang Draft, luôn sử dụng Markdown Headings tiêu chuẩn (`#`, `##`, `###`) thay vì giữ nguyên các chuỗi định dạng của Outline (`### H2:`). Điều này đảm bảo Script QA hoạt động chính xác khi cắt block nội dung.
- **Phạm vi:** Global

### Trình bày trực quan bằng List/Table
- **Trạng thái:** ACTIVE
- **Nguồn:** phi-luu-ky-chung-khoan
- **Phản hồi từ User:** "trình bày bài viết linh hoạt giữa list, table thay vì chỉ có text thôi"
- **Bản năng:** Khi trình bày các số liệu so sánh, mức phí, hoặc quy trình từng bước, ưu tiên sử dụng Bảng (Table) hoặc Danh sách (Bullet list) để bài viết trực quan, dễ đọc, tránh các đoạn văn bản (text) quá dài.
- **Phạm vi:** Global

### Bắt buộc có Sapo và Link CTA
- **Trạng thái:** ACTIVE
- **Nguồn:** phi-luu-ky-chung-khoan
- **Phản hồi từ User:** "chưa thấy dẫn về mở tài khoản", "chưa thấy có phần sapo bài viết"
- **Bản năng:** Mọi bài viết phải có đoạn Sapo (Mở bài) ngay dưới tiêu đề H1. Trong phần Kết bài (CTA), phải luôn chèn link trực tiếp đến trang mở tài khoản chứng khoán hoặc bài hướng dẫn tương ứng, không được để lời kêu gọi suông.
- **Phạm vi:** Global

### Sử dụng từ Chiến lược thay cho Thủ thuật hoặc Chiêu trò
- **Trạng thái:** ACTIVE
- **Nguồn:** bollinger-bands-la-gi
- **Phản hồi từ User:** "dùng từ chiến lược hơn từ thủ thuật", "từ chiêu trò nghe không chuyên nghiệp", "kinh điển giống văn nói"
- **Bản năng:** Khi phân tích các phương pháp giao dịch, chỉ báo kỹ thuật hoặc các thủ pháp tài chính chuyên sâu cho Active Trader (P3), luôn sử dụng từ "chiến lược" hoặc "phương pháp" thay cho "thủ thuật" hay "chiêu trò". Điều này đảm bảo giọng văn mang tính chuyên nghiệp cao cấp, chuẩn mực ngôn từ của một định chế tài chính (Investment Bank tone) đồng hành cùng nhà đầu tư.
- **Phạm vi:** Global

### Tránh sử dụng thuật ngữ "cơ chế truyền dẫn"
- **Trạng thái:** ACTIVE
- **Nguồn:** cac-chi-so-phan-tich-bao-cao-tai-chinh
- **Phản hồi từ User:** "'cơ chế truyền dẫn' không phải từ ngữ phù hợp trong văn viết, đặc biệt là lĩnh vực tài chính. Viết là Tác động là được rồi. Không cần cơ chế đâu"
- **Bản năng:** Không sử dụng cụm từ "cơ chế truyền dẫn" trong các bài viết tài chính hay kinh tế vĩ mô. Hãy thay thế hoàn toàn bằng từ "tác động" để đảm bảo câu văn ngắn gọn, dễ hiểu, phù hợp với văn phong chuyên nghiệp và tự nhiên của nhà đầu tư.
- **Phạm vi:** Global

### Loại bỏ công thức LaTeX và tối ưu đếm câu list-item
- **Trạng thái:** ACTIVE
- **Nguồn:** chia-tach-co-phieu
- **Phản hồi từ User:** "phần công thức lên docs sẽ bị lỗi. Sửa lại" + "word count / sentence length check"
- **Bản năng:** Tuyệt đối không sử dụng định dạng LaTeX `$$` hay `$` cho các công thức tính toán tài chính vì dễ gây lỗi hiển thị trên CMS. Thay thế bằng công thức in đậm chuẩn trực quan (ví dụ: `**P' = P / (1 + a)**`). Đối với các danh sách (list-item) hoặc câu định nghĩa bắt đầu bằng cụm in đậm có dấu hai chấm `: `, hãy thay thế `:` bằng dấu chấm `. ` để ngăn script QA đếm gộp thành câu dài quá 25 từ, đồng thời giúp câu văn gãy gọn hơn.
- **Phạm vi:** Global

### Ràng buộc từ khóa Sapo, Bridge hỗ trợ tư vấn và Miễn trừ trách nhiệm
- **Trạng thái:** ACTIVE
- **Nguồn:** co-nen-mua-co-phieu-las
- **Phản hồi từ User:** "sapo chưa chứa từ khóa 'có nên mua cổ phiếu LAS không'. Phần dẫn về DSC ko có nói về hỗ trợ tư vấn đầu tư. Chưa có phần miễn trừ trách nhiệm. viết vào thành 1 điểm liệt kê thay vì tách riêng ra thành tip"
- **Bản năng:**
  1. Luôn bảo đảm đoạn Sapo đầu bài viết chứa từ khóa chính xác dạng truy vấn (như "có nên mua cổ phiếu LAS không") một cách tự nhiên.
  2. Phần dẫn dắt dịch vụ DSC (Product Bridge) bắt buộc phải tích hợp rõ ràng thông tin "hỗ trợ tư vấn đầu tư" từ chuyên gia Môi giới 1:1. Đồng thời, nên gộp thông tin này thành một điểm liệt kê (bullet point) đồng nhất thay vì tách riêng thành hộp Tip để liền mạch với hệ sinh thái.
  3. Bắt buộc chèn hộp cảnh báo "Tuyên bố miễn trừ trách nhiệm" rõ ràng ở phần đánh giá hoặc cuối bài viết để đảm bảo tính khách quan pháp lý.
- **Phạm vi:** Global

### Tách biệt hoàn toàn visual elements để pass check đoạn văn liên tiếp
- **Trạng thái:** ACTIVE
- **Nguồn:** co-nen-mua-co-phieu-novaland
- **Phản hồi từ User:** "consecutive paragraphs check"
- **Bản năng:** Trong bài viết, các danh sách liệt kê (bullet points, numbered lists) hoặc bảng biểu khi đứng ngay sau một đoạn giới thiệu ngắn (ví dụ: "Các mốc tiến độ bao gồm:") phải được ngăn cách bằng 2 dòng trống (`\n\n`) thay vi viết liền kề. Việc này ngăn chặn script QA tự động đếm gộp đoạn văn và danh sách thành một khối không trực quan dài dòng, đồng thời tạo nhịp đọc thông thoáng cho người dùng.
- **Phạm vi:** Global

### Ràng buộc về năng lực sản phẩm thực tế của thương hiệu
- **Trạng thái:** ACTIVE
- **Nguồn:** chung-khoan-phai-sinh-la-gi
- **Phản hồi từ User:** "DSC k có trading phái sinh nên k dẫn về mở tk giao dịch phái sinh được"
- **Bản năng:** Trước khi viết bất kỳ Product Bridge hay ví dụ thực tiễn nào liên quan đến sản phẩm tài chính, luôn kiểm tra chéo năng lực sản phẩm và dịch vụ thực tế của định chế. Nếu định chế không cung cấp sản phẩm đó (ví dụ: DSC không hỗ trợ giao dịch phái sinh), tuyệt đối không kêu gọi mở tài khoản phái sinh hay đề cập tỷ lệ ký quỹ tại đây. Hãy định hướng người dùng rèn luyện kiến thức và xây dựng nền tảng vững chắc thông qua sản phẩm cơ sở (như cổ phiếu cơ sở), đồng thời sử dụng các dịch vụ hỗ trợ của định chế (như Môi giới 1:1, mở tài khoản eKYC cổ phiếu) để tích lũy kinh nghiệm.
- **Phạm vi:** Global

### Thống nhất thời gian đăng ký eKYC DSC và loại bỏ từ dạng xương máu
- **Trạng thái:** ACTIVE
- **Nguồn:** cach-dau-tu-chung-khoan-cho-nguoi-moi-bat-dau
- **Phản hồi từ User:** "bỏ từ dạng xương máu đi. ekyc chỗ thì 3 phút, 5 phút giờ lại 30 giây. thống nhất lại"
- **Bản năng:**
  1. Tuyệt đối không sử dụng từ ngữ giật gân, thiếu chuyên nghiệp như "xương máu" khi viết bài tư vấn đầu tư. Thay thế bằng các cụm từ trung tính, sang trọng và chuẩn mực như "quý báu", "sống còn", "cốt lõi".
  2. Thống nhất thời gian mở tài khoản định danh điện tử eKYC tại DSC là "3 phút" trên toàn hệ thống bài viết để đảm bảo tính đồng bộ dữ liệu thương hiệu và độ tin cậy.
- **Phạm vi:** Global

### Tải cấu trúc đoạn văn theo ngữ nghĩa thay vì chia câu cơ học
- **Trạng thái:** ACTIVE
- **Nguồn:** quy-dong-la-gi
- **Phản hồi từ User:** "việc ngắt của bạn đang ko theo nội dung. sau cái đầu tiên ko ngắt mà cái thứ 2 lại ngắt"
- **Bản năng:** Khi tối ưu cấu trúc đoạn văn để đáp ứng chuẩn Mobile-First (tối đa 3 câu/đoạn, câu dưới 25 từ), phải gộp và ngắt đoạn dựa trên sự liên kết ngữ nghĩa (semantic grouping) của nội dung thay vì bẻ câu hay gộp câu một cách máy móc. Các câu thuộc cùng một khía cạnh giải thích phải nằm chung trong một đoạn (tối đa 3 câu) để đảm bảo mạch văn trôi chảy và tự nhiên.
- **Phạm vi:** Global

### Trực quan hóa danh sách để tối ưu độ cô đọng
- **Trạng thái:** ACTIVE
- **Nguồn:** quy-tuong-ho-la-gi
- **Phản hồi từ User:** "bài viết đang toàn text, dài. cô đọng hơn"
- **Bản năng:** Đối với các bài viết tài chính cho F0, tránh lạm dụng các khối văn bản lớn (text-heavy). Hãy cấu trúc lại thông tin thành các danh sách gạch đầu dòng có tiêu đề in đậm làm mốc phân cấp để tăng tính cô đọng và scannable. Các câu chuyện minh họa thực tế nên được trình bày thành các điểm dữ liệu ngắn gọn thay vì viết thành đoạn văn miêu tả dài dòng.
- **Phạm vi:** Global

### Hợp nhất các danh sách liên tiếp để tránh đứt đoạn mạch đọc
- **Trạng thái:** ACTIVE
- **Nguồn:** quy-trai-phieu-la-gi
- **Phản hồi từ User:** "Tham khảo nội dung AI overview trên để tối ưu" (Đặc điểm nổi bật + Ai nên đầu tư)
- **Bản năng:** Khi gặp các nội dung phân loại liệt kê liên tiếp (như Đặc điểm nổi bật và Đối tượng phù hợp), tránh thiết lập các khối danh sách (bullet list) đứng kề nhau. Hãy hợp nhất chúng thành một danh sách kết hợp hoặc viết thêm một đoạn văn xuôi ngắn ở giữa làm cầu nối dẫn dắt để mạch đọc tự nhiên và pass QA.
- **Phạm vi:** Global

---

### Tránh sử dụng callout box không tương thích
- **Trạng thái:** ACTIVE
- **Nguồn:** dcf-la-gi
- **Phản hồi từ User:** "các phần quote kiểu > [!NOTE] ko hoạt động trên website tôi nên bỏ đi"
- **Bản năng:** Không sử dụng cú pháp callout mở rộng của Markdown (như `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`) vì chúng không tương thích hiển thị trên một số CMS. Hãy thay thế bằng cú pháp trích dẫn chuẩn của Markdown kết hợp tiêu đề in đậm (ví dụ: `> **Lưu ý:**` hoặc `> **Mẹo:**`).
- **Phạm vi:** Global

### Cách đặt dấu câu trong list-item/FAQ để tối ưu tách câu
- **Trạng thái:** ACTIVE
- **Nguồn:** chi-so-gia-tieu-dung-cpi-la-gi-va-moi-quan-he-voi-thi-truong-chung-khoan
- **Phản hồi từ User:** Lỗi "Sentence too long" do script QA gộp câu trong danh sách hoặc FAQ.
- **Bản năng:** Khi viết câu hỏi FAQ hoặc list-item bắt đầu bằng thẻ in đậm `**`, hãy đặt dấu chấm `. ` hoặc dấu chấm hỏi `? ` ngay bên ngoài thẻ in đậm (ví dụ: `* **Nhóm hàng hóa tỷ trọng lớn nhất**. Hàng ăn...` thay vì `* **Nhóm hàng hóa tỷ trọng lớn nhất?** Hàng ăn...`). Điều này giúp regex phân tách câu của script QA nhận diện dấu câu chính xác và ngăn chặn hiện tượng gộp đầu dòng thành câu dài quá 25 từ.
- **Phạm vi:** Global

---

### Tách biệt list-item chứa nhiều câu và loại bỏ từ trigger "rõ ràng"
- **Trạng thái:** ACTIVE
- **Nguồn:** loi-nhuan-rong-va-loi-nhuan-sau-thue
- **Phản hồi từ User:** Lỗi "Paragraph too many sentences" do script QA gộp các list item và cảnh báo từ trigger "rõ ràng".
- **Bản năng:**
  1. Với các danh sách gạch đầu dòng (list-item) mà mỗi dòng chứa từ 2 câu trở lên, luôn chèn một dòng trống ngăn cách giữa các dòng. Điều này giúp ngăn script QA tự động gộp các câu thành một đoạn văn quá dài (> 3 câu), đồng thời làm thoáng bố cục trên giao diện di động.
  2. Tuyệt đối không sử dụng từ trigger rỗng nghĩa như "rõ ràng" (ví dụ: "phân biệt rõ ràng") để đảm bảo văn phong chuyên nghiệp và khách quan.
- **Phạm vi:** Global

---

### Tối ưu hóa cầu nối sản phẩm chuyển dịch dòng vốn và trực quan hóa các yếu tố vĩ mô
- **Trạng thái:** ACTIVE
- **Nguồn:** cach-dau-tu-vang
- **Phản hồi từ User:** "Những yếu tố ảnh hưởng đến sự biến động của giá vàng viết theo dạng list để dễ skim ý chính. Phần chuyển từ đầu tư vàng sang đầu tư chứng khoán DSC chưa được tối ưu"
- **Bản năng:**
  1. Khi viết các yếu tố tác động vĩ mô (ví dụ: yếu tố tác động đến giá vàng, giá dầu), luôn trình bày dưới dạng danh sách gạch đầu dòng có in đậm tiêu đề để tăng tính trực quan và dễ skim ý chính cho người đọc.
  2. Phần dẫn dắt chuyển dịch dòng tiền (Product Bridge) từ các kênh phòng thủ (như vàng, gửi tiết kiệm) sang kênh cổ phiếu tăng trưởng/chứng chỉ quỹ của DSC phải được lập luận bằng logic tài chính (rủi ro mua đuổi vùng đỉnh, chênh lệch spread rộng của vàng vật chất, tính chất không sinh dòng tiền thụ động của vàng so với lợi thế cổ tức tiền mặt của cổ phiếu) để tạo động lực chuyển dịch tài sản một cách tự nhiên và thuyết phục.
- **Phạm vi:** Global
---

### Tránh sử dụng dấu ngoặc kép trong YAML front matter
- **Trạng thái:** ACTIVE
- **Nguồn:** co-tien-nen-dau-tu-bac
- **Phản hồi từ User:** Lỗi Emphatic Quotes từ script QA do phát hiện dấu ngoặc kép bao quanh chuỗi ký tự trong YAML front matter.
- **Bản năng:** Khi định nghĩa các trường văn bản trong YAML front matter (như Featured_Snippet, Anti_AI_Flags), không bao quanh chuỗi bằng dấu ngoặc kép kép (`""`). Hãy viết trực tiếp chuỗi không có dấu ngoặc kép hoặc dùng dấu ngoặc đơn (`''`) để tránh trigger nhầm bộ quét Emphatic Quotes của Quality Guardian.
- **Phạm vi:** Global

---

### Đặt dấu câu FAQ ngoài thẻ bold
- **Trạng thái:** ACTIVE
- **Nguồn:** dau-tu-vang-nen-mua-loai-na
- **Phản hồi từ User:** QA script báo câu quá dài ở FAQ vì script đọc text bên trong bold tag cộng với dấu hỏi cuối là một câu liên tục.
- **Bản năng:** Với câu hỏi FAQ dạng `**Câu hỏi?**`, phải di chuyển dấu `?` ra ngoài thẻ bold: `**Câu hỏi**?`. Điều này giúp QA script tách câu đúng vị trí và không tính phần bold label vào độ dài câu trả lời.
- **Phạm vi:** Global

---

### Sử dụng số liệu vĩ mô thực tế tại Việt Nam
- **Trạng thái:** ACTIVE
- **Nguồn:** he-so-icor-la-gi
- **Phản hồi từ User:** Phê duyệt đề xuất đưa số liệu thực tế Việt Nam thay cho số liệu giả định chung chung.
- **Bản năng:** Đối với các bài viết phân tích vĩ mô, bắt buộc phải sử dụng các số liệu thực tế đã được công bố của Việt Nam trong các giai đoạn gần nhất (ví dụ: giai đoạn phục hồi 2021-2025, mục tiêu 2026) thay vì sử dụng các số liệu giả định chung chung. Điều này nhằm tối đa hóa độ tin cậy và chiều sâu phân tích của DSC.
- **Phạm vi:** Chỉ topic: Vĩ mô

---

### Bảng so sánh định nghĩa & Chi tiết hóa Product Bridge
- **Trạng thái:** ACTIVE
- **Nguồn:** von-hoa-thi-truong-la-gi
- **Phản hồi từ User:** "phần content về DSC ngắn quá, phần Sự khác biệt giữa vốn hóa thị trường và vốn chủ sở hữu có thể tạo dạng bảng", "nhiều phần ngắn thì ko cần phải tách ra thành H3 đâu, viết thành list luôn"
- **Bản năng:**
  1. Khi viết các mục phân biệt hoặc đối chiếu giữa hai hay nhiều khái niệm tài chính quan trọng (ví dụ: Vốn chủ sở hữu vs Vốn hóa thị trường), hãy chuyển đổi cấu trúc dạng văn xuôi thành bảng so sánh đối chuẩn trực quan (Table) để tối ưu khả năng đọc lướt (scannability) cho người đọc di động.
  2. Phần giới thiệu giải pháp/sản phẩm của DSC (Product Bridge) cần được chi tiết hóa đầy đủ, tránh viết chung chung. Hãy giới thiệu cụ thể các dịch vụ thực tế như: tính năng phân loại vốn hóa/cảnh báo giá trên App DSC Trading, quy trình mở tài khoản eKYC 3 phút, dịch vụ Môi giới 1:1 hỗ trợ cá nhân hóa danh mục, và chính sách phí giao dịch ưu đãi chỉ từ 0.1% cùng báo cáo phân tích miễn phí.
  3. Đối với các phần giới thiệu dịch vụ ngắn hoặc phần thông tin phụ có độ dài ít câu (2-3 câu mỗi phần), không cần chia nhỏ bằng tiêu đề H3 mà hãy gộp chung thành một danh sách gạch đầu dòng (bulleted list) có in đậm tiêu đề ở đầu mỗi bullet để tăng tính liền mạch và gọn gàng.
- **Phạm vi:** Global

---

### Tuyệt đối không dùng lưu đồ Code Block (ASCII Art) cho CMS
- **Trạng thái:** ACTIVE
- **Nguồn:** quan-tri-rui-ro-la-gi
- **Phản hồi từ User:** "phần lưu đồ trong CMS ko hiển thị được. Cập nhật lại skill liên quan đến internal link"
- **Bản năng:** CMS website không hỗ trợ tốt hiển thị các khối code block lưu đồ/sơ đồ ASCII (`+---+`, `[Bước 1] -> [Bước 2]`, cây phân nhánh), gây vỡ layout và không tối ưu trên di động. Bắt buộc chuyển đổi toàn bộ lưu đồ, quy trình và phân loại thành Bảng Markdown (Table), Danh sách đánh số từng bước (Ordered List), hoặc khối trích dẫn (Blockquote). Công thức toán học biểu diễn bằng chữ in đậm thông thường thay vì khối LaTeX.
- **Phạm vi:** Global

---

### Xác thực Internal Link bằng Sitemap Live của DSC
- **Trạng thái:** ACTIVE
- **Nguồn:** quan-tri-rui-ro-la-gi
- **Phản hồi từ User:** "phần gợi ý internal link tôi muốn cào dữ liệu sitemap (https://www.dsc.com.vn/sitemap/sitemap_knowledge.xml) để gợi ý chính xác hơn"
- **Bản năng:** Khi gợi ý hoặc gắn internal link, bắt buộc phải cào dữ liệu trực tiếp từ sitemap knowledge của DSC (`https://www.dsc.com.vn/sitemap/sitemap_knowledge.xml`) để lấy danh sách URL live thực tế. Tuyệt đối không tự suy đoán slug hoặc dùng đường dẫn tương đối không kiểm chứng. Chọn anchor text chứa từ khóa ngữ cảnh tự nhiên nhất để tối ưu sức mạnh liên kết nội bộ.
- **Phạm vi:** Global

---

### Bắt buộc có Internal Link dẫn về trang Mở tài khoản chứng khoán DSC
- **Trạng thái:** ACTIVE
- **Nguồn:** quan-tri-rui-ro-la-gi
- **Phản hồi từ User:** "trang này cơ mà: https://www.dsc.com.vn/mo-tai-khoan trang bạn đề xuất target key 'cách mở tài khoản chứng khoán' cơ"
- **Bản năng:** 100% mọi bài viết trong toàn bộ pipeline (Drafting, Optimize, Write, Link) bắt buộc phải gắn ít nhất 01 link chuyển đổi dẫn trực tiếp về Landing Page Mở tài khoản chứng khoán chính thức của DSC: `https://www.dsc.com.vn/mo-tai-khoan` (không nhầm với bài blog chia sẻ kiến thức có target key "cách mở tài khoản chứng khoán" tại `/kien-thuc/cach-mo-tai-khoan-chung-khoan`). Vị trí đặt: Phần Product Bridge hoặc đoạn Kết luận (Call to Action). Anchor text tự nhiên: `mở tài khoản chứng khoán`, `mở tài khoản chứng khoán online`, `mở tài khoản trực tuyến eKYC tại DSC`, `mở tài khoản eKYC tại DSC`.
- **Phạm vi:** Global

---

### Tiêu đề SEO (Title) Bắt buộc Tối đa 59 Ký tự
- **Trạng thái:** ACTIVE
- **Nguồn:** thao-tung-thi-truong-chung-khoan-la-gi
- **Phản hồi từ User:** "title đề xuất quá 60 ký tự. check lại và cập nhật skill liên quan"
- **Bản năng:** Mọi Tiêu đề SEO (SEO Title / Title đề xuất trong Proposal / Outline Title) BẮT BUỘC có độ dài tối đa 59 ký tự (bao gồm cả khoảng trắng và dấu câu) và chứa từ khóa chính (Target Keyword) ngay đầu hoặc giữa tiêu đề. Điều này đảm bảo tiêu đề không bị Google cắt bớt (truncate) trên trang kết quả tìm kiếm (SERP), tối ưu tỷ lệ click (CTR). Luôn đếm ký tự chính xác trước khi xuất báo cáo Proposal hoặc bài viết.
- **Phạm vi:** Global

---

### Bắt buộc dùng Đường dẫn Tuyệt đối (Absolute URLs & Absolute Paths)
- **Trạng thái:** ACTIVE
- **Nguồn:** thao-tung-thi-truong-chung-khoan-la-gi
- **Phản hồi từ User:** "dùng absolute path nhé"
- **Bản năng:**
  1. **Internal Links trong bài viết:** 100% internal links và conversion links trong bài viết SEO bắt buộc dùng URL tuyệt đối đầy đủ (`https://www.dsc.com.vn/kien-thuc/[slug]` hoặc `https://www.dsc.com.vn/mo-tai-khoan`), tuyệt đối không dùng relative path dạng `/kien-thuc/...` hay `/mo-tai-khoan`.
  2. **File Paths khi tương tác:** Luôn dẫn link và tham chiếu file bằng absolute path đầy đủ trong workspace/hệ thống.
- **Phạm vi:** Global

---

### Xác thực Internal Link bằng Sitemap Live của DSC (Bắt buộc)
- **Trạng thái:** ACTIVE
- **Nguồn:** Global feedback (duong-trendline-la-gi)
- **Phản hồi từ User:** "có 1 vấn đề là internal link đang ko quét sitemap mà chỉ lấy các bài viết ở folder 4-content"
- **Bản năng:** Khi tạo hoặc tối ưu bài viết, tuyệt đối không dùng link file cục bộ (`file:///...` hoặc `.md`) làm internal link. Phải đọc trực tiếp sitemap live `https://www.dsc.com.vn/sitemap/sitemap_knowledge.xml` để lấy URL tuyệt đối của bài viết đích. Đồng thời, đối chiếu kỹ slug của file cục bộ với sitemap để tránh sai lệch cấu trúc URL (ví dụ: file `Final-rsi-la-gi.md` trên sitemap live có URL là `https://www.dsc.com.vn/kien-thuc/chi-so-rsi-la-gi`, file `Final-chi-bao-ky-thuat-la-gi.md` có URL là `https://www.dsc.com.vn/kien-thuc/chi-bao-ky-thuat`).
- **Phạm vi:** Global

---

### Viết đoạn văn ngữ cảnh tự nhiên cho Internal Link (Không dùng "Xem thêm")
- **Trạng thái:** ACTIVE
- **Nguồn:** bien-do-giao-dong-gia-co-phieu-la-gi
- **Phản hồi từ User:** "phần >> xem thêm có thể viết đoạn ngữ nghĩa để internal link"
- **Bản năng:** Thay vì sử dụng các khối liên kết thô cứng ngắt mạch đọc của người dùng dạng `*>> Xem thêm:* [***Tên bài viết***](URL)`, hãy chuyển đổi và tích hợp liên kết nội bộ (internal link) một cách tự nhiên vào một câu hoặc đoạn văn có đầy đủ ngữ cảnh ngữ nghĩa liên quan. Điều này vừa giúp tối ưu trải nghiệm đọc (UX) vừa nâng cao hiệu quả truyền tải dòng chảy tin cậy (Link Juice) cho SEO.
- **Phạm vi:** Global

---

### Định dạng nhãn in đậm trong danh sách (Sử dụng dấu hai chấm)
- **Trạng thái:** ACTIVE
- **Nguồn:** bien-do-giao-dong-gia-co-phieu-la-gi
- **Phản hồi từ User:** "phần list thì dùng : thay vì . nhé. Ví dụ Biên độ đối với Chứng quyền (CW). phải là Biên độ đối với Chứng quyền (CW):"
- **Bản năng:** Khi trình bày các nhãn in đậm ở đầu các mục danh sách (bullet points/ordered lists), bắt buộc sử dụng dấu hai chấm `:` thay vì dấu chấm `.` làm ký tự phân tách giữa nhãn in đậm và nội dung câu tiếp theo (Ví dụ: `* **Nhãn**: Nội dung`).
- **Phạm vi:** Global

---

### Sử dụng dấu chấm ở cuối câu dẫn dắt danh sách liền kề
- **Trạng thái:** ACTIVE
- **Nguồn:** phan-tich-nganh-la-gi
- **Phản hồi từ User:** QA script cảnh báo lỗi câu dài do gộp câu dẫn dắt danh sách với mục list-item đầu tiên khi dùng dấu hai chấm.
- **Bản năng:** Khi viết câu dẫn dắt vào danh sách (bullet points/ordered lists) nằm liền kề (không có dòng trống phân cách), hãy kết thúc câu dẫn dắt bằng dấu chấm `.` thay vì dấu hai chấm `:` để script QA nhận diện và phân tách câu giới thiệu với mục đầu tiên của danh sách, tránh lỗi đếm gộp câu dài quá giới hạn.
- **Phạm vi:** Global

---

### Bảng so sánh đa chiều các loại giá trị cổ phiếu
- **Trạng thái:** ACTIVE
- **Nguồn:** thi-gia-co-phieu-la-gi
- **Phản hồi từ User:** "không" (Người dùng duyệt bản nháp tối ưu có bảng so sánh chi tiết và phân biệt rõ ràng các khái niệm)
- **Bản năng:** Đối với các bài viết giải thích khái niệm dễ gây nhầm lẫn (như Thị giá cổ phiếu - P2/F0), bắt buộc phải tích hợp một Bảng đối sánh đa chiều (Mệnh giá vs Giá trị sổ sách vs Thị giá) để triệt tiêu hoàn toàn sự mơ hồ. Hãy luôn duy trì 100% liên kết tuyệt đối khớp với sitemap live của DSC và đặt dấu hai chấm `:` ở cuối nhãn in đậm trong danh sách để tuân thủ định dạng.
- **Phạm vi:** Global

---

### Phân nhóm H2 cho bài viết từ điển/glossary và Đặt dấu câu ngoài thẻ bold
- **Trạng thái:** ACTIVE
- **Nguồn:** cac-thuat-ngu-trong-chung-khoan
- **Phản hồi từ User:** "ko" (Người dùng duyệt bản nháp tối ưu đã phân nhóm chuyên đề H2 và chỉnh sửa dấu câu FAQ ngoài bold tag để pass QA)
- **Bản năng:** Đối với các bài viết glossary dạng tổng hợp thuật ngữ, bắt buộc phải chia nhỏ danh sách phẳng thành 5 nhóm chuyên đề H2 rõ ràng để tăng scannability. Các câu hỏi FAQ hoặc list-item in đậm kết thúc bằng dấu chấm hỏi `?` hoặc dấu chấm `.` phải đặt dấu câu đó ra ngoài thẻ bold `**` (ví dụ: `**Câu hỏi**?`) để script QA tách câu chính xác và không đếm gộp nhãn in đậm vào câu trả lời gây lỗi câu quá dài (>30 từ).
- **Phạm vi:** Global

---

### Bảng phân nhóm LLR và Loại bỏ LaTeX
- **Trạng thái:** ACTIVE
- **Nguồn:** ty-le-bao-phu-no-xau
- **Phản hồi từ User:** "ko" (Người dùng duyệt bản nháp đã tối ưu hóa bảng phân nhóm LLR, loại bỏ LaTeX, cập nhật số liệu 2026 và tích hợp product bridge)
- **Bản năng:** Đối với các bài viết về chỉ số tài chính chuyên sâu (như Tỷ lệ bao phủ nợ xấu - LLR), bắt buộc phải có Bảng phân nhóm trực quan các ngưỡng an toàn của chỉ số và ý nghĩa đầu tư thực tế cho từng nhóm. Không sử dụng ký tự LaTeX (như $ hoặc $$) cho công thức tính toán mà hãy sử dụng định dạng chữ in đậm thông thường để tránh lỗi hiển thị trên CMS. Tích hợp phân tích liên kết chỉ số LLR với các chỉ số chất lượng tài sản khác như NPL, CASA, ROA để tăng độ sâu phân tích.
- **Phạm vi:** Global

---

### Bản chất NAV và Đính chính Thuật ngữ Lãi suất CCQ
- **Trạng thái:** ACTIVE
- **Nguồn:** lai-suat-chung-chi-quy
- **Phản hồi từ User:** "ko"
- **Bản năng:** Đối với các bài viết về chứng chỉ quỹ nhắm đến tệp Người tiết kiệm thận trọng (P1), phải chủ động đính chính thuật ngữ "lãi suất" (vốn là cách gọi quen thuộc nhưng không đúng bản chất của chứng chỉ quỹ) và chuyển đổi sang hiệu suất sinh lời hoặc sự tăng trưởng giá trị tài sản ròng (NAV) để đảm bảo tính chính xác và uy tín chuyên môn. Luôn cung cấp bảng so sánh trực quan giữa CCQ và gửi tiết kiệm ngân hàng, kết hợp bảng mô phỏng lãi kép định kỳ (ví dụ: tích lũy định kỳ 2 triệu đồng/tháng sau 1, 3, 5, 10 năm) để thuyết phục người đọc phân bổ dòng tiền gửi tiết kiệm sang chứng chỉ quỹ hoặc tài khoản chứng khoán DSC.
- **Phạm vi:** Global

---

### Định dạng số thập phân bằng dấu phẩy và Hướng dẫn thực hành cho Active Trader (P3)
- **Trạng thái:** ACTIVE
- **Nguồn:** backtest-la-gi
- **Phản hồi từ User:** "không"
- **Bản năng:**
  1. **Định dạng số thập phân tiếng Việt:** Bắt buộc sử dụng dấu phẩy `,` thay vì dấu chấm `.` cho số thập phân khi viết bài tiếng Việt (ví dụ: `T+1,5` thay vì `T+1.5`, phí `0,1%` thay vì `0.1%`, margin `13,5%` thay vì `13.5%`). Điều này vừa giúp tuân thủ chính xác quy tắc chính tả tiếng Việt của brand, vừa tránh lỗi QA script nhận diện nhầm dấu chấm thập phân là dấu chấm hết câu gây tách câu sai lệch.
  2. **Tăng tính thực chiến P3:** Đối với các bài phân tích kỹ thuật và chiến lược trading nhắm đến Active Trader (P3), luôn cung cấp hướng dẫn thực hành từng bước chi tiết (ví dụ: các bước sử dụng Bar Replay trên TradingView, code mẫu Pine Script v5) và phân tích sâu các sai lầm/bẫy tâm lý giao dịch (Overfitting, Survivorship Bias) để tối ưu E-E-A-T.
- **Phạm vi:** Global

---

### Tiết giảm mốc thời gian động và bổ sung quy định NFC/CCCD
- **Trạng thái:** ACTIVE
- **Nguồn:** cach-mo-tai-khoan-chung-khoan
- **Phản hồi từ User:** "ko phải phần nào cũng viết "Tính đến tháng 8/2026,", ngoài ra có thêm fact, thông tin báo chí gì mới liên quan có thể cho vào bài viết ko?"
- **Bản năng:**
  1. Tránh lạm dụng mốc thời gian động (ví dụ: "Tính đến tháng 8/2026,") ở đầu mọi tiêu đề H2 hoặc phần quy định pháp luật chung. Chỉ dùng mốc thời gian động ở những câu thực sự chứa số liệu/thống kê biến động (như biểu phí, số lượng tài khoản, lãi suất). Đa dạng hóa cách viết tự nhiên (ví dụ: "Theo quy chế hiện hành...", "Thống kê nội bộ tháng 8/2026 cho thấy...", "Theo thông tin dịch vụ cập nhật tháng 8/2026...").
  2. Cập nhật các dữ liệu thực tế và quy chế mới nhất của cơ quan quản lý (như quy định bắt buộc của UBCKNN về quét NFC trên thẻ CCCD gắn chip để đồng bộ thông tin với Cơ sở dữ liệu quốc gia về dân cư) làm luận cứ tăng tính E-E-A-T và thời sự cho bài viết hướng dẫn mở tài khoản.
- **Phạm vi:** Global

### Phân tích chỉ số tài chính theo ngành và xử lý lỗi ngoặc kép "Số cuối kỳ"
- **Trạng thái:** ACTIVE
- **Nguồn:** dar-la-gi
- **Phản hồi từ User:** "không"
- **Bản năng:** Khi phân tích các chỉ số cơ cấu tài chính (như DAR), luôn đính kèm so sánh định lượng đặc thù từng nhóm ngành cụ thể (như Ngân hàng 88%-92%, Bất động sản 55%-75%, Công nghệ 20%-35%). Tránh dùng dấu ngoặc kép bọc quanh tên các chỉ mục báo cáo tài chính (ví dụ: dùng "cột Số cuối kỳ" thay vì "cột 'Số cuối kỳ'") để tránh trigger lỗi emphatic quotes của QA script.
- **Phạm vi:** Global

### Không sử dụng đường kẻ ngang giữa các phần/heading
- **Trạng thái:** ACTIVE
- **Nguồn:** take-profit-la-gi
- **Phản hồi từ User:** "bỏ "---" giữa các heading"
- **Bản năng:** Tuyệt đối không sử dụng ký tự đường kẻ ngang (`---`) ở giữa các heading hoặc giữa các phần trong nội dung bài viết (trừ phần YAML front matter ở đầu trang nếu có). Giữa các phần chỉ dùng đúng một dòng trống để phân cách.
- **Phạm vi:** Global

---

### Phân tách câu hỏi và câu trả lời trong mục FAQs
- **Trạng thái:** ACTIVE
- **Nguồn:** ty-le-ky-quy
- **Phản hồi từ User:** Lỗi gộp câu tại mục FAQs do script QA đếm gộp câu hỏi và câu trả lời thành câu dài.
- **Bản năng:** Phân tách câu hỏi và câu trả lời trong mục FAQs bằng dòng trống để script QA không đếm gộp thành câu dài.
- **Phạm vi:** Global




