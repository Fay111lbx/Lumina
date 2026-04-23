from typing import Optional, List
from sqlmodel import select, and_
from datetime import datetime, timedelta
from agentchat.database.session import async_session_getter, session_getter
from agentchat.database.models.usage_stats import UsageStats


class UsageStatsDao:

    @classmethod
    async def create_usage_stats(cls, usage_stats: UsageStats):
        async with async_session_getter() as session:
            session.add(usage_stats)
            await session.commit()
            await session.refresh(usage_stats)
            return usage_stats

    @classmethod
    def sync_create_usage_stats(cls, usage_stats: UsageStats):
        with session_getter() as session:
            session.add(usage_stats)
            session.commit()
            session.refresh(usage_stats)
            return usage_stats

    @classmethod
    async def get_agent_all_usage(cls, user_id, agent):
        async with async_session_getter() as session:
            statement = select(UsageStats).where(
                UsageStats.user_id == user_id,
                UsageStats.agent == agent
            )

            result = await session.exec(statement)
            return result.all()

    @classmethod
    async def get_agent_monthly_usage(cls, user_id, agent):
        one_month_ago = datetime.now() - timedelta(days=30)
        current_time = datetime.now()

        async with async_session_getter() as session:
            statement = select(UsageStats).where(
                UsageStats.agent == agent,
                UsageStats.user_id == user_id,
                UsageStats.create_time >= one_month_ago,
                UsageStats.create_time <= current_time
            )

            result = await session.exec(statement)
            return result.all()

    @classmethod
    async def get_agent_weekly_usage(cls, user_id, agent):
        one_week_ago = datetime.now() - timedelta(days=7)
        current_time = datetime.now()

        async with async_session_getter() as session:
            statement = select(UsageStats).where(
                UsageStats.agent == agent,
                UsageStats.user_id == user_id,
                UsageStats.create_time >= one_week_ago,
                UsageStats.create_time <= current_time
            )

            result = await session.exec(statement)
            return result.all()

    # 根据模型进行分类
    @classmethod
    async def get_model_all_usage(cls, user_id, model):
        async with async_session_getter() as session:
            statement = select(UsageStats).where(
                UsageStats.user_id == user_id,
                UsageStats.model == model
            )

            result = await session.exec(statement)
            return result.all()

    @classmethod
    async def get_model_monthly_usage(cls, user_id, model):
        one_month_ago = datetime.now() - timedelta(days=30)
        current_time = datetime.now()

        async with async_session_getter() as session:
            statement = select(UsageStats).where(
                UsageStats.model == model,
                UsageStats.user_id == user_id,
                UsageStats.create_time >= one_month_ago,
                UsageStats.create_time <= current_time
            )

            result = await session.exec(statement)
            return result.all()

    @classmethod
    async def get_model_weekly_usage(cls, user_id, model):
        one_week_ago = datetime.now() - timedelta(days=7)
        current_time = datetime.now()

        async with async_session_getter() as session:
            statement = select(UsageStats).where(
                UsageStats.model == model,
                UsageStats.user_id == user_id,
                UsageStats.create_time >= one_week_ago,
                UsageStats.create_time <= current_time
            )

            result = await session.exec(statement)
            return result.all()

    @classmethod
    async def get_agent_model_time_usage(
        cls,
        user_id: str,
        agent: Optional[str] = None,
        model: Optional[str] = None,
        delta_days: int = 10000 # 默认值可视为所有数据
    ):
        ago_time = datetime.now() - timedelta(days=delta_days)

        conditions = [
            UsageStats.user_id == user_id,
            UsageStats.create_time >= ago_time
        ]

        # 追加条件（根据agent和model是否存在）
        if agent is not None:
            conditions.append(UsageStats.agent == agent)
        if model is not None:
            conditions.append(UsageStats.model == model)

        statement = select(UsageStats).where(*conditions)

        async with async_session_getter() as session:
            result = await session.exec(statement)
            return result.all()

    @classmethod
    async def get_usage_agents(cls, user_id):
        async with async_session_getter() as session:
            statement = select(UsageStats.agent).where(
                UsageStats.user_id == user_id
            ).distinct()

            result = await session.exec(statement)
            return result.all()

    @classmethod
    async def get_usage_models(cls, user_id):
        async with async_session_getter() as session:
            statement = select(UsageStats.model).where(
                UsageStats.user_id == user_id
            ).distinct()

            result = await session.exec(statement)
            return result.all()

    # ========== 管理员统计方法 ==========

    @classmethod
    def get_total_token_usage(cls) -> dict:
        """获取系统总Token使用量"""
        from sqlmodel import func
        with session_getter() as session:
            statement = select(
                func.sum(UsageStats.input_tokens).label('total_input_tokens'),
                func.sum(UsageStats.output_tokens).label('total_output_tokens')
            )
            result = session.exec(statement).first()
            return {
                'total_input_tokens': result[0] or 0,
                'total_output_tokens': result[1] or 0
            }

    @classmethod
    def get_token_usage_by_date(cls, date) -> dict:
        """获取指定日期的Token使用量"""
        from datetime import datetime, timedelta
        from sqlmodel import func

        start_time = datetime.combine(date, datetime.min.time())
        end_time = start_time + timedelta(days=1)

        with session_getter() as session:
            statement = select(
                func.sum(UsageStats.input_tokens).label('input_tokens'),
                func.sum(UsageStats.output_tokens).label('output_tokens')
            ).where(
                UsageStats.create_time >= start_time,
                UsageStats.create_time < end_time
            )
            result = session.exec(statement).first()
            return {
                'input_tokens': result[0] or 0,
                'output_tokens': result[1] or 0
            }

    @classmethod
    def get_user_token_usage(cls, user_id: str, start_date: datetime) -> dict:
        """获取指定用户从某日期开始的Token使用量"""
        from sqlmodel import func
        with session_getter() as session:
            statement = select(
                func.sum(UsageStats.input_tokens).label('input_tokens'),
                func.sum(UsageStats.output_tokens).label('output_tokens')
            ).where(
                UsageStats.user_id == user_id,
                UsageStats.create_time >= start_date
            )
            result = session.exec(statement).first()
            return {
                'input_tokens': result[0] or 0,
                'output_tokens': result[1] or 0
            }

    @classmethod
    def get_user_model_usage(cls, user_id: str, start_date: datetime) -> list:
        """获取指定用户的模型使用统计"""
        from sqlmodel import func
        with session_getter() as session:
            statement = select(
                UsageStats.model,
                func.count(UsageStats.id).label('count'),
                func.sum(UsageStats.input_tokens).label('input_tokens'),
                func.sum(UsageStats.output_tokens).label('output_tokens')
            ).where(
                UsageStats.user_id == user_id,
                UsageStats.create_time >= start_date
            ).group_by(UsageStats.model)

            results = session.exec(statement).all()
            return [
                {
                    'model': r[0],
                    'count': r[1],
                    'input_tokens': r[2] or 0,
                    'output_tokens': r[3] or 0
                }
                for r in results
            ]

    @classmethod
    def get_user_agent_usage(cls, user_id: str, start_date: datetime) -> list:
        """获取指定用户的Agent使用统计"""
        from sqlmodel import func
        with session_getter() as session:
            statement = select(
                UsageStats.agent,
                func.count(UsageStats.id).label('count')
            ).where(
                UsageStats.user_id == user_id,
                UsageStats.create_time >= start_date
            ).group_by(UsageStats.agent)

            results = session.exec(statement).all()
            return [
                {
                    'agent': r[0],
                    'count': r[1]
                }
                for r in results
            ]

    @classmethod
    def get_model_statistics(cls, start_date: datetime) -> list:
        """获取所有模型的使用统计"""
        from sqlmodel import func
        with session_getter() as session:
            statement = select(
                UsageStats.model,
                func.count(UsageStats.id).label('call_count'),
                func.sum(UsageStats.input_tokens).label('input_tokens'),
                func.sum(UsageStats.output_tokens).label('output_tokens'),
                func.count(func.distinct(UsageStats.user_id)).label('user_count')
            ).where(
                UsageStats.create_time >= start_date
            ).group_by(UsageStats.model)

            results = session.exec(statement).all()
            return [
                {
                    'model': r[0],
                    'call_count': r[1],
                    'input_tokens': r[2] or 0,
                    'output_tokens': r[3] or 0,
                    'user_count': r[4]
                }
                for r in results
            ]

    @classmethod
    def get_agent_statistics(cls, start_date: datetime) -> list:
        """获取所有Agent的使用统计"""
        from sqlmodel import func
        with session_getter() as session:
            statement = select(
                UsageStats.agent,
                func.count(UsageStats.id).label('call_count'),
                func.count(func.distinct(UsageStats.user_id)).label('user_count')
            ).where(
                UsageStats.create_time >= start_date
            ).group_by(UsageStats.agent)

            results = session.exec(statement).all()
            return [
                {
                    'agent': r[0],
                    'call_count': r[1],
                    'user_count': r[2]
                }
                for r in results
            ]