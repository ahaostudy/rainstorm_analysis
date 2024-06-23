import os

import requests
from requests import Response
from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

htmls = './data/htmls'


def init_browser() -> webdriver.Chrome:
    # get直接返回，不再等待界面加载完成（避免网页一直加载出现超时，后面可配合WebDriverWait等待某个元素出现使用）
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"
    # 创建chrome参数对象
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    options.add_argument('window-size=1600x900')  # 指定浏览器分辨率
    options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    # 禁止图片和css加载
    prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(3)
    browser.set_script_timeout(3)  # 这两种设置都进行才有效
    return browser


def search_baidu_news(wd: str, page: int) -> Response:
    url = 'https://www.baidu.com/s'
    param = {
        'wd': wd,
        'pn': str(page),
        'tn': 'news'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62'
    }
    return requests.get(url=url, params=param, headers=headers)


def create_dirs(group, city):
    for i in range(3):
        g = group[i]
        cs = city[i]
        for c in cs:
            path = os.path.join(htmls, g, c)
            if not os.path.exists(path):
                os.makedirs(path)


def main():
    browser = init_browser()
    group = ['京津冀城市群城市', '粤港澳大湾区城市', '长三角城市群城市']
    city = [['北京', '天津', '石家庄', '唐山', '保定', '秦皇岛', '廊坊', '沧州', '承德', '张家口'],
            ['香港', '澳门', '广州', '深圳', '珠海', '佛山', '中山', '东莞', '肇庆', '江门', '惠州'],
            ['无锡', '常州', '苏州', '南通', '扬州', '镇江', '盐城', '泰州', '杭州', '宁波', '温州', '湖州', '嘉兴',
             '绍兴', '金华', '舟山', '台州', '合肥', '芜湖', '马鞍山', '铜陵', '安庆', '滁州', '池州', '宣城']]
    word = ' 暴雨 内涝'

    for x in range(len(group)):
        for y in range(len(city[x])):
            wd = city[x][y] + word
            list_kw = []
            for page in range(0, 39, 10):
                response = search_baidu_news(wd, page)
                page_text = response.text
                tree = etree.HTML(page_text)
                r = tree.xpath('//div[@id="content_left"]//h3/a/@href')
                list_kw.append(r)
            print(wd)
            print(list_kw[0][2])
            for i in range(len(list_kw)):
                for j in range(len(list_kw[i])):
                    href = list_kw[i][j]
                    filename = os.path.join(htmls, group[x], city[x][y], f'{i}{j}.html')
                    print(filename, end=' ')
                    if os.path.exists(filename):
                        print('exists')
                        continue
                    print('not exists')
                    try:
                        browser.get(href)
                        page_text = browser.page_source
                        dirName = os.path.dirname(filename)
                        if not os.path.exists(dirName):
                            os.makedirs(dirName)
                        with open(filename, 'w', encoding='utf-8') as fp:
                            fp.seek(0)
                            fp.truncate()
                            fp.write(page_text)
                    except Exception as err:
                        print(err)
                        print('timeout')
                        browser.execute_script('window.stop()')


if __name__ == '__main__':
    main()
