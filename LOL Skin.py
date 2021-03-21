import requests
from fake_useragent import UserAgent
from urllib import request, error
import re
import time
import os


def get_html(url):
    """
    传入要爬取的URL
    设置代理
    返回HTML
    """
    headers = {"User-Agent": UserAgent().random}
    resp = requests.get(url, headers=headers)
    time.sleep(1.5)
    if resp.status_code == 200:
        resp.encoding = "unicode_escape"
        return resp.text
    else:
        return None


def get_hero(html):
    """
    传入HTML
    获取英雄的属性：编号，昵称，英文名，中文名
    返回英雄属性列表：如 [('1',"黑暗之女","Annie","安妮"), ...]
    """
    hero_list = re.findall(
        r'"heroId":"(.*?)","name":"(.*?)","alias":"(.*?)","title":"(.*?)"', html)
    return hero_list



def save_file(file_path, skin_name, data):
    """
    保存为以皮肤名称为文件名称的.jpg文件
    """
    # 拼接得到皮肤文件名
    file_name = os.path.join(file_path, skin_name + ".jpg")
    # 将皮肤数据以二进制方式写入文件中
    with open(file_name, "wb") as f:
        f.write(data)


def main():
    # 要存放皮肤图片的文件夹路径
    path = r"D:/Picture/lol/"
    # 英雄列表的URL
    url = r"https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js"
    # 得到英雄列表的HTML
    html = get_html(url)
    # 在HTML中获取数据为英雄属性列表
    hero_list = get_hero(html)

    # 遍历英雄属性列表
    for hero in hero_list:
        # 构造每个英雄的文件夹,用英雄编号和昵称
        file_path = r"{}{}.{}".format(path, hero[0], hero[2])
        # ddragon这个网站图片会更清晰更好些，但是未找到SkinId，所以用range一个一个找
        # 根据玩lol的经验，大多数英雄皮肤不超过30个
        skin_list = [str(i) for i in range(0, 31)]

        # 在皮肤不超过30个的情况下
        for skin in skin_list:
            # 编辑图片名字
            file_name = "{}/{}{}.jpg".format(file_path, hero[0], skin)
            # 构造每个皮肤的URL
            skin_url = r"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{}_{}.jpg".format(hero[2],skin)

            # 异常处理
            try:
                # 获取皮肤URL返回response
                response = request.urlopen(skin_url)
                # 读取response
                data = response.read()
                # 关闭response
                response.close()
            except error.HTTPError as e:
                # 返回状态码和出错原因
                print("{}:{}".format(e.code, e.reason))
                continue

            # 每获得一个皮肤属性等待0.5秒
            time.sleep(0.5)


            if os.path.exists(file_path):  # 判断当前英雄的文件夹是否存在
                if os.path.exists(file_name):  # 判断当前英雄的当前皮肤文件是否存在
                    print("Exist!  "+hero[2]+"————"+skin)
                    continue  # 以上都存在，终止此次循环，进入下一次循环
                else:  # 如果当前英雄的当前皮肤文件不存在
                    save_file(file_path, (hero[2]+skin), data)  # 调用save_file下载
                    print("Downloaded！  "+hero[2]+"————"+skin)
            else:  # 如果当前英雄的文件夹不存在
                # 创建当前英雄的文件夹
                os.mkdir(path + "{}.{}".format(hero[0], hero[2]))
                # 调用save_file下载
                save_file(file_path, (hero[2]+skin), data)
                print("Downloaded！  "+hero[2]+"————"+skin)

        time.sleep(0.5)


if __name__ == "__main__":
    main()