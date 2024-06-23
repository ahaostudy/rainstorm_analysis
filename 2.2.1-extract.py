import json
import os
from typing import List

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

htmls_path = './data/htmls'
train_path = './data/train'
stopwords_path = 'data/stopwords/stopwords.txt'
filter_path = './data/filter/filter.json'

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_API_BASE_URL', 'https://api.openai.com/v1')
)


def mkdir(p):
    if not os.path.exists(p):
        os.makedirs(p)


def get_positive() -> List[str]:
    res = list()
    with open(filter_path, 'r') as f:
        json_data = f.read()
        data = json.loads(json_data)
        for item in data:
            if item.get('label') == 'positive':
                res.append(item.get('path'))
    return res


def extract_rain_info(content: str):
    prompt = """
    从下列的网页文本数据中提取暴雨内涝的信息，并返回以下 JSON 格式的内容（每个事件的前两个字段为必须，如果不存在则忽略该事件）：
    {
      "暴雨内涝事件列表": [
        {
          "暴雨内涝开始时间": "",  // 记录暴雨内涝事件的开始时间, string (格式: YYYY-MM-DD HH:MM:SS)
          "暴雨内涝城市": "",  // 记录事件发生的城市名称, string
          "降雨量": 0,  // 记录降雨量, number (单位: mm)
          "降雨强度": 0,  // 记录降雨强度, number (单位: mm/h)
          "降雨历时": 0,  // 记录降雨持续时间, number (单位: 小时)
          "内涝严重程度": "",  // 记录内涝的严重程度, string
          "积水深度": 0,  // 记录积水深度, number (单位: cm)
          "积水点位置": "",  // 记录积水点的具体位置, string
          "淹没范围": "",  // 记录淹没的范围, string
          "内涝持续时间": 0,  // 记录内涝的持续时间, number (单位: 小时)
          "人员伤亡": 0,  // 记录人员伤亡情况, number (单位: 人)
          "受困人员": 0,  // 记录受困人员数量, number (单位: 人)
          "受灾人员": 0,  // 记录受灾人员数量, number (单位: 人)
          "车辆损失": 0,  // 记录车辆损失情况, number (单位: 辆)
          "房屋损失": 0,  // 记录房屋损失情况, number (单位: 间)
          "直接经济损失": 0,  // 记录直接经济损失金额, number (单位: 元)
          "交通影响": "",  // 记录交通影响情况（道路、地铁、列车、机场等）, string
          "电力等基础设施影响": ""  // 记录对电力等基础设施的影响, string
        }
      ]  
    }
    """
    response = client.chat.completions.create(
        messages=[
            {'role': 'user', 'content': prompt},
            {'role': 'user', 'content': content}
        ],
        model='gpt-3.5-turbo-0125',
        response_format={'type': 'json_object'}
    )
    res = response.choices[0].message.content
    return json.loads(res).get('暴雨内涝事件列表', [])


class Cache:
    cache = None

    def __init__(self, path):
        self.path = path

    def set(self, k, v):
        data = self._read()
        data[k] = v
        self._write(data)

    def get(self, k, default=None):
        return self._read().get(k, default)

    def _write(self, data: dict):
        s = json.dumps(data, ensure_ascii=False)
        self._cache().write(s)

    def _read(self) -> dict:
        data = self._cache().read()
        return json.loads(data)

    def _cache(self):
        if self.cache is None:
            dirname = os.path.dirname(self.path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            self.cache = open(self.path, 'w+')
            self.cache.write('{}')
        self.cache.seek(0)
        return self.cache

    def close(self):
        if self.cache is not None:
            self.cache.close()


def main():
    htmls = get_positive()
    cache = Cache('./data/cache/cache.json')
    success = cache.get('success', [])
    for path in htmls:
        if '长三角城市' not in path:
            continue
        if path in success:
            continue
        try:
            print('path:', path)
            with open(path, 'rb') as fp:
                content = fp.read().decode("utf8", "ignore")
                soup = BeautifulSoup(content, 'html.parser')
                for tag in soup(['style', 'script']):
                    tag.decompose()
                content = soup.get_text()
                content = content.replace(' ', '').replace('\n', ' ').replace('\r', ' ')
                if len(content) > 12000: content = content[:12000]
                events = extract_rain_info(content)
                dirname = os.path.dirname(path).replace('htmls', 'event')
                mkdir(dirname)
                data_path = os.path.join(dirname, 'data.json')
                with open(data_path, 'r+' if os.path.exists(data_path) else 'w+') as f:
                    data_str = f.read()
                    if len(data_str) == 0:
                        data_str = '{"event": []}'
                    data = json.loads(data_str)
                    data['event'].extend(events)
                    f.seek(0)
                    f.write(json.dumps(data, ensure_ascii=False))
        except Exception as e:
            print(f'the file {path} extract error:', e)
        else:
            print('content:', content)
            print('events:', events)
            print()
            success.append(path)
            cache.set('success', success)
    cache.close()


if __name__ == '__main__':
    main()
