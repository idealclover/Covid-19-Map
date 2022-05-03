# 2022 疫情地图组件

> 😷 与其说是 2022 年，不如说是疫情第三年

之前自己一直在用的 [博客组件](https://idealclover.top/archives/617/) 停止更新了，趁着五一假期，自己抢救了一下

用 Vue.js(v3.x) 进行了前端整体的重构，把数据获取和展示分离了（原作者用的应该是一整个 PHP 文件）

数据源来自 [BlankerL/DXY-COVID-19-Crawler](https://github.com/BlankerL/DXY-COVID-19-Crawler) 通过目录中的 [`script/script.py`](script/script.py) 进行周期性爬取（我这儿是半天一次）缓存提供给前端

## 效果展示

![china.png](https://s2.loli.net/2022/05/03/yoAtXfNhE5xLbzd.png)

![world.png](https://s2.loli.net/2022/05/03/KavFkLyoNE8Ownm.png)

## 如何使用

和之前一样，支持以 iframe 形式进行一句话调用，不过地址需要改一下

新的地址在 [map.icl.moe](https://map.icl.moe)

```
<iframe src="https://map.icl.moe" height="500" frameborder="no" border="0" width="100%"> </iframe>
```

## 开发与 debug

### 后端脚本

```
python3 script/script.py
```

如果部署在服务器上，需要通过 `crontab` 进行周期性爬取

```
0 4,16 * * * /usr/local/bin/python3.8 /root/map/script.py
```

### 前端页面

```
# 安装依赖
yarn

# 开发
yarn dev

# 构建
yarn build
```
