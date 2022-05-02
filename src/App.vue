<template>
  <div>
    <div>
      <div class="title">2021新冠实时疫情图</div>
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
          <p>累积死亡</p>
          <p style="color: rgb(93, 112, 146)">{{ chinaData.deadCount }}</p>
        </div>
        <div>
          <p>累积治愈</p>
          <p style="color: rgb(40, 183, 163)">{{ chinaData.curedCount }}</p>
        </div>
      </div>

      <div class="info" id="worldinfo">
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
          <p>累积死亡</p>
          <p style="color: rgb(93, 112, 146)">{{ worldData.deadCount }}</p>
        </div>
        <div>
          <p>累积治愈</p>
          <p style="color: rgb(40, 183, 163)">{{ worldData.curedCount }}</p>
        </div>
      </div>
    </div>
    <div id="cnmap" class="map"></div>
    <div id="worldmap" class="map"></div>
    <div class="copyright">
      <a target="_blank" href="https://www.ghpym.com/2020cnyqt.html"
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
  name: "HelloWorld",
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
      let btncn = document.getElementById("btn-cn");
      let btnworld = document.getElementById("btn-world");

      cnmap.style.display = "none";
      worldmap.style.display = "block";
      cninfo.style.display = "none";
      worldinfo.style.display = "flex";
      btncn.className = "button";
      btnworld.className = "button btn-active";
    },
    async loadData() {
      axios
        .get("https://lab.isaaclin.cn/nCoV/api/overall?latest=1")
        .then((response) => {
          let data = response.data.results[0];
          console.log(data);
          this.chinaData = {
            currentConfirmedCount: data.currentConfirmedCount,
            confirmedCount: data.confirmedCount,
            deadCount: data.deadCount,
            curedCount: data.curedCount,
          };
          this.worldData = {
            currentConfirmedCount: data.globalStatistics.currentConfirmedCount,
            confirmedCount: data.globalStatistics.confirmedCount,
            deadCount: data.globalStatistics.deadCount,
            curedCount: data.globalStatistics.curedCount,
          };
        });

      axios
        // .get("https://lab.isaaclin.cn/nCoV/api/area", {
        .get("static/area.json")
        .then((response) => {
          console.log(response.data.results);
          let data = response.data.results;
          let tempChinaData = [];
          let tempWorldData = [];
          for (let i = 0; i < data.length; i++) {
            const item = data[i];
            if (item.countryName === "中国" && item.provinceName != "中国") {
              tempChinaData.push({
                name: item.provinceShortName,
                provinceName: item.provinceShortName,
                value: item.currentConfirmedCount,
              });
            } else {
              let maps = {
                "United States of America": "United States",
                "Russian Federation": "Russia",

                "Republic of Korea": "Korea",

                "Bolivia (Plurinational State of)": "Bolivia",
                "Democratic Republic of the Congo": "Dem. Rep. Congo",
                "The Republic of Zambia": "Zambia",
                "Central African Republic": "Central African Rep.",
                "The Republic of Burundi": "Burundi",
              };
              if (typeof maps[item.countryFullName] !== "undefined") {
                item.countryFullName = maps[item.countryFullName];
                console.log(item.currentConfirmedCount);
              }
              tempWorldData.push({
                name: item.countryFullName,
                provinceName: item.countryName,
                value: item.currentConfirmedCount,
              });
            }
          }
          console.log(tempChinaData);
          console.log(tempWorldData);
          // tempChinaData = [
          //   { name: "北京", provinceName: "北京", value: 345 },
          // ];
          this.chinaDetailData = tempChinaData;
          this.worldDetailData = tempWorldData;
          this.loadMap();
        });
      // this.worldDetailData = [
      //   { name: "United States", value: 8496432, provinceName: "\u7f8e\u56fd" },
      //   { name: "France", value: 7009810, provinceName: "\u6cd5\u56fd" },
      //   {
      //     name: "United Kingdom",
      //     value: 3222281,
      //     provinceName: "\u82f1\u56fd",
      //   },
      //   { name: "Netherlands", value: 2431113, provinceName: "\u8377\u5170" },
      //   { name: "Turkey", value: 1725833, provinceName: "\u571f\u8033\u5176" },
      //   { name: "Belgium", value: 1535693, provinceName: "\u6bd4\u5229\u65f6" },
      //   {
      //     name: "Serbia",
      //     value: 1223637,
      //     provinceName: "\u585e\u5c14\u7ef4\u4e9a",
      //   },
      //   { name: "Sweden", value: 1168654, provinceName: "\u745e\u5178" },
      //   { name: "Russia", value: 970549, provinceName: "\u4fc4\u7f57\u65af" },
      //   { name: "Germany", value: 946979, provinceName: "\u5fb7\u56fd" },
      //   { name: "Brazil", value: 910778, provinceName: "\u5df4\u897f" },
      //   {
      //     name: "Kazakhstan",
      //     value: 904484,
      //     provinceName: "\u54c8\u8428\u514b\u65af\u5766",
      //   },
      //   { name: "India", value: 819530, provinceName: "\u5370\u5ea6" },
      //   {
      //     name: "Iran (Islamic Republic of)",
      //     value: 808359,
      //     provinceName: "\u4f0a\u6717",
      //   },
      //   {
      //     name: "Slovakia",
      //     value: 795562,
      //     provinceName: "\u65af\u6d1b\u4f10\u514b",
      //   },
      //   { name: "Ukraine", value: 622010, provinceName: "\u4e4c\u514b\u5170" },
      //   { name: "Switzerland", value: 611420, provinceName: "\u745e\u58eb" },
      //   { name: "Greece", value: 493660, provinceName: "\u5e0c\u814a" },
      //   { name: "Ireland", value: 484660, provinceName: "\u7231\u5c14\u5170" },
      //   { name: "Mexico", value: 433419, provinceName: "\u58a8\u897f\u54e5" },
      //   {
      //     name: "Slovenia",
      //     value: 391085,
      //     provinceName: "\u65af\u6d1b\u6587\u5c3c\u4e9a",
      //   },
      //   { name: "Poland", value: 357836, provinceName: "\u6ce2\u5170" },
      //   { name: "Austria", value: 318734, provinceName: "\u5965\u5730\u5229" },
      //   { name: "Italy", value: 304713, provinceName: "\u610f\u5927\u5229" },
      //   {
      //     name: "Honduras",
      //     value: 247687,
      //     provinceName: "\u6d2a\u90fd\u62c9\u65af",
      //   },
      //   { name: "Vietnam", value: 202886, provinceName: "\u8d8a\u5357" },
      //   {
      //     name: "Georgia",
      //     value: 202798,
      //     provinceName: "\u683c\u9c81\u5409\u4e9a",
      //   },
      //   { name: "Czechia", value: 188787, provinceName: "\u6377\u514b" },
      //   {
      //     name: "Puerto Rico",
      //     value: 183646,
      //     provinceName: "\u6ce2\u591a\u9ece\u5404",
      //   },
      //   {
      //     name: "Australia",
      //     value: 161508,
      //     provinceName: "\u6fb3\u5927\u5229\u4e9a",
      //   },
      //   { name: "Spain", value: 158329, provinceName: "\u897f\u73ed\u7259" },
      //   { name: "Norway", value: 151490, provinceName: "\u632a\u5a01" },
      //   {
      //     name: "Bulgaria",
      //     value: 147036,
      //     provinceName: "\u4fdd\u52a0\u5229\u4e9a",
      //   },
      //   { name: "Finland", value: 142574, provinceName: "\u82ac\u5170" },
      //   { name: "Iraq", value: 139285, provinceName: "\u4f0a\u62c9\u514b" },
      //   {
      //     name: "Costa Rica",
      //     value: 120969,
      //     provinceName: "\u54e5\u65af\u8fbe\u9ece\u52a0",
      //   },
      //   { name: "Hungary", value: 117716, provinceName: "\u5308\u7259\u5229" },
      //   { name: "Cuba", value: 111051, provinceName: "\u53e4\u5df4" },
      //   {
      //     name: "Azerbaijan",
      //     value: 103748,
      //     provinceName: "\u963f\u585e\u62dc\u7586",
      //   },
      //   { name: "Libya", value: 100968, provinceName: "\u5229\u6bd4\u4e9a" },
      //   { name: "Jordan", value: 95139, provinceName: "\u7ea6\u65e6" },
      //   {
      //     name: "Armenia",
      //     value: 84489,
      //     provinceName: "\u4e9a\u7f8e\u5c3c\u4e9a",
      //   },
      //   {
      //     name: "Sri Lanka",
      //     value: 83736,
      //     provinceName: "\u65af\u91cc\u5170\u5361",
      //   },
      //   { name: "Chile", value: 82162, provinceName: "\u667a\u5229" },
      //   { name: "Korea", value: 75603, provinceName: "\u97e9\u56fd" },
      //   {
      //     name: "Guatemala",
      //     value: 75425,
      //     provinceName: "\u5371\u5730\u9a6c\u62c9",
      //   },
      //   {
      //     name: "occupied Palestinian territory",
      //     value: 75387,
      //     provinceName: "\u5df4\u52d2\u65af\u5766",
      //   },
      //   { name: "Thailand", value: 72412, provinceName: "\u6cf0\u56fd" },
      //   { name: "Argentina", value: 72243, provinceName: "\u963f\u6839\u5ef7" },
      //   {
      //     name: "Croatia",
      //     value: 71109,
      //     provinceName: "\u514b\u7f57\u5730\u4e9a",
      //   },
      //   {
      //     name: "Algeria",
      //     value: 67864,
      //     provinceName: "\u963f\u5c14\u53ca\u5229\u4e9a",
      //   },
      //   {
      //     name: "Romania",
      //     value: 66583,
      //     provinceName: "\u7f57\u9a6c\u5c3c\u4e9a",
      //   },
      //   {
      //     name: "Bosnia and Herzegovina",
      //     value: 64135,
      //     provinceName: "\u6ce2\u9ed1",
      //   },
      //   {
      //     name: "Malaysia",
      //     value: 63960,
      //     provinceName: "\u9a6c\u6765\u897f\u4e9a",
      //   },
      //   {
      //     name: "Venezuela",
      //     value: 62029,
      //     provinceName: "\u59d4\u5185\u745e\u62c9",
      //   },
      //   {
      //     name: "R\u00e9union",
      //     value: 56794,
      //     provinceName: "\u7559\u5c3c\u65fa",
      //   },
      //   { name: "Lebanon", value: 56696, provinceName: "\u9ece\u5df4\u5ae9" },
      //   {
      //     name: "Guadeloupe",
      //     value: 54032,
      //     provinceName: "\u74dc\u5fb7\u7f57\u666e\u5c9b",
      //   },
      //   { name: "Laos", value: 52426, provinceName: "\u8001\u631d" },
      //   { name: "Denmark", value: 51788, provinceName: "\u4e39\u9ea6" },
      //   {
      //     name: "Bolivia",
      //     value: 49352,
      //     provinceName: "\u73bb\u5229\u7ef4\u4e9a",
      //   },
      //   {
      //     name: "Dominican Republic",
      //     value: 47960,
      //     provinceName: "\u591a\u7c73\u5c3c\u52a0",
      //   },
      //   {
      //     name: "Ecuador",
      //     value: 46843,
      //     provinceName: "\u5384\u74dc\u591a\u5c14",
      //   },
      //   {
      //     name: "French Guiana",
      //     value: 45261,
      //     provinceName: "\u6cd5\u5c5e\u572d\u4e9a\u90a3",
      //   },
      //   {
      //     name: "Martinique",
      //     value: 43726,
      //     provinceName: "\u9a6c\u63d0\u5c3c\u514b",
      //   },
      //   { name: "Portugal", value: 42472, provinceName: "\u8461\u8404\u7259" },
      //   {
      //     name: "Swaziland",
      //     value: 42301,
      //     provinceName: "\u65af\u5a01\u58eb\u5170",
      //   },
      //   {
      //     name: "Cyprus",
      //     value: 38543,
      //     provinceName: "\u585e\u6d66\u8def\u65af",
      //   },
      //   { name: "Egypt", value: 37661, provinceName: "\u57c3\u53ca" },
      //   { name: "Canada", value: 36387, provinceName: "\u52a0\u62ff\u5927" },
      //   { name: "Jamaica", value: 31685, provinceName: "\u7259\u4e70\u52a0" },
      //   { name: "Uganda", value: 29976, provinceName: "\u4e4c\u5e72\u8fbe" },
      //   { name: "Oman", value: 29777, provinceName: "\u963f\u66fc" },
      //   {
      //     name: "Colombia",
      //     value: 29080,
      //     provinceName: "\u54e5\u4f26\u6bd4\u4e9a",
      //   },
      //   {
      //     name: "Bangladesh",
      //     value: 29042,
      //     provinceName: "\u5b5f\u52a0\u62c9\u56fd",
      //   },
      //   { name: "Lithuania", value: 28652, provinceName: "\u7acb\u9676\u5b9b" },
      //   {
      //     name: "Philippines",
      //     value: 27065,
      //     provinceName: "\u83f2\u5f8b\u5bbe",
      //   },
      //   {
      //     name: "Dem. Rep. Congo",
      //     value: 25918,
      //     provinceName: "\u521a\u679c\uff08\u91d1\uff09",
      //   },
      //   {
      //     name: "Tanzania",
      //     value: 25333,
      //     provinceName: "\u5766\u6851\u5c3c\u4e9a",
      //   },
      //   {
      //     name: "Afghanistan",
      //     value: 24768,
      //     provinceName: "\u963f\u5bcc\u6c57",
      //   },
      //   { name: "Cameroon", value: 23987, provinceName: "\u5580\u9ea6\u9686" },
      //   {
      //     name: "French Polynesia",
      //     value: 23504,
      //     provinceName: "\u6cd5\u5c5e\u6ce2\u5229\u5c3c\u897f\u4e9a",
      //   },
      //   {
      //     name: "Pakistan",
      //     value: 22479,
      //     provinceName: "\u5df4\u57fa\u65af\u5766",
      //   },
      //   { name: "Suriname", value: 22355, provinceName: "\u82cf\u91cc\u5357" },
      //   {
      //     name: "Estonia",
      //     value: 21886,
      //     provinceName: "\u7231\u6c99\u5c3c\u4e9a",
      //   },
      //   {
      //     name: "Uzbekstan",
      //     value: 20874,
      //     provinceName: "\u4e4c\u5179\u522b\u514b\u65af\u5766",
      //   },
      //   {
      //     name: "Syrian\u00a0ArabRepublic",
      //     value: 20793,
      //     provinceName: "\u53d9\u5229\u4e9a",
      //   },
      //   { name: "Mayotte", value: 20675, provinceName: "\u9a6c\u7ea6\u7279" },
      //   {
      //     name: "Botswana",
      //     value: 20595,
      //     provinceName: "\u535a\u8328\u74e6\u7eb3",
      //   },
      //   {
      //     name: "The Republic of Burundi",
      //     value: 20290,
      //     provinceName: "\u5e03\u9686\u8fea\u5171\u548c\u56fd",
      //   },
      //   { name: "South Africa", value: 18288, provinceName: "\u5357\u975e" },
      //   { name: "Singapore", value: 17135, provinceName: "\u65b0\u52a0\u5761" },
      //   {
      //     name: "Mauritius",
      //     value: 16885,
      //     provinceName: "\u6bdb\u91cc\u6c42\u65af",
      //   },
      //   { name: "Tunisia", value: 16853, provinceName: "\u7a81\u5c3c\u65af" },
      //   {
      //     name: "Barbados",
      //     value: 16598,
      //     provinceName: "\u5df4\u5df4\u591a\u65af",
      //   },
      //   {
      //     name: "Ethiopia",
      //     value: 16496,
      //     provinceName: "\u57c3\u585e\u4fc4\u6bd4\u4e9a",
      //   },
      //   {
      //     name: "The Republic of El Salvador",
      //     value: 16199,
      //     provinceName: "\u8428\u5c14\u74e6\u591a",
      //   },
      //   { name: "Lesotho", value: 14235, provinceName: "\u83b1\u7d22\u6258" },
      //   { name: "Cambodia", value: 14103, provinceName: "\u67ec\u57d4\u5be8" },
      //   {
      //     name: "Latvia",
      //     value: 13358,
      //     provinceName: "\u62c9\u8131\u7ef4\u4e9a",
      //   },
      //   {
      //     name: "Cura\u00e7ao",
      //     value: 12646,
      //     provinceName: "\u5e93\u62c9\u7d22\u5c9b",
      //   },
      //   { name: "Somalia", value: 12395, provinceName: "\u7d22\u9a6c\u91cc" },
      //   {
      //     name: "Nicaragua",
      //     value: 12118,
      //     provinceName: "\u5c3c\u52a0\u62c9\u74dc",
      //   },
      //   {
      //     name: "New Caledonia",
      //     value: 11468,
      //     provinceName: "\u65b0\u5580\u91cc\u591a\u5c3c\u4e9a",
      //   },
      //   { name: "Belize", value: 10987, provinceName: "\u4f2f\u5229\u5179" },
      //   {
      //     name: "Congo",
      //     value: 10170,
      //     provinceName: "\u521a\u679c\uff08\u5e03\uff09",
      //   },
      //   { name: "Gabon", value: 9724, provinceName: "\u52a0\u84ec" },
      //   {
      //     name: "Brunei Darussalam",
      //     value: 9626,
      //     provinceName: "\u6587\u83b1",
      //   },
      //   {
      //     name: "Trinidad & Tobago",
      //     value: 9253,
      //     provinceName: "\u7279\u7acb\u5c3c\u8fbe\u548c\u591a\u5df4\u54e5",
      //   },
      //   {
      //     name: "Republic of Moldova",
      //     value: 8739,
      //     provinceName: "\u6469\u5c14\u591a\u74e6",
      //   },
      //   {
      //     name: "Belarus",
      //     value: 8592,
      //     provinceName: "\u767d\u4fc4\u7f57\u65af",
      //   },
      //   { name: "Nepal", value: 8376, provinceName: "\u5c3c\u6cca\u5c14" },
      //   {
      //     name: "Albania",
      //     value: 8175,
      //     provinceName: "\u963f\u5c14\u5df4\u5c3c\u4e9a",
      //   },
      //   {
      //     name: "North Macedonia",
      //     value: 8164,
      //     provinceName: "\u5317\u9a6c\u5176\u987f",
      //   },
      //   {
      //     name: "Indonesia",
      //     value: 7823,
      //     provinceName: "\u5370\u5ea6\u5c3c\u897f\u4e9a",
      //   },
      //   {
      //     name: "The Republic of Yemen",
      //     value: 7666,
      //     provinceName: "\u4e5f\u95e8\u5171\u548c\u56fd",
      //   },
      //   { name: "Myanmar", value: 7471, provinceName: "\u7f05\u7538" },
      //   { name: "Rwanda", value: 7377, provinceName: "\u5362\u65fa\u8fbe" },
      //   { name: "Ghana", value: 7064, provinceName: "\u52a0\u7eb3" },
      //   { name: "Montenegro", value: 6681, provinceName: "\u9ed1\u5c71" },
      //   { name: "Sudan", value: 6405, provinceName: "\u82cf\u4e39" },
      //   {
      //     name: "Kyrgyzstan",
      //     value: 6264,
      //     provinceName: "\u5409\u5c14\u5409\u65af\u65af\u5766",
      //   },
      //   { name: "Israel", value: 5412, provinceName: "\u4ee5\u8272\u5217" },
      //   {
      //     name: "Saint Vincent and the Grenadines",
      //     value: 5148,
      //     provinceName:
      //       "\u5723\u6587\u68ee\u7279\u548c\u683c\u6797\u7eb3\u4e01\u65af",
      //   },
      //   {
      //     name: "The Republic of Haiti",
      //     value: 4956,
      //     provinceName: "\u6d77\u5730",
      //   },
      //   {
      //     name: "Central African Republic",
      //     value: 4706,
      //     provinceName: "\u4e2d\u975e\u5171\u548c\u56fd",
      //   },
      //   {
      //     name: "New Zealand",
      //     value: 4436,
      //     provinceName: "\u65b0\u897f\u5170",
      //   },
      //   {
      //     name: "Cayman Islands",
      //     value: 4371,
      //     provinceName: "\u5f00\u66fc\u7fa4\u5c9b",
      //   },
      //   {
      //     name: "Maldives",
      //     value: 4185,
      //     provinceName: "\u9a6c\u5c14\u4ee3\u592b",
      //   },
      //   {
      //     name: "Saudi Arabia",
      //     value: 4173,
      //     provinceName: "\u6c99\u7279\u963f\u62c9\u4f2f",
      //   },
      //   {
      //     name: "Nigeria",
      //     value: 4041,
      //     provinceName: "\u5c3c\u65e5\u5229\u4e9a",
      //   },
      //   { name: "Morocco", value: 3833, provinceName: "\u6469\u6d1b\u54e5" },
      //   { name: "Benin", value: 3755, provinceName: "\u8d1d\u5b81" },
      //   { name: "Bahamas", value: 3663, provinceName: "\u5df4\u54c8\u9a6c" },
      //   { name: "Guam", value: 3625, provinceName: "\u5173\u5c9b" },
      //   {
      //     name: "Isle of Man",
      //     value: 3599,
      //     provinceName: "\u9a6c\u6069\u5c9b",
      //   },
      //   {
      //     name: "The Republic of Fiji",
      //     value: 3411,
      //     provinceName: "\u6590\u6d4e",
      //   },
      //   { name: "Luxembourg", value: 3270, provinceName: "\u5362\u68ee\u5821" },
      //   {
      //     name: "Papua New Guinea",
      //     value: 3269,
      //     provinceName: "\u5df4\u5e03\u4e9a\u65b0\u51e0\u5185\u4e9a",
      //   },
      //   {
      //     name: "Mauritania",
      //     value: 3180,
      //     provinceName: "\u6bdb\u91cc\u5854\u5c3c\u4e9a",
      //   },
      //   { name: "China", value: 3069, provinceName: "\u4e2d\u56fd" },
      //   {
      //     name: "United Arab Emirates",
      //     value: 3063,
      //     provinceName: "\u963f\u8054\u914b",
      //   },
      //   { name: "Togo", value: 3048, provinceName: "\u591a\u54e5" },
      //   { name: "Jersey", value: 2812, provinceName: "\u6cfd\u897f\u5c9b" },
      //   { name: "Uruguay", value: 2730, provinceName: "\u4e4c\u62c9\u572d" },
      //   {
      //     name: "Namibia",
      //     value: 2721,
      //     provinceName: "\u7eb3\u7c73\u6bd4\u4e9a",
      //   },
      //   {
      //     name: "Dominica",
      //     value: 2548,
      //     provinceName: "\u591a\u7c73\u5c3c\u514b",
      //   },
      //   {
      //     name: "Cote d Ivoire",
      //     value: 2401,
      //     provinceName: "\u79d1\u7279\u8fea\u74e6",
      //   },
      //   {
      //     name: "Saint Martin",
      //     value: 2357,
      //     provinceName: "\u5723\u9a6c\u4e01\u5c9b",
      //   },
      //   {
      //     name: "Mozambique",
      //     value: 2271,
      //     provinceName: "\u83ab\u6851\u6bd4\u514b",
      //   },
      //   { name: "Panama", value: 2267, provinceName: "\u5df4\u62ff\u9a6c" },
      //   {
      //     name: "Eq.Guinea",
      //     value: 2072,
      //     provinceName: "\u8d64\u9053\u51e0\u5185\u4e9a",
      //   },
      //   { name: "Mali", value: 2043, provinceName: "\u9a6c\u91cc" },
      //   {
      //     name: "Faroe Islands",
      //     value: 2007,
      //     provinceName: "\u6cd5\u7f57\u7fa4\u5c9b",
      //   },
      //   {
      //     name: "Antigua & Barbuda",
      //     value: 1893,
      //     provinceName: "\u5b89\u63d0\u74dc\u548c\u5df4\u5e03\u8fbe",
      //   },
      //   { name: "Bermuda", value: 1889, provinceName: "\u767e\u6155\u5927" },
      //   { name: "Seychelles", value: 1867, provinceName: "\u585e\u820c\u5c14" },
      //   { name: "Iceland", value: 1848, provinceName: "\u51b0\u5c9b" },
      //   {
      //     name: "Sierra Leone",
      //     value: 1845,
      //     provinceName: "\u585e\u62c9\u5229\u6602",
      //   },
      //   { name: "Qatar", value: 1771, provinceName: "\u5361\u5854\u5c14" },
      //   {
      //     name: "Saint Kitts and Nevis",
      //     value: 1736,
      //     provinceName: "\u5723\u5176\u8328\u548c\u5c3c\u7ef4\u65af",
      //   },
      //   {
      //     name: "Saint Barthelemy",
      //     value: 1657,
      //     provinceName: "\u5723\u5df4\u6cf0\u52d2\u7c73\u5c9b",
      //   },
      //   { name: "Guernsey", value: 1422, provinceName: "\u6839\u897f\u5c9b" },
      //   {
      //     name: "Tinor-Leste",
      //     value: 1419,
      //     provinceName: "\u4e1c\u5e1d\u6c76",
      //   },
      //   { name: "Kenya", value: 1409, provinceName: "\u80af\u5c3c\u4e9a" },
      //   {
      //     name: "Madagascar",
      //     value: 1386,
      //     provinceName: "\u9a6c\u8fbe\u52a0\u65af\u52a0",
      //   },
      //   {
      //     name: "Burkina Faso",
      //     value: 1357,
      //     provinceName: "\u5e03\u57fa\u7eb3\u6cd5\u7d22",
      //   },
      //   { name: "Cabo Verde", value: 1349, provinceName: "\u4f5b\u5f97\u89d2" },
      //   { name: "Guinea", value: 1338, provinceName: "\u51e0\u5185\u4e9a" },
      //   {
      //     name: "South Sudan",
      //     value: 1310,
      //     provinceName: "\u5357\u82cf\u4e39",
      //   },
      //   {
      //     name: "Gibraltar",
      //     value: 1305,
      //     provinceName: "\u76f4\u5e03\u7f57\u9640",
      //   },
      //   {
      //     name: "The Republic of Djibouti",
      //     value: 1153,
      //     provinceName: "\u5409\u5e03\u63d0",
      //   },
      //   { name: "Malta", value: 1103, provinceName: "\u9a6c\u8033\u4ed6" },
      //   {
      //     name: "Guinea-Bissau",
      //     value: 1051,
      //     provinceName: "\u51e0\u5185\u4e9a\u6bd4\u7ecd",
      //   },
      //   { name: "Japan", value: 986, provinceName: "\u65e5\u672c" },
      //   {
      //     name: "S\u00e3o Tom\u00e9 and Pr\u00edncipe",
      //     value: 930,
      //     provinceName: "\u5723\u591a\u7f8e\u548c\u666e\u6797\u897f\u6bd4",
      //   },
      //   {
      //     name: "United States Virgin Islands",
      //     value: 871,
      //     provinceName: "\u7f8e\u5c5e\u7ef4\u5c14\u4eac\u7fa4\u5c9b",
      //   },
      //   { name: "Aruba", value: 815, provinceName: "\u963f\u9c81\u5df4" },
      //   { name: "Malawi", value: 803, provinceName: "\u9a6c\u62c9\u7ef4" },
      //   { name: "Anguilla", value: 797, provinceName: "\u5b89\u572d\u62c9" },
      //   { name: "Niger", value: 786, provinceName: "\u5c3c\u65e5\u5c14" },
      //   {
      //     name: "Liechtenstein",
      //     value: 707,
      //     provinceName: "\u5217\u652f\u6566\u58eb\u767b",
      //   },
      //   { name: "Andorra", value: 667, provinceName: "\u5b89\u9053\u5c14" },
      //   { name: "Greenland", value: 612, provinceName: "\u683c\u9675\u5170" },
      //   {
      //     name: "Saint Lucia",
      //     value: 522,
      //     provinceName: "\u5723\u5362\u897f\u4e9a",
      //   },
      //   { name: "Paraguay", value: 504, provinceName: "\u5df4\u62c9\u572d" },
      //   {
      //     name: "Zimbabwe",
      //     value: 479,
      //     provinceName: "\u6d25\u5df4\u5e03\u97e6",
      //   },
      //   {
      //     name: "Eritrea",
      //     value: 439,
      //     provinceName: "\u5384\u7acb\u7279\u91cc\u4e9a",
      //   },
      //   {
      //     name: "Sint Maarten",
      //     value: 436,
      //     provinceName: "\u8377\u5c5e\u5723\u9a6c\u4e01",
      //   },
      //   {
      //     name: "Northern Mariana Islands (Commonwealth of the)",
      //     value: 396,
      //     provinceName:
      //       "\u5317\u9a6c\u91cc\u4e9a\u7eb3\u7fa4\u5c9b\u8054\u90a6",
      //   },
      //   {
      //     name: "San Marino",
      //     value: 355,
      //     provinceName: "\u5723\u9a6c\u529b\u8bfa",
      //   },
      //   {
      //     name: "Senegal",
      //     value: 330,
      //     provinceName: "\u585e\u5185\u52a0\u5c14",
      //   },
      //   {
      //     name: "Union des Comores",
      //     value: 327,
      //     provinceName: "\u79d1\u6469\u7f57",
      //   },
      //   { name: "Monaco", value: 262, provinceName: "\u6469\u7eb3\u54e5" },
      //   {
      //     name: "Turks & Caicos\u00a0Islands",
      //     value: 257,
      //     provinceName:
      //       "\u7279\u514b\u65af\u548c\u51ef\u79d1\u65af\u7fa4\u5c9b",
      //   },
      //   { name: "Kuwait", value: 225, provinceName: "\u79d1\u5a01\u7279" },
      //   { name: "Bahrain", value: 222, provinceName: "\u5df4\u6797" },
      //   { name: "Guyana", value: 220, provinceName: "\u572d\u4e9a\u90a3" },
      //   {
      //     name: "Grenada",
      //     value: 186,
      //     provinceName: "\u683c\u6797\u90a3\u8fbe",
      //   },
      //   { name: "Angola", value: 179, provinceName: "\u5b89\u54e5\u62c9" },
      //   {
      //     name: "Bonaire, Sint Eustatius and Saba",
      //     value: 174,
      //     provinceName: "\u8377\u5170\u52a0\u52d2\u6bd4\u5730\u533a",
      //   },
      //   {
      //     name: "VirginIslands,British",
      //     value: 172,
      //     provinceName: "\u82f1\u5c5e\u7ef4\u5c14\u4eac\u7fa4\u5c9b",
      //   },
      //   {
      //     name: "International conveyance (Diamond Princess)",
      //     value: 154,
      //     provinceName: "\u94bb\u77f3\u516c\u4e3b\u53f7\u90ae\u8f6e",
      //   },
      //   {
      //     name: "Liberia",
      //     value: 140,
      //     provinceName: "\u5229\u6bd4\u91cc\u4e9a",
      //   },
      //   {
      //     name: "The Republic of Zambia",
      //     value: 87,
      //     provinceName: "\u8d5e\u6bd4\u4e9a\u5171\u548c\u56fd",
      //   },
      //   { name: "Chad", value: 75, provinceName: "\u4e4d\u5f97" },
      //   { name: "Gambia", value: 57, provinceName: "\u5188\u6bd4\u4e9a" },
      //   { name: "Bhutan", value: 36, provinceName: "\u4e0d\u4e39" },
      //   {
      //     name: "Falkland Islands",
      //     value: 16,
      //     provinceName: "\u798f\u514b\u5170\u7fa4\u5c9b",
      //   },
      //   {
      //     name: "Montserrat",
      //     value: 13,
      //     provinceName: "\u8499\u7279\u585e\u62c9\u7279",
      //   },
      //   {
      //     name: "Saint Pierre and Miquelon",
      //     value: 3,
      //     provinceName:
      //       "\u5723\u76ae\u57c3\u5c14\u548c\u5bc6\u514b\u9686\u7fa4\u5c9b",
      //   },
      //   { name: "Holy See", value: 2, provinceName: "\u68b5\u8482\u5188" },
      //   {
      //     name: "Tajikistan",
      //     value: -373,
      //     provinceName: "\u5854\u5409\u514b\u65af\u5766",
      //   },
      //   { name: "Mongolia", value: -23735, provinceName: "\u8499\u53e4" },
      //   { name: "Peru", value: -181115, provinceName: "\u79d8\u9c81" },
      // ];
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
body {
  height: 800px;
  overflow: hidden;
}

*:focus {
  outline: none;
}

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
  height: 600px;
}

#worldmap {
  height: 580px;
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
