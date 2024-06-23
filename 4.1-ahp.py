import numpy as np
import matplotlib.pyplot as plt
import json


# 计算对成矩阵中各个指标的权重
def weight(x):
    x1 = np.prod(x, axis=1) ** (1 / x.shape[0])
    s = x1.sum()
    res = x1 / s
    return res.reshape(x.shape[0], 1)


# 获取随机一致性指标
def get_ri(num):
    if num == 1 or num == 2:
        return 0
    elif num == 3:
        return 0.52
    elif num == 4:
        return 0.89
    elif num == 5:
        return 1.12


# 一致性检验
def check(x):
    n = x.shape[0]
    w = weight(x)
    aw = np.dot(x, w)
    lmd = (aw / w).sum() / n
    if n == 1 or n == 2:
        cr = 0
    else:
        ci = (lmd - n) / (n - 1)
        ri = get_ri(n)
        cr = ci / ri
    if cr > 0.1:
        print('check: 一致性检验未通过')
    else:
        print('check: 一致性检验通过')
    return cr


# 可视化
def draw(x, y):
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
    plt.figure(figsize=(8, 5))
    plt.barh(y, x)
    plt.title("暴雨内涝危害评价")
    plt.show()


def main():
    # 设置判断矩阵
    alist = ['死亡人数', '失踪人数', '受伤人数', '受灾人数', '转移人数', '直接经济损失', '间接经济损失', '城市交通影响',
             '地铁交通影响', '铁路交通影响', '航班影响']
    # '死亡人数', '失踪人数', '受伤人数'之间的相对重要性
    a = np.array([[1, 3, 8],
                  [1 / 3, 1, 3],
                  [1 / 8, 1 / 3, 1]])
    # '死亡人数', '失踪人数', '受伤人数', '受灾人数', '转移人数'之间的相对重要性
    b1 = np.array([[1, 3, 5, 8, 9],
                   [1 / 3, 1, 2, 4, 5],
                   [1 / 5, 1 / 2, 1, 2, 3],
                   [1 / 8, 1 / 4, 1 / 2, 1, 2],
                   [1 / 9, 1 / 5, 1 / 3, 1 / 2, 1]])
    # '直接经济损失', '间接经济损失'之间的相对重要性
    b2 = np.array([[1, 6],
                   [1 / 6, 1]])
    # '城市交通影响', '地铁交通影响', '铁路交通影响', '航班影响'之间的相对重要性
    b3 = np.array([[1, 3, 7, 7],
                   [1 / 3, 1, 3, 3],
                   [1 / 7, 1 / 3, 1, 1],
                   [1 / 7, 1 / 3, 1, 1]])

    # 计算各个指标权重并进行一致性校验
    aw, b1w, b2w, b3w = weight(a), weight(b1), weight(b2), weight(b3)
    print('a-weight:', aw.flatten())
    print('cr:', check(a))
    print('b1-weight:', b1w.flatten())
    print('cr:', check(b1))
    print('b2-weight:', b2w.flatten())
    print('cr:', check(b2))
    print('b3-weight:', b3w.flatten())
    print('cr:', check(b3))
    print()

    # 合并结果
    a1 = b1w * aw[0]
    a2 = b2w * aw[1]
    a3 = b3w * aw[2]
    res = list(a1.flatten()) + list(a2.flatten()) + list(a3.flatten())

    # 可视化
    draw(res, alist)

    # 生成最终的结果数据
    score_dic = {"data": []}
    for i in range(0, 11):
        score_dic['data'].append({'name': alist[i], 'value': res[i]})
    score = json.dumps(score_dic, ensure_ascii=False)
    print(score)


if __name__ == '__main__':
    main()
