# pip install pillow

from PIL import Image, ImageDraw, ImageFont
import string
import random
from io import BytesIO
# 随机颜色
def random_color():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

str_all = string.digits + string.ascii_letters

# 随机验证码
def random_code(size=(184,44), length=4, point_num=80, line_num=10):
    width,  height = size

    # 生成一个200X40的白色背景图片
    img = Image.new('RGB' ,(width, height), color=(255, 255, 255))

    # 新建一个和图片同大小的画布
    darw = ImageDraw.Draw(img)

    # 生成对象
    font = ImageFont.truetype(font='static/my/font/MexicanTequila.ttf', size=35)

    # 书写验证码
    valid_code = ''
    for i in range(length):
        random_char = random.choice(str_all)
        darw.text((40*i+30, 10), random_char, (0, 0, 0), font=font)
        valid_code += random_char
    print(valid_code)

    # 随机生成点
    for i in range(point_num):
        x, y = random.randint(0, width), random.randint(0, height)
        darw.point((x, y), random_color())

    # 随机生成线
    for i in range(line_num):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        darw.line((x1, y1, x2, y2), fill=random_color())

    # 创建一个内存句柄
    f = BytesIO()
    # 将图片保存到内存句柄中
    img.save(f, 'PNG')
    # 读取内存句柄
    data = f.getvalue()
    return (data, valid_code)

    img.save('new_img.png', 'PNG')

if __name__ == '__main__':
    random_code()