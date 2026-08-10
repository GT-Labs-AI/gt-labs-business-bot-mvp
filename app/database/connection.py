from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config.config import config
from app.database.models import Base

engine = create_async_engine(config.DB_URL, echo=False)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)