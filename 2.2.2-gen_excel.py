import json
import os

import pandas as pd

event_path = './data/event'
excel_path = './data/excel'


def main():
    if not os.path.exists(excel_path):
        os.makedirs(excel_path)
    for group in os.listdir(event_path):
        for city in os.listdir(os.path.join(event_path, group)):
            for file in os.listdir(os.path.join(event_path, group, city)):
                try:
                    data = {
                        "暴雨内涝开始时间": [],
                        "所在城市": [],
                        "降雨量": [],
                        "降雨强度": [],
                        "降雨历时": [],
                        "内涝严重程度": [],
                        "积水深度": [],
                        "积水点位置": [],
                        "淹没范围": [],
                        "内涝持续时间": [],
                        "人员伤亡": [],
                        "受困人员": [],
                        "受灾人员": [],
                        "车辆损失": [],
                        "房屋损失": [],
                        "直接经济损失": [],
                        "交通影响": [],
                        "电力等基础设施影响": []
                    }
                    with open(os.path.join(event_path, group, city, file)) as f:
                        events = json.loads(f.read()).get('event')
                        for event in events:
                            event['所在城市'] = city
                            for k in data:
                                data[k].append(event.get(k, None))
                    print(data)
                    df = pd.DataFrame(data)
                    df.to_excel(os.path.join(excel_path, f'{group}_{city}.xlsx'), index=False)
                except Exception as e:
                    print('export excel error:', e)


if __name__ == '__main__':
    main()
