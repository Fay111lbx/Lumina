"""
物流快递查询接口
"""
from fastapi import APIRouter, Query
from agentchat.schema.schemas import UnifiedResponseModel, resp_200, resp_500
from agentchat.tools.delivery.action import _get_delivery
from loguru import logger

router = APIRouter(tags=["Delivery"])


@router.get("/delivery/track", response_model=UnifiedResponseModel)
async def track_delivery(
    tracking_number: str = Query(description="快递单号")
):
    """
    查询快递物流信息

    ## 参数说明
    - tracking_number: 快递单号（必填）

    ## 返回数据
    - 快递公司名称
    - 物流跟踪信息（时间、状态）

    ## 示例
    ```
    GET /api/v1/delivery/track?tracking_number=1234567890
    ```
    """
    try:
        result = _get_delivery(tracking_number)

        logger.info(f"快递查询成功: {tracking_number}")

        return resp_200(data={
            "tracking_number": tracking_number,
            "info": result
        })

    except Exception as e:
        logger.error(f"快递查询失败: {e}")
        return resp_500(message=f"查询快递失败: {str(e)}")
