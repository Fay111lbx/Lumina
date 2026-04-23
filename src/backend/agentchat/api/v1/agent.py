from typing import List
from loguru import logger
from uuid import uuid4
from fastapi import APIRouter, Form, UploadFile, File, Depends, Body

from agentchat.api.services.agent import AgentService
from agentchat.schema.agent import AgentCreateReq, AgentUpdateReq, AgentSearchReq, AgentDeleteReq
from agentchat.schema.schemas import resp_200, resp_500, UnifiedResponseModel
from agentchat.settings import app_settings
from agentchat.api.services.user import UserPayload, get_login_user
from agentchat.utils.file_utils import normalize_object_storage_value

router = APIRouter(tags=["Agent"])

@router.post("/agent", response_model=UnifiedResponseModel)
async def create_agent(
    req: AgentCreateReq,
    login_user: UserPayload = Depends(get_login_user)
):
    try:
        # 判断Agent名称是否重复
        if await AgentService.check_repeat_name(name=req.name, user_id=login_user.user_id):
            return resp_500(message="应用名称重复，请更换一个")
        # 为空的话换成默认的Logo
        if not req.logo_url:
            req.logo_url = app_settings.default_config.get("agent_logo_url")
        else:
            req.logo_url = normalize_object_storage_value(req.logo_url)

        result = await AgentService.create_agent(login_user, req)
        return resp_200(data=result)
    except Exception as err:
        logger.error(err)
        return resp_500(message=str(err))


@router.get("/agent", response_model=UnifiedResponseModel)
async def get_agent(
    login_user: UserPayload = Depends(get_login_user)
):
    try:
        results = await AgentService.get_all_agent_by_user_id(user_id=login_user.user_id)
        return resp_200(data=results)
    except Exception as err:
        logger.error(err)
        return resp_500(message=str(err))


@router.delete("/agent", response_model=UnifiedResponseModel)
async def delete_agent(
    req: AgentDeleteReq,
    login_user: UserPayload = Depends(get_login_user)
):
    try:
        # 验证用户权限
        await AgentService.verify_user_permission(
            req.agent_id,
            login_user.user_id
        )

        await AgentService.delete_agent_by_id(req.agent_id)
        return resp_200()
    except Exception as err:
        logger.error(err)
        return resp_500(message=str(err))


@router.put("/agent", response_model=UnifiedResponseModel)
async def update_agent(
    agent_request: AgentUpdateReq,
    login_user: UserPayload = Depends(get_login_user)
):
    try:
        await AgentService.verify_user_permission(
            agent_request.agent_id,
            login_user.user_id
        )

        update_values = agent_request.model_dump(
            exclude={"agent_id"},
            exclude_none=True
        )
        if update_values.get("logo_url"):
            update_values["logo_url"] = normalize_object_storage_value(update_values["logo_url"])

        await AgentService.update_agent(
            agent_id=agent_request.agent_id,
            update_values=update_values,
            user_id=login_user.user_id
        )

        return resp_200()

    except Exception as err:
        logger.error(err)
        return resp_500(message=str(err))


@router.get("/agent/{agent_id}", response_model=UnifiedResponseModel)
async def get_agent_by_id(
    agent_id: str,
    login_user: UserPayload = Depends(get_login_user)
):
    """根据ID获取单个智能体详情"""
    try:
        result = await AgentService.select_agent_by_id(agent_id=agent_id)
        if not result:
            return resp_500(message="智能体不存在")

        # 验证用户权限（只能查看自己的或系统的智能体）
        if result.get('user_id') != login_user.user_id and result.get('user_id') != '0':
            return resp_500(message="没有权限访问该智能体")

        return resp_200(data=result)
    except Exception as err:
        logger.error(err)
        return resp_500(message=str(err))


@router.post("/agent/{agent_id}/clone", response_model=UnifiedResponseModel)
async def clone_agent(
    agent_id: str,
    login_user: UserPayload = Depends(get_login_user)
):
    """克隆智能体"""
    try:
        # 获取原智能体信息
        original_agent = await AgentService.select_agent_by_id(agent_id=agent_id)
        if not original_agent:
            return resp_500(message="原智能体不存在")

        # 验证用户权限
        if original_agent.get('user_id') != login_user.user_id and original_agent.get('user_id') != '0':
            return resp_500(message="没有权限克隆该智能体")

        # 创建新的智能体名称
        new_name = f"{original_agent.get('name')} - 副本"
        counter = 1
        while await AgentService.check_repeat_name(name=new_name, user_id=login_user.user_id):
            counter += 1
            new_name = f"{original_agent.get('name')} - 副本{counter}"

        # 创建克隆的智能体
        from agentchat.schema.agent import AgentCreateReq
        clone_req = AgentCreateReq(
            name=new_name,
            description=original_agent.get('description', ''),
            logo_url=original_agent.get('logo_url', ''),
            tool_ids=original_agent.get('tool_ids', []),
            llm_id=original_agent.get('llm_id', ''),
            mcp_ids=original_agent.get('mcp_ids', []),
            system_prompt=original_agent.get('system_prompt', ''),
            knowledge_ids=original_agent.get('knowledge_ids', []),
            enable_memory=original_agent.get('enable_memory', False)
        )

        result = await AgentService.create_agent(login_user, clone_req)
        return resp_200(data=result, message=f"智能体已克隆为: {new_name}")
    except Exception as err:
        logger.error(err)
        return resp_500(message=str(err))


@router.post("/agent/search", response_model=UnifiedResponseModel)
async def search_agent(
    req: AgentSearchReq,
    login_user: UserPayload = Depends(get_login_user)
):
    try:
        results = await AgentService.search_agent_name(
            name=req.name,
            user_id=login_user.user_id
        )
        return resp_200(data=results)
    except Exception as err:
        logger.error(err)
        return resp_500(message=str(err))
