"""
管理员后台接口 - 用于查看系统整体运营数据
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from datetime import datetime, timedelta
from agentchat.api.services.user import UserPayload, get_login_user
from agentchat.schema.schemas import resp_200, resp_500
from agentchat.database.dao.user import UserDao
from agentchat.database.dao.usage_stats import UsageStatsDao
from agentchat.database.dao.dialog import DialogDao
from agentchat.database.dao.message import MessageDao
from loguru import logger

router = APIRouter(tags=["Admin"])


def check_admin_permission(login_user: UserPayload):
    """检查是否为管理员"""
    user = UserDao.get_user_by_id(login_user.user_id)
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return True


@router.get("/admin/dashboard", summary="管理员仪表板 - 系统概览")
async def get_admin_dashboard(login_user: UserPayload = Depends(get_login_user)):
    """
    获取系统整体运营数据

    返回数据包括：
    - 总用户数、今日新增用户、活跃用户
    - 总对话数、今日对话数
    - 总消息数、今日消息数
    - Token使用量统计
    """
    try:
        check_admin_permission(login_user)

        # 获取用户统计
        total_users = UserDao.count_total_users()
        today_new_users = UserDao.count_users_by_date(datetime.now().date())
        active_users_7d = UserDao.count_active_users(days=7)
        active_users_30d = UserDao.count_active_users(days=30)

        # 获取对话统计
        total_dialogs = DialogDao.count_total_dialogs()
        today_dialogs = DialogDao.count_dialogs_by_date(datetime.now().date())

        # 获取消息统计
        total_messages = MessageDao.count_total_messages()
        today_messages = MessageDao.count_messages_by_date(datetime.now().date())

        # 获取Token使用统计
        token_stats = UsageStatsDao.get_total_token_usage()
        today_token_stats = UsageStatsDao.get_token_usage_by_date(datetime.now().date())

        return resp_200(data={
            "users": {
                "total": total_users,
                "today_new": today_new_users,
                "active_7d": active_users_7d,
                "active_30d": active_users_30d
            },
            "dialogs": {
                "total": total_dialogs,
                "today": today_dialogs
            },
            "messages": {
                "total": total_messages,
                "today": today_messages
            },
            "tokens": {
                "total_input": token_stats.get("total_input_tokens", 0),
                "total_output": token_stats.get("total_output_tokens", 0),
                "today_input": today_token_stats.get("input_tokens", 0),
                "today_output": today_token_stats.get("output_tokens", 0)
            }
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取管理员仪表板数据失败: {e}")
        return resp_500(message=f"获取数据失败: {str(e)}")


@router.get("/admin/users", summary="用户列表 - 查看所有用户")
async def get_all_users(
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=20, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(default=None, description="搜索关键词"),
    login_user: UserPayload = Depends(get_login_user)
):
    """
    获取所有用户列表（分页）

    支持按用户名搜索
    """
    try:
        check_admin_permission(login_user)

        users, total = UserDao.get_users_paginated(page, page_size, keyword)

        return resp_200(data={
            "users": [
                {
                    "user_id": user.user_id,
                    "user_name": user.user_name,
                    "create_time": user.create_time.isoformat() if user.create_time else None,
                    "update_time": user.update_time.isoformat() if user.update_time else None,
                    "delete": user.delete
                }
                for user in users
            ],
            "total": total,
            "page": page,
            "page_size": page_size
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取用户列表失败: {e}")
        return resp_500(message=f"获取用户列表失败: {str(e)}")


@router.get("/admin/users/{user_id}/stats", summary="用户详情 - 查看单个用户的使用统计")
async def get_user_stats(
    user_id: str,
    days: int = Query(default=7, ge=1, le=90, description="统计天数"),
    login_user: UserPayload = Depends(get_login_user)
):
    """
    获取指定用户的详细使用统计

    包括：
    - 对话数量
    - 消息数量
    - Token使用量
    - 使用的模型和Agent
    """
    try:
        check_admin_permission(login_user)

        # 获取用户信息
        user = UserDao.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")

        # 获取统计数据
        start_date = datetime.now() - timedelta(days=days)

        dialog_count = DialogDao.count_user_dialogs(user_id, start_date)
        message_count = MessageDao.count_user_messages(user_id, start_date)
        token_usage = UsageStatsDao.get_user_token_usage(user_id, start_date)
        model_usage = UsageStatsDao.get_user_model_usage(user_id, start_date)
        agent_usage = UsageStatsDao.get_user_agent_usage(user_id, start_date)

        return resp_200(data={
            "user": {
                "user_id": user.user_id,
                "user_name": user.user_name,
                "create_time": user.create_time.isoformat() if user.create_time else None
            },
            "stats": {
                "dialogs": dialog_count,
                "messages": message_count,
                "tokens": token_usage,
                "models": model_usage,
                "agents": agent_usage
            },
            "period": f"最近{days}天"
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取用户统计失败: {e}")
        return resp_500(message=f"获取用户统计失败: {str(e)}")


@router.get("/admin/stats/trend", summary="趋势分析 - 查看系统使用趋势")
async def get_usage_trend(
    days: int = Query(default=30, ge=1, le=90, description="统计天数"),
    login_user: UserPayload = Depends(get_login_user)
):
    """
    获取系统使用趋势数据（按天统计）

    返回每日的：
    - 新增用户数
    - 活跃用户数
    - 对话数
    - 消息数
    - Token使用量
    """
    try:
        check_admin_permission(login_user)

        trend_data = []
        for i in range(days):
            date = datetime.now().date() - timedelta(days=i)

            daily_data = {
                "date": date.isoformat(),
                "new_users": UserDao.count_users_by_date(date),
                "active_users": UserDao.count_active_users_by_date(date),
                "dialogs": DialogDao.count_dialogs_by_date(date),
                "messages": MessageDao.count_messages_by_date(date),
                "tokens": UsageStatsDao.get_token_usage_by_date(date)
            }
            trend_data.append(daily_data)

        # 反转列表，使日期从旧到新
        trend_data.reverse()

        return resp_200(data={
            "trend": trend_data,
            "period": f"最近{days}天"
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取趋势数据失败: {e}")
        return resp_500(message=f"获取趋势数据失败: {str(e)}")


@router.get("/admin/stats/models", summary="模型使用统计")
async def get_model_stats(
    days: int = Query(default=7, ge=1, le=90, description="统计天数"),
    login_user: UserPayload = Depends(get_login_user)
):
    """
    获取各模型的使用统计

    返回每个模型的：
    - 调用次数
    - Token使用量
    - 使用用户数
    """
    try:
        check_admin_permission(login_user)

        start_date = datetime.now() - timedelta(days=days)
        model_stats = UsageStatsDao.get_model_statistics(start_date)

        return resp_200(data={
            "models": model_stats,
            "period": f"最近{days}天"
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取模型统计失败: {e}")
        return resp_500(message=f"获取模型统计失败: {str(e)}")


@router.get("/admin/stats/agents", summary="Agent使用统计")
async def get_agent_stats(
    days: int = Query(default=7, ge=1, le=90, description="统计天数"),
    login_user: UserPayload = Depends(get_login_user)
):
    """
    获取各Agent的使用统计

    返回每个Agent的：
    - 调用次数
    - 使用用户数
    """
    try:
        check_admin_permission(login_user)

        start_date = datetime.now() - timedelta(days=days)
        agent_stats = UsageStatsDao.get_agent_statistics(start_date)

        return resp_200(data={
            "agents": agent_stats,
            "period": f"最近{days}天"
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取Agent统计失败: {e}")
        return resp_500(message=f"获取Agent统计失败: {str(e)}")


@router.post("/admin/users/{user_id}/disable", summary="禁用用户")
async def disable_user(
    user_id: str,
    login_user: UserPayload = Depends(get_login_user)
):
    """
    禁用指定用户
    """
    try:
        check_admin_permission(login_user)

        UserDao.disable_user(user_id)

        return resp_200(message="用户已禁用")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"禁用用户失败: {e}")
        return resp_500(message=f"禁用用户失败: {str(e)}")


@router.post("/admin/users/{user_id}/enable", summary="启用用户")
async def enable_user(
    user_id: str,
    login_user: UserPayload = Depends(get_login_user)
):
    """
    启用指定用户
    """
    try:
        check_admin_permission(login_user)

        UserDao.enable_user(user_id)

        return resp_200(message="用户已启用")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"启用用户失败: {e}")
        return resp_500(message=f"启用用户失败: {str(e)}")
