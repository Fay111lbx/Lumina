from agentchat.database.models.message import MessageDownTable, MessageLikeTable
from sqlmodel import Session, select
from agentchat.database.session import session_getter

class MessageLikeDao:

    @classmethod
    def _get_message_like_sql(cls, user_input: str, agent_output: str):
        like = MessageLikeTable(user_input=user_input, agent_output=agent_output)
        return like

    @classmethod
    def create_message_like(cls, user_input: str, agent_output: str):
        with session_getter() as session:
            session.add(cls._get_message_like_sql(user_input, agent_output))
            session.commit()

    @classmethod
    def get_message_like(cls):
        with session_getter() as session:
            sql = select(MessageLikeTable)
            result = session.exec(sql).all()
            return result


class MessageDownDao:

    @classmethod
    def _get_message_down_sql(cls, user_input: str, agent_output: str):
        down = MessageDownTable(user_input=user_input, agent_output=agent_output)
        return down

    @classmethod
    def create_message_down(cls, user_input: str, agent_output: str):
        with session_getter() as session:
            session.add(cls._get_message_down_sql(user_input, agent_output))
            session.commit()

    @classmethod
    def get_message_down(cls):
        with session_getter() as session:
            sql = select(MessageDownTable)
            result = session.exec(sql).all()
            return result


# ========== 管理员统计方法 ==========

class MessageDao:
    """消息统计DAO"""

    @classmethod
    def count_total_messages(cls) -> int:
        """统计总消息数"""
        from sqlmodel import func
        from agentchat.database.models.history import HistoryTable

        with session_getter() as session:
            statement = select(func.count(HistoryTable.id))
            return session.scalar(statement) or 0

    @classmethod
    def count_messages_by_date(cls, date) -> int:
        """统计指定日期的消息数"""
        from datetime import datetime, timedelta
        from sqlmodel import func
        from agentchat.database.models.history import HistoryTable

        start_time = datetime.combine(date, datetime.min.time())
        end_time = start_time + timedelta(days=1)

        with session_getter() as session:
            statement = select(func.count(HistoryTable.id)).where(
                HistoryTable.create_time >= start_time,
                HistoryTable.create_time < end_time
            )
            return session.scalar(statement) or 0

    @classmethod
    def count_user_messages(cls, user_id: str, start_date) -> int:
        """统计指定用户从某日期开始的消息数"""
        from sqlmodel import func
        from agentchat.database.models.history import HistoryTable
        from agentchat.database.models.dialog import DialogTable

        with session_getter() as session:
            statement = select(func.count(HistoryTable.id)).join(
                DialogTable, HistoryTable.dialog_id == DialogTable.dialog_id
            ).where(
                DialogTable.user_id == user_id,
                HistoryTable.create_time >= start_date
            )
            return session.scalar(statement) or 0
