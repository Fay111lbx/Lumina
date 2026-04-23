from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Body, Response
# from fastapi_jwt_auth import AuthJWT

from agentchat.services.redis import redis_client
from agentchat.database.dao.user import UserDao
from agentchat.api.errcode.user import UserValidateError
from agentchat.schema.schemas import resp_200
from agentchat.utils.JWT import ACCESS_TOKEN_EXPIRE_TIME
from agentchat.api.services.user import UserService, get_login_user, get_user_jwt, UserPayload
from agentchat.database.models.user import AdminUser
from agentchat.schema.schemas import UnifiedResponseModel
from loguru import logger
from agentchat.utils.constants import USER_CURRENT_SESSION

router = APIRouter(tags=["User"])


@router.post('/user/register', response_model=UnifiedResponseModel)
async def register(user_name: str = Body(description='用户名'),
                   user_email: Optional[str] = Body(description='用户邮箱'),
                   user_password: str = Body(description='用户密码')):
    exist_user = UserDao.get_user_by_username(user_name)
    if exist_user:
        raise HTTPException(status_code=500, detail='用户名重复')
    if len(user_name) > 20:
        raise HTTPException(status_code=500, detail='用户名长度不应该超过20')
    try:
        user_password = UserService.encrypt_sha256_password(user_password)
        user_avatar = UserService.get_random_user_avatar()

        # 所有注册用户都是普通用户，不再自动创建管理员
        UserDao.add_user_and_default_role(user_name, user_email, user_password, user_avatar)
    except Exception as e:
        logger.error(f'register user is appear error: {e}')
        raise HTTPException(status_code=500, detail=f'register user is appear error: {e}')
    return resp_200()


@router.post('/user/login', response_model=UnifiedResponseModel)
async def login(response: Response,
                user_name: str = Body(description='用户名'),
                user_password: str = Body(description='用户密码')):
    # 验证码校验
    # if userConfig.USE_CAPTCHA:
    #     if not user.captcha_key or not await verify_captcha(user.captcha, user.captcha_key):
    #         raise HTTPException(status_code=500, detail='验证码错误')

    db_user = UserDao.get_user_by_username(user_name)
    # 检查密码
    if not db_user or not UserService.verify_password(user_password, db_user.user_password):
        return UserValidateError.return_resp()

    if db_user.delete:
        raise HTTPException(status_code=500, detail='该账号已被禁用，请联系管理员')

    access_token, refresh_token, role = get_user_jwt(db_user)

    # Set the JWT cookies in the response
    response.set_cookie(
        key="access_token_cookie",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_TIME,
        samesite="lax"
    )
    response.set_cookie(
        key="refresh_token_cookie",
        value=refresh_token,
        httponly=True,
        max_age=604800,  # 7 days
        samesite="lax"
    )

    # 设置登录用户当前的cookie, 比jwt有效期多一个小时
    redis_client.set(USER_CURRENT_SESSION.format(db_user.user_id), access_token, ACCESS_TOKEN_EXPIRE_TIME + 3600)

    return resp_200(data={'user_id': db_user.user_id, 'access_token': access_token})


@router.put("/user/update", response_model=UnifiedResponseModel)
async def update_user_info(user_id: str = Body(description="用户的ID"),
                           user_avatar: Optional[str] = Body(description="用户的头像地址"),
                           user_description: Optional[str] = Body(description="用户的描述")):
    UserService.update_user_info(user_id, user_avatar, user_description)
    return resp_200()


@router.get("/user/icons", response_model=UnifiedResponseModel)
async def get_select_user_avatar():
    result = UserService.get_available_avatars()

    return resp_200(result)


@router.get("/user/info", response_model=UnifiedResponseModel)
async def get_user_info(user_id: str):
    result = UserService.get_user_info_by_id(user_id)

    return resp_200(result)


@router.post('/user/setup-admin', response_model=UnifiedResponseModel)
async def setup_admin(
    user_name: str = Body(description='用户名'),
    new_password: str = Body(description='新密码'),
    login_user: UserPayload = Depends(get_login_user)
):
    """设置用户为管理员并修改密码（仅管理员可操作）"""
    # 检查当前用户是否为管理员
    current_user = UserDao.get_user_by_id(login_user.user_id)
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=403, detail='需要管理员权限')

    # 查找目标用户
    target_user = UserDao.get_user_by_username(user_name)
    if not target_user:
        raise HTTPException(status_code=404, detail='用户不存在')

    try:
        # 更新密码和管理员状态
        encrypted_password = UserService.encrypt_sha256_password(new_password)

        from sqlmodel import update
        from agentchat.database.session import session_getter
        from agentchat.database.models.user import UserTable

        with session_getter() as session:
            statement = update(UserTable).where(
                UserTable.user_id == target_user.user_id
            ).values(
                user_password=encrypted_password,
                is_admin=True
            )
            session.exec(statement)
            session.commit()

        logger.info(f"User {user_name} has been set as admin by {login_user.user_id}")
        return resp_200(data={'message': f'用户 {user_name} 已设置为管理员，密码已更新'})

    except Exception as e:
        logger.error(f"Failed to setup admin: {e}")
        raise HTTPException(status_code=500, detail=f'设置管理员失败: {str(e)}')
