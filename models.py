from sqlalchemy import ForeignKey, BigInteger, String
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    # wallet_id: Mapped[int] = mapped_column(ForeignKey('wallets.id', ondelete="CASCADE"))
    # wallet_name: Mapped[str] = mapped_column(ForeignKey("wallets.name"))

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    completed: Mapped[bool] = mapped_column(default=False)
    user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

# class Wallet(Base):
#     __tablename__ = "wallets"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(512), default="None(Нет названия)")

async def init_db():
    async with engine.begin() as conn:
        print('Initialize db!')
        await conn.run_sync(Base.metadata.create_all)