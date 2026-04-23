"""
文生图接口
"""
from fastapi import APIRouter, Body
from agentchat.schema.schemas import UnifiedResponseModel, resp_200, resp_500
from agentchat.tools.text2image.action import _text_to_image
from loguru import logger

router = APIRouter(tags=["Image"])


@router.post("/image/generate", response_model=UnifiedResponseModel)
async def generate_image(
    prompt: str = Body(description="图片描述提示词")
):
    """
    根据文字描述生成图片

    ## 参数说明
    - prompt: 图片描述提示词（必填），详细描述你想要生成的图片内容

    ## 返回数据
    - 生成的图片URL链接

    ## 示例
    ```json
    {
      "prompt": "一只可爱的橙色小猫在阳光下玩耍"
    }
    ```
    """
    try:
        result = _text_to_image(prompt)

        if "图片链接为" in result or "![图片]" in result:
            logger.info(f"图片生成成功: {prompt}")
            return resp_200(data={"message": result, "prompt": prompt})
        else:
            logger.error(f"图片生成失败: {result}")
            return resp_500(message=result)

    except Exception as e:
        logger.error(f"图片生成异常: {e}")
        return resp_500(message=f"图片生成失败: {str(e)}")
