<template>
  <div ref="scorePieRef" class="chart"></div>
</template>

<script setup>
import {ref, onMounted} from 'vue'
import * as echarts from "echarts"

const scorePieRef = ref(null)
const baseOption = {
  title: {
    text: '暴雨内涝危害评价',
    
    textStyle: {
      color: '#bdeaf5', // 设置标题字体颜色为白色
      fontSize: 16, // 设置标题字体大小为16
    }
  },
  tooltip: {
    trigger: 'item',
    
  },
  series: [
    {
      name: 'Access From',
      type: 'pie',
      radius: ['40%', '70%'],
      label: {
        // 设置饼图中文字的样式
        formatter: '{b}',
        textStyle: {
          color: '#fff', // 设置文字颜色为白色
        },
        borderWidth: 0, // 设置边框宽度为0，即无边框
        // 可根据需要设置其他样式属性
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)',
          
        }
      }
    }
  ]
}
const dataset = {
  dimensions: ["name", "value"]
}
onMounted(async()=>{
  const chart = echarts.init(scorePieRef.value)
  const {data:res} = await fetch('/data/json/score.json').then(res=>res.json())
  chart.setOption(baseOption)
  dataset.source = res
  chart.setOption({dataset})
  window.addEventListener('resize',()=>{chart.resize()})
})
</script>

<style lang='less' scoped>

</style>
