import os
import re
from typing import Set

from openai import OpenAI
from dotenv import load_dotenv

htmls_path = './data/htmls'
train_path = './data/train'
stopwords_path = 'data/stopwords/stopwords.txt'

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_API_BASE_URL', 'https://api.openai.com/v1')
)


def get_stopwords() -> Set[str]:
    words = set()
    with open(stopwords_path, 'r') as f:
        for line in f.readlines():
            words.add(str(line.replace('\n', '').replace(' ', '')))
        return words


def is_rain(content: str) -> bool:
    try:
        response = client.chat.completions.create(
            model='gpt-3.5-turbo-0125',
            messages=[
                {"role": "user",
                 "content": "This is the text content of the web page, please tell if the content contains a storm water flooding event, reply true or false"},
                {"role": "user", "content": content}
            ],
        )
        res = response.choices[0].message.content.lower().strip('.')
        print(res, content)
        if 'true' in res:
            return True
        elif 'false' in res:
            return False
        raise Exception('chatgpt reply format is incorrect.')
    except Exception as e:
        print('chatgpt error:', e)


def mkdir(p):
    if not os.path.exists(p):
        os.makedirs(p)


def main():
    stopwords = get_stopwords()
    labels = ['positive', 'negative']
    mkdir(f'{train_path}/{labels[0]}')
    mkdir(f'{train_path}/{labels[1]}')
    for group in os.listdir(htmls_path):
        for city in os.listdir(f'{htmls_path}/{group}'):
            for file in os.listdir(f'{htmls_path}/{group}/{city}'):
                path = f'{htmls_path}/{group}/{city}/{file}'
                try:
                    with open(path, 'rb') as fp:
                        content = fp.read().decode("utf8", "ignore")
                        content = content.replace(' ', '')
                        pattern = re.compile("[^\u4e00-\u9fa5]")
                        content = re.sub(pattern, '', content)
                        # 分了节省成本，截断较长的内容
                        if len(content) > 3000: content = content[:3000]
                except Exception as e:
                    print(f'the file {path} does not exits', e)
                else:
                    print(path, end=' ')
                    label = labels[0] if is_rain(content) else labels[1]
                    with open(f'{train_path}/{label}/{group}-{city}-{file.replace(".html", ".txt")}', 'w') as f:
                        f.write(content)


if __name__ == '__main__':
    main()
