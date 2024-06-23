<template>
  <div @dblclick="getChina" ref="mapRef" class="chart"></div>
</template>

<script setup>
import {ref, onMounted, defineEmits, reactive} from "vue"
import * as echarts from "echarts"
import {toPingyin} from "@/utils/map.js"

const mapRef = ref(null)
let chart = null
const emits = defineEmits(['getCityName'])

const baseOption = {
  title: {
    text: "三大城市群内涝事件",
    left: 20,
    top: 20,
    textStyle: {
      color: '#bdeaf5', // 设置标题字体颜色为白色
      fontSize: 16, // 设置标题字体大小为16
    }

  },
  geo: {
    type: "map",
    map: "china",
    top: "5%",
    bottom: "5%",
    //允许拖动及缩放
    roam: true,
    itemStyle: {
      // 地图的填充色
      areaColor: "rgba(158, 236, 255, 0.3)",
      borderColor: "#174690",
    },
  },
  visualMap: {
    min: 0,
    max: 25,
    calculable: true, //显示拖拽
    inRange: {
      color: ["#c7f4ff", "#07ceff", "#1f0099"], //颜色
    },
    textStyle: {
      color: "#a2e7f9",
    },
    text: ['内涝总次数']
  },
}

let dataSeries = []

async function getRainData() {
  const regionData = await fetch(`/data/map/region.json`).then(res => res.json())

  const cityRainData = await fetch(`/data/json/cityRain.json`).then(res => res.json())

  let rainData = []
  for (let cityRain of cityRainData.data) {
    console.log(cityRain.count)
    for (let cityRegion of regionData.data) {
      if (cityRegion.name.startsWith(cityRain.cityName)) {
        rainData.push({
          name: cityRain.cityName,
          value: [cityRegion.center.longitude, cityRegion.center.latitude, cityRain.count]
        })
        break
      }
    }
  }

  dataSeries = [
    {
      type: "effectScatter",
      data: rainData,
      coordinateSystem: "geo",
      label: {
        normal: {
          formatter: "{b}",
          position: "right",
          show: true,
          color: "#bdeaf5", // 设置字体颜色为浅蓝色
          borderColor: "transparent", // 设置边框颜色为透明（无边框）
        }

      },
    },
  ]
}

const changeMap = (chart) => {
  chart.on("click", async (e) => {
    const provinceMapData = await fetch(`/data/map/${toPingyin(e.name)}.json`).then((res) =>
        res.json()
    )
    echarts.registerMap(`${e.name}`, provinceMapData)
    //防止错位
    chart.setOption(baseOption, true)
    chart.setOption({series: dataSeries})
    chart.setOption({geo: {map: `${e.name}`}})
    //点击散点
    if (e.componentSubType === 'effectScatter') {
      emits('getCityName', e.name)
    }
  })
}
onMounted(async () => {
  await getRainData()
  const chinaMapData = await fetch("/data/map/china.json").then((res) =>
      res.json()
  )
  echarts.registerMap("china", chinaMapData)
  chart = echarts.init(mapRef.value)
  chart.setOption(baseOption)
  chart.setOption({series: dataSeries})
  window.addEventListener('resize', () => {
    chart.resize()
  })
  changeMap(chart)
})
//双击返回
const getChina = () => {
  chart.setOption({geo: {map: `china`}})
}
</script>

<style lang='less' scoped>
</style>
