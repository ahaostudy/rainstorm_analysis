import pandas as pd
import os
import matplotlib.pyplot as plt
import json

cities1 = ['北京', '天津', '石家庄', '唐山', '保定', '秦皇岛', '廊坊', '沧州', '承德', '张家口']
cities2 = ['香港', '澳门', '广州', '深圳', '珠海', '佛山', '中山', '东莞', '肇庆', '江门', '惠州']
cities3 = ['无锡', '常州', '苏州', '南通', '扬州', '镇江', '盐城', '泰州', '杭州', '宁波', '温州', '湖州', '嘉兴',
           '绍兴', '金华', '舟山', '台州', '合肥', '芜湖', '马鞍山', '铜陵', '安庆', '滁州', '池州', '宣城']
cities_name = ['京津冀城市群', '粤港澳城市群', '长三角城市群']


def rain_time(df):
    month_list = [0] * 12
    year_list = [0] * 13  # 2012-2024
    time_set = set()
    try:
        for item in df['暴雨内涝开始时间']:
            item = item.translate(str.maketrans({'-': '/', '.': '/'}))
            time_set.add(item.split(' ')[0])
        for time_set_item in time_set:
            if '/' in time_set_item:
                month = int(time_set_item.split('/')[1])
                month_list[month - 1] += 1
                year = int(time_set_item.split('/')[0])
                year_list[year - 2012] += 1
    except Exception as e:
        print('error:', e)
    return month_list, year_list


def rain_analysis(df):
    data = {"data": []}
    city_month_list = []
    city_year_list = []
    city_count_dic = {}
    df_year = [0] * 13  # 2012-2024
    for cities in [cities1, cities2, cities3]:
        df_month = [0] * 12
        year = [0] * 13
        for city in cities:
            df_item = df[df['所在城市'] == city]
            df_item_month, df_item_year = rain_time(df_item)
            dic = {"cityName": city, "month": df_item_month, "year": df_item_year, "count": sum(df_item_month)}
            data['data'].append(dic)
            for i in range(0, 12):
                df_month[i] += df_item_month[i]
            for i in range(0, 13):
                df_year[i] += df_item_year[i]
                year[i] += df_item_year[i]
            city_count_dic[city] = sum(df_item_month)

        city_month_list.append(df_month)
        city_year_list.append(year)
    print('city_rain.json:', json.dumps(data, ensure_ascii=False))
    return city_month_list, city_count_dic, df_year, city_year_list


def draw_cities(cities, month_list):
    month_label = [str(i) + '月' for i in range(1, 13)]
    x = month_label
    y = month_list
    plt.bar(x, y)
    for a, b, i in zip(x, y, range(len(x))):  # zip 函数
        plt.text(a, b + 0.01, "%.2f" % y[i], ha='center', fontsize=12)  # plt.text 函数
    plt.ylabel('次数')
    plt.title(cities + "--下雨统计")
    plt.show()


def draw_month(race_list):
    month_label = [str(i) + '月' for i in range(1, 13)]
    x = month_label
    y = [float(i.split('%')[0]) for i in race_list]
    plt.bar(x, y)
    for a, b, i in zip(x, y, range(len(x))):  # zip 函数
        plt.text(a, b + 0.01, "%.2f" % y[i], ha='center', fontsize=12)  # plt.text 函数
    plt.ylabel('次数')
    plt.title("暴雨内涝次数比例")
    plt.show()


def draw_city(city_list):
    x = [i for i, j in city_list]
    y = [j for i, j in city_list]
    plt.barh(x, y)
    plt.title("各个城市暴雨统计")
    plt.show()


def draw_year(year_list):
    x = [2012 + i for i in range(0, 13)]
    y = year_list
    plt.plot(x, y)
    for a, b, i in zip(x, y, range(len(x))):  # zip 函数
        plt.text(a, b + 0.01, y[i], ha='center', fontsize=12)  # plt.text 函数
    plt.title('2012年--2024年')
    plt.show()


def main():
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']  # 用来正常显示中文标签
    excels = './data/excel'
    df_list = []
    for excel in os.listdir(excels):
        excel_path = excels + '/' + excel
        df = pd.read_excel(excel_path)
        df_list.append(df)
    df = pd.concat([i for i in df_list])
    df['暴雨内涝开始时间'] = df['暴雨内涝开始时间'].astype(str)

    print('任务1：统计每个城市群（京津冀、粤港澳、长三角）的月度暴雨次数')
    months, cities, years, year = rain_analysis(df)
    cities_year_json = {}
    for i in range(0, 3):
        print(f'{cities_name[i]} month count: {months[i]}')
        print(f'{cities_name[i]} year count: {year[i]}')
        cities_year_json[cities_name[i]] = year[i]
        draw_cities(cities_name[i], months[i])
    print('year_line.json:', json.dumps(cities_year_json, ensure_ascii=False))

    print('\n任务2：统计所有城市的月度暴雨次数，并计算占比')
    month_count = [0] * 12
    for i in range(0, 12):
        month_count[i] = months[0][i] + months[1][i] + months[2][i]
    print(month_count)
    month_sum = sum(month_count)
    month_race = [str(round(item * 100 / month_sum, 2)) + '%' for item in month_count]
    print(month_race)
    draw_month(month_race)

    print('\n任务3：统计各个城市的暴雨次数，并按降序排序')
    city_count = sorted(cities.items(), key=lambda d: d[1], reverse=True)
    print(city_count)
    draw_city(city_count)

    print('\n任务4：统计从2012年至2024年每年的暴雨次数')
    print(years)
    draw_year(years)


if __name__ == '__main__':
    main()
