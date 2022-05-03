<template>
  <div class="main">
    <div>
      <div class="title">2022新冠实时疫情图</div>
      <div class="tab">
        <button @click="showcn()" id="btn-cn" class="button btn-active">
          中国
        </button>
        <button @click="showworld()" id="btn-world" class="button">全球</button>
      </div>
      <div class="info" id="cninfo">
        <div>
          <p>现存确诊</p>
          <p style="color: rgb(247, 76, 49)">
            {{ chinaData.currentConfirmedCount }}
          </p>
        </div>
        <div>
          <p>累计确诊</p>
          <p style="color: rgb(247, 130, 7)">{{ chinaData.confirmedCount }}</p>
        </div>
        <div>
          <p>死亡</p>
          <p style="color: rgb(93, 112, 146)">{{ chinaData.deadCount }}</p>
        </div>
        <div>
          <p>治愈</p>
          <p style="color: rgb(40, 183, 163)">{{ chinaData.curedCount }}</p>
        </div>
      </div>

      <div class="info" id="worldinfo" style="display: none">
        <div>
          <p>现存确诊</p>
          <p style="color: rgb(247, 76, 49)">
            {{ worldData.currentConfirmedCount }}
          </p>
        </div>
        <div>
          <p>累计确诊</p>
          <p style="color: rgb(247, 130, 7)">{{ worldData.confirmedCount }}</p>
        </div>
        <div>
          <p>死亡</p>
          <p style="color: rgb(93, 112, 146)">{{ worldData.deadCount }}</p>
        </div>
        <div>
          <p>治愈</p>
          <p style="color: rgb(40, 183, 163)">{{ worldData.curedCount }}</p>
        </div>
      </div>
    </div>
    <div id="cnmap" class="map"></div>
    <div id="worldmap" class="map"></div>
    <div class="copyright">
      <a target="_blank" href="https://idealclover.top"
        >调用地图</a
      >
    </div>
  </div>
</template>

<script>
import echarts from "echarts";
import china from "echarts/map/json/china.json";
echarts.registerMap("china", china);
import world from "echarts/map/json/world.json";
echarts.registerMap("world", world);
import axios from "axios";

export default {
  props: {},
  data() {
    return {
      chinaData: {
        currentConfirmedCount: 0,
        confirmedCount: 0,
        deadCount: 0,
        curedCount: 0,
      },
      worldData: {
        currentConfirmedCount: 0,
        confirmedCount: 0,
        deadCount: 0,
        curedCount: 0,
      },

      chinaDetailData: [],
      worldDetailData: [],
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    loadMap() {
      var dom = document.getElementById("cnmap");
      var myChart = echarts.init(dom, null, { renderer: "svg" });
      const cnoption = {
        bottom: "10px",
        tooltip: {
          show: true,
          trigger: "item",
        },
        dataRange: {
          x: "center",
          orient: "horizontal",
          min: 0,
          max: 20000,
          text: ["高", "低"], // 文本，默认为数值文本
          splitNumber: 0,
          splitList: [
            { start: 1000, end: 999999 },
            { start: 100, end: 999 },
            { start: 50, end: 99 },
            { start: 10, end: 49 },
            { start: 1, end: 9 },
            { start: 0, end: 0 },
          ],
          inRange: {
            color: [
              "#fff",
              "#fff5c9",
              "#FDEBCF",
              "#F59E83",
              "#F59E83",
              "#CB2A2F",
              "#e6ac53",
              "#70161D",
            ],
          },
        },
        series: [
          {
            label: {
              normal: {
                fontFamily: "Microsoft YaHei",
                fontSize: 9,
                show: true,
              },
              emphasis: {
                show: false,
              },
            },
            name: "现存确诊",
            type: "map",
            mapType: "china",
            zoom: 1,
            itemStyle: {
              normal: {
                borderWidth: 0.5, //区域边框宽度
                borderColor: "#B6B6B6", //区域边框颜色
                areaColor: "#ffefd5", //区域颜色
              },
            },
            data: this.chinaDetailData,
          },
        ],
        animation: false,
      };
      myChart.setOption(cnoption, true);

      var worldmapdom = document.getElementById("worldmap");
      var worldChart = echarts.init(worldmapdom, null, { renderer: "svg" });
      const worldoption = {
        bottom: "10px",
        tooltip: {
          show: true,
          trigger: "item",
          formatter: function (val) {
            console.log(val);
            if (typeof val.data === "undefined")
              val.data = { provinceName: val.name, value: "未知" };
            return (
              val.data.provinceName + "<br>" + "现存确诊: " + val.data.value
            );
          },
        },
        dataRange: {
          x: "center",
          orient: "horizontal",
          min: 0,
          max: 9999999,
          text: ["高", "低"], // 文本，默认为数值文本
          splitNumber: 0,
          splitList: [
            { start: 1000000, end: 999999999 },
            { start: 100000, end: 999999 },
            { start: 10000, end: 99999 },
            { start: 1000, end: 9999 },
            { start: 100, end: 999 },
            { start: 0, end: 99 },
          ],
          inRange: {
            color: [
              "#FAEBD2",
              "#D56355",
              "#BB3937",
              "#cb2a2f",
              "#772526",
              "#5e0a0b",
            ],
          },
        },
        series: [
          {
            label: {
              normal: {
                fontFamily: "Microsoft YaHei",
                fontSize: 9,
                show: false,
              },
              emphasis: {
                show: false,
              },
            },
            name: "现存确诊",
            type: "map",
            mapType: "world",
            zoom: 0.8,
            itemStyle: {
              normal: { label: { show: true, color: "#333" }, borderWidth: 0 },
            },
            data: this.worldDetailData,
          },
        ],
        animation: false,
      };
      worldChart.setOption(worldoption, true);
      worldChart.resize();

      let worldmap = document.getElementById("worldmap");
      let cnmap = document.getElementById("cnmap");
      let cninfo = document.getElementById("cninfo");
      let worldinfo = document.getElementById("worldinfo");
      // let btncn = document.getElementById("btn-cn");
      // let btnworld = document.getElementById("btn-world");

      cnmap.style.display = "block";
      worldmap.style.display = "none";
      cninfo.style.display = "flex";
      worldinfo.style.display = "none";
      // btncn.className = "button";
      // btnworld.className = "button btn-active";
    },
    loadData() {
      axios.get("https://idealclover.cn/covidinfo.json").then((response) => {
        let data = response.data;
        this.chinaData = data["china"];
        this.worldData = data["world"];
        this.chinaDetailData = data["chinaDetail"];
        this.worldDetailData = data["worldDetail"];
        this.loadMap();
      });
    },
    showcn() {
      let worldmap = document.getElementById("worldmap");
      let cnmap = document.getElementById("cnmap");
      let cninfo = document.getElementById("cninfo");
      let worldinfo = document.getElementById("worldinfo");
      let btncn = document.getElementById("btn-cn");
      let btnworld = document.getElementById("btn-world");
      cnmap.style.display = "block";
      worldmap.style.display = "none";
      cninfo.style.display = "flex";
      worldinfo.style.display = "none";
      btncn.className = "button btn-active";
      btnworld.className = "button";
    },
    showworld() {
      let worldmap = document.getElementById("worldmap");
      let cnmap = document.getElementById("cnmap");
      let cninfo = document.getElementById("cninfo");
      let worldinfo = document.getElementById("worldinfo");
      let btncn = document.getElementById("btn-cn");
      let btnworld = document.getElementById("btn-world");
      worldmap.style.display = "block";
      cnmap.style.display = "none";
      cninfo.style.display = "none";
      worldinfo.style.display = "flex";
      btncn.className = "button";
      btnworld.className = "button btn-active";
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

#main {
  max-width: px;
  margin: auto;
}

.info {
  display: flex;
  justify-content: space-between;
  text-align: center;
  line-height: 0.5;
  border-bottom: 1px solid #ebebeb;
}

.info > div {
  flex-grow: 1;
  margin: 0 4px;
  border-radius: 3px;
}

.info > div > p:first-child {
  font-size: 12px;
}

.title {
  text-align: center;
}

.copyright {
  font-size: 10px;
  text-align: right;
  color: #909399;
}

.copyright a {
  text-decoration: none;
}

.copyright a:hover,
a:active,
a:visited,
a:link,
a:focus {
  color: #909399;
}

.map {
  position: relative;
  height: 380px;
}

#worldmap {
  height: 380px;
}

.copyright {
  position: relative;
  width: 100%;
}

.copyright,
.map {
  top: -65px;
}

.hide {
  display: none;
}

#worldmap {
  width: 100%;
}

.button {
  display: inline-block;
  margin-bottom: 0;
  font-weight: 400;
  text-align: center;
  vertical-align: middle;
  -ms-touch-action: manipulation;
  touch-action: manipulation;
  cursor: pointer;
  background-image: none;
  border: 1px solid transparent;
  white-space: nowrap;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  height: 28px;
  padding: 0 15px;
  font-size: 14px;
  border-radius: 4px;
  transition: color 0.2s linear, background-color 0.2s linear,
    border 0.2s linear, box-shadow 0.2s linear;
  color: #515a6e;
  background-color: #fff;
  border-color: #dcdee2;
}

.btn-active {
  color: #fff;
  background-color: #2d8cf0;
  border-color: #2d8cf0;
}

.tab {
  margin-top: 5px;
  text-align: center;
}
</style>
