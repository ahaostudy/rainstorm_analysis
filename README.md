# Rainstorm Analysis

基于大数据的暴雨内涝事件分析。

## Tasks

项目分为 5 个任务，分别为：

1. 网页数据收集：使用爬虫技术从 Web 搜索引擎中搜索出需要的暴雨内涝时间网页
2. 数据结构化处理：针对每个网页文件，尽可能地从文件中提取暴雨内涝相关信息
3. 数据智能分析：对结构化的数据进行数据分析统计（如分析各城市每月的暴雨事件数量）
4. 暴雨内涝灾害指数评价：计算城市群和各个城市的灾害指数
5. 数据可视化：通过 Web 网页图标的形式展示分析后的数据

## Run

项目中接入了 GhatGPT 来辅助分析数据，所以**需要设置以下环境变量**：

```env
OPENAI_API_KEY=sk-xxx  # OpenAI 的 ApiKey，此项为必须，没有默认值
OPENAI_API_BASE_URL=https://api.openai.com/v1  # 默认为 OpenAI 官网地址
```

依次运行前 4 个任务对应的 Python 源代码，并记录中间的结果数据。

在启动最后的可视化网页之前，需要将前面运行时的**中间数据手动搬到 `./charts/public/data/json/` 下的 JSON 文件中**，然后运行下面的指令启动：

```shell
npm install
npm run serve
```

启动后访问 http://localhost:8080 即可查看最终效果。

## Preview

![Preview](./image/preview.png)
