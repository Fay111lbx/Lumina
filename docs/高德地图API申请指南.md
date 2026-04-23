# 高德地图天气 API 申请指南

## 第一步：注册高德开放平台账号

1. 访问：https://lbs.amap.com/
2. 点击右上角"注册/登录"
3. 使用手机号或邮箱注册账号

## 第二步：创建应用

1. 登录后，进入"控制台"：https://console.amap.com/dev/
2. 点击"应用管理" → "我的应用"
3. 点击"创建新应用"
   - 应用名称：填写你的项目名称，例如 "OmniAgent"
   - 应用类型：选择 "Web服务"

## 第三步：添加 Key

1. 在创建的应用下，点击"添加"按钮
2. 填写 Key 信息：
   - Key 名称：例如 "天气查询"
   - 服务平台：选择 "Web服务"
   - 点击"提交"

3. 创建成功后，你会看到一个 Key（格式类似：`a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`）

## 第四步：配置到项目中

将获取到的 Key 填入配置文件：

```yaml
# config.yaml
tools:
  weather:
    api_key: "你的高德地图Key"
    endpoint: "https://restapi.amap.com/v3/weather/weatherInfo?parameters"
```

## API 说明

### 接口地址
```
https://restapi.amap.com/v3/weather/weatherInfo
```

### 请求参数
- `key`: 你的 API Key
- `city`: 城市编码（adcode）或城市名称
- `extensions`: 
  - `base` - 返回实况天气
  - `all` - 返回预报天气

### 示例请求
```bash
# 查询北京实时天气
https://restapi.amap.com/v3/weather/weatherInfo?key=你的key&city=110000&extensions=base

# 查询北京未来天气预报
https://restapi.amap.com/v3/weather/weatherInfo?key=你的key&city=110000&extensions=all
```

### 返回示例
```json
{
  "status": "1",
  "count": "1",
  "info": "OK",
  "infocode": "10000",
  "lives": [
    {
      "province": "北京",
      "city": "北京市",
      "adcode": "110000",
      "weather": "晴",
      "temperature": "15",
      "winddirection": "西北",
      "windpower": "≤3",
      "humidity": "45",
      "reporttime": "2024-04-21 14:00:00"
    }
  ]
}
```

## 免费额度

- 个人开发者：每天 30 万次调用
- 对于学习和小型项目完全够用

## 注意事项

1. Key 不要泄露到公开的代码仓库
2. 如果超过配额，可以申请多个 Key 轮换使用
3. 生产环境建议做好限流和缓存

## 相关文档

- 官方文档：https://lbs.amap.com/api/webservice/guide/api/weatherinfo
- 城市编码查询：https://lbs.amap.com/api/webservice/guide/api/district
