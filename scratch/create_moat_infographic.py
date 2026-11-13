from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import textwrap
root=Path(__file__).resolve().parents[1]
out=root/'knowledge/operations/syndication/assets';out.mkdir(exist_ok=True)
font='C:/Windows/Fonts/arial.ttf'; bold='C:/Windows/Fonts/arialbd.ttf'
im=Image.new('RGB',(1000,1500),'#E8F8F2');d=ImageDraw.Draw(im)
def text(x,y,t,size=28,color='#0D1B2A',strong=False):
    d.text((x,y),t,font=ImageFont.truetype(bold if strong else font,size),fill=color)
logo=Image.open(root/'knowledge/1-brand/assets/logos/logo-for-light-bg.png').convert('RGBA');logo.thumbnail((200,85));im.paste(logo,(40,40),logo)
text(55,150,'CON HÀO KINH TẾ',54,strong=True)
text(55,225,'5 nguồn lợi thế cạnh tranh',40,strong=True)
text(55,290,'Khung đọc doanh nghiệp cùng Chứng khoán DSC',27)
items=[('Tài sản vô hình','Thương hiệu, bằng sáng chế, giấy phép.'),('Chi phí chuyển đổi','Thay nhà cung cấp gây tốn kém hoặc gián đoạn.'),('Hiệu ứng mạng','Thêm người dùng có thể tăng giá trị mạng lưới.'),('Lợi thế chi phí','Cấu trúc chi phí giúp cạnh tranh bền hơn.'),('Quy mô hiệu quả','Thị trường ngách chỉ đủ cho ít đơn vị hiệu quả.')]
for i,(title,desc) in enumerate(items):
    y=365+i*175
    d.rounded_rectangle((45,y,955,y+148),radius=20,fill='white')
    d.ellipse((65,y+30,135,y+100),fill='#00AD14');text(87,y+40,str(i+1),38,'white',True)
    text(160,y+25,title,34,strong=True)
    for j,line in enumerate(textwrap.wrap(desc,46)): text(160,y+76+j*32,line,27)
text(55,1280,'Một dấu hiệu chưa đủ để kết luận có lợi thế bền vững.',27,strong=True)
text(55,1330,'Đọc bài đầy đủ tại dsc.com.vn',30,'#007E15',True)
text(55,1395,'Nội dung giáo dục • Không phải khuyến nghị mua bán',24)
im.save(out/'con-hao-kinh-te-pinterest-v1.png')
print(str(out/'con-hao-kinh-te-pinterest-v1.png'))
