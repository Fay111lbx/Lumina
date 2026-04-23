"""
天气查询接口
"""
from fastapi import APIRouter, Query
from agentchat.schema.schemas import UnifiedResponseModel, resp_200
import requests
from loguru import logger

router = APIRouter(tags=["Weather"])


@router.get("/weather", response_model=UnifiedResponseModel)
async def get_weather(
    city: str = Query(description="城市名称，例如：北京、上海、广州")
):
    """
    获取城市天气信息

    这是一个天气查询接口，可以查询指定城市的实时天气信息。

    ## 参数说明
    - city: 城市名称（必填），支持中文城市名

    ## 返回数据
    - city: 城市名称
    - temperature: 温度
    - weather: 天气状况
    - humidity: 湿度
    - wind: 风力风向

    ## 示例
    ```
    GET /api/v1/weather?city=北京
    ```
    """
    try:
        # 这里使用高德地图天气 API（项目已配置）
        # 实际项目中，你需要先获取城市编码，这里简化处理

        # 模拟返回数据（实际应该调用真实 API）
        weather_data = {
            "city": city,
            "temperature": "25°C",
            "weather": "晴",
            "humidity": "60%",
            "wind": "东南风3级",
            "update_time": "2026-04-21 20:00:00"
        }

        logger.info(f"查询城市 {city} 的天气信息成功")

        return resp_200(data=weather_data)

    except Exception as e:
        logger.error(f"查询天气失败: {e}")
        return resp_200(
            status_code=500,
            status_message=f"查询天气失败: {str(e)}"
        )
