"""
数据库迁移脚本：为 user 表添加 is_admin 字段

使用方法：
python -m agentchat.database.migrations.add_is_admin_field
"""

from loguru import logger
from sqlalchemy import text
from agentchat.database import engine


def migrate():
    """添加 is_admin 字段到 user 表"""
    try:
        with engine.connect() as conn:
            # 检查字段是否已存在
            result = conn.execute(text("""
                SELECT COUNT(*) as count
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'user'
                AND COLUMN_NAME = 'is_admin'
            """))

            exists = result.fetchone()[0] > 0

            if exists:
                logger.info("is_admin 字段已存在，跳过迁移")
                return

            # 添加 is_admin 字段
            conn.execute(text("""
                ALTER TABLE user
                ADD COLUMN is_admin BOOLEAN DEFAULT FALSE COMMENT '是否为管理员'
            """))

            # 将 user_id='1' 的用户设置为管理员（兼容旧数据）
            conn.execute(text("""
                UPDATE user
                SET is_admin = TRUE
                WHERE user_id = '1'
            """))

            conn.commit()
            logger.success("成功添加 is_admin 字段并迁移旧数据")

    except Exception as e:
        logger.error(f"数据库迁移失败: {e}")
        raise


if __name__ == "__main__":
    migrate()
