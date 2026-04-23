"""
邮件发送接口
"""
from fastapi import APIRouter, Body, Depends
from agentchat.schema.schemas import UnifiedResponseModel, resp_200, resp_500
from agentchat.tools.send_email.action import _send_email
from agentchat.api.services.user import get_login_user, UserPayload
from agentchat.api.services.mcp_user_config import MCPUserConfigService
from agentchat.api.services.mcp_server import MCPService
from loguru import logger

router = APIRouter(tags=["Email"])


@router.post("/email/send", response_model=UnifiedResponseModel)
async def send_email(
    receiver: str = Body(description="收件人邮箱地址"),
    message: str = Body(description="邮件内容"),
    subject: str = Body(default="", description="邮件主题（可选）"),
    login_user: UserPayload = Depends(get_login_user)
):
    """
    发送邮件（从用户配置中读取发件人信息）

    ## 使用前提
    用户需要先在"配置管理"页面配置邮箱信息

    ## 参数说明
    - receiver: 收件人邮箱地址（必填）
    - message: 邮件内容（必填）
    - subject: 邮件主题（可选）

    ## 返回数据
    - 发送成功或失败的消息
    """
    try:
        # 1. 查找"邮件发送"这个 MCP Server
        email_server = await MCPService.get_server_by_name("邮件发送")
        if not email_server:
            return resp_500(message="邮件服务未配置，请联系管理员")

        # 2. 获取当前用户的邮件配置
        user_config = await MCPUserConfigService.get_mcp_user_config(
            user_id=login_user.user_id,
            mcp_server_id=email_server["mcp_server_id"]
        )

        # 3. 检查用户是否配置了邮箱
        if not user_config or not user_config.get("sender_email"):
            return resp_500(message="请先在【配置管理】页面设置您的邮箱信息")

        sender = user_config.get("sender_email")
        password = user_config.get("email_password")

        if not sender or not password:
            return resp_500(message="邮箱配置不完整，请检查配置")

        # 4. 调用发送邮件
        result = _send_email(sender, receiver, message, password)

        if "successful" in result:
            logger.info(f"邮件发送成功: {sender} -> {receiver}")
            return resp_200(data={"message": "邮件发送成功"})
        else:
            logger.error(f"邮件发送失败: {result}")
            return resp_500(message="邮件发送失败，请检查邮箱配置")

    except Exception as e:
        logger.error(f"发送邮件异常: {e}")
        return resp_500(message=f"发送邮件失败: {str(e)}")


@router.get("/email/config/status", response_model=UnifiedResponseModel)
async def check_email_config(login_user: UserPayload = Depends(get_login_user)):
    """
    检查当前用户是否已配置邮箱
    """
    try:
        email_server = await MCPService.get_server_by_name("邮件发送")
        if not email_server:
            return resp_200(data={"configured": False, "message": "邮件服务未启用"})

        user_config = await MCPUserConfigService.get_mcp_user_config(
            user_id=login_user.user_id,
            mcp_server_id=email_server["mcp_server_id"]
        )

        configured = bool(user_config and user_config.get("sender_email"))

        return resp_200(data={
            "configured": configured,
            "sender_email": user_config.get("sender_email") if configured else None
        })

    except Exception as e:
        logger.error(f"检查邮件配置失败: {e}")
        return resp_500(message=str(e))
