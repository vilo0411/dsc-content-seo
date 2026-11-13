# Nguồn chính thống được phép link ra ngoài

`scripts/qa_lint.py` đọc file này: link ngoài tới domain dưới đây được tính là nguồn gốc (`SRC-missing`), link tới domain khác bị báo `SRC-host`. Thêm domain = thêm 1 dòng `- domain — ghi chú`.

Quy tắc dùng:
- Link đặt ngay tại câu trích số liệu / điều khoản, anchor là tên văn bản hoặc tên báo cáo (không phải "tại đây").
- Trích văn bản pháp luật → link tới văn bản trên cổng chính phủ / cơ quan ban hành, ghi số hiệu + ngày.
- Số của một doanh nghiệp / quỹ → link trang công bố thông tin của chính doanh nghiệp / công ty quản lý quỹ đó (thêm domain vào mục cuối).
- Không link sang công ty chứng khoán khác, sàn/app đối thủ, trang tổng hợp lại tin.

## Cơ quan quản lý
- ssc.gov.vn — Ủy ban Chứng khoán Nhà nước
- sbv.gov.vn — Ngân hàng Nhà nước
- mof.gov.vn — Bộ Tài chính
- gdt.gov.vn — Tổng cục Thuế
- div.gov.vn — Bảo hiểm tiền gửi Việt Nam

## Sở giao dịch, lưu ký
- hsx.vn — HOSE
- hnx.vn — HNX
- vnx.vn — Sở Giao dịch Chứng khoán Việt Nam
- vsd.vn — VSDC (Tổng công ty Lưu ký và Bù trừ)
- vsdc.vn — VSDC

## Văn bản pháp luật
- vanban.chinhphu.vn — Cổng văn bản Chính phủ
- chinhphu.vn — Cổng thông tin Chính phủ
- vbpl.vn — CSDL quốc gia về văn bản pháp luật
- quochoi.vn — Quốc hội

## Thống kê, tổ chức quốc tế
- gso.gov.vn — Tổng cục Thống kê
- nso.gov.vn — Cục Thống kê
- worldbank.org — World Bank
- imf.org — IMF
- federalreserve.gov — Fed

## Công bố của doanh nghiệp / công ty quản lý quỹ (chỉ khi trích số của chính họ)
- dragoncapital.com.vn — Dragon Capital
- vinacapital.com — VinaCapital
- ssiam.com.vn — SSIAM
- vcbf.com — VCBF
- hoaphat.com.vn — Hòa Phát (HPG), BCTC trên file.hoaphat.com.vn
- vinamilk.com.vn — Vinamilk (VNM)
- fpt.com — FPT
