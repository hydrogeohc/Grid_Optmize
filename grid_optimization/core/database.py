from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class GridState(Base):
    __tablename__ = "grid_state"
    id = Column(Integer, primary_key=True)
    region = Column(String)
    demand = Column(Float)
    supply = Column(Float)
    current_load = Column(Float, default=0.0)
    capacity = Column(Float, default=1000.0)
    efficiency = Column(Float, default=85.0)
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))


class OptimizationResult(Base):
    __tablename__ = "optimization_result"
    id = Column(Integer, primary_key=True)
    region = Column(String)
    optimized_supply = Column(Float)
    optimized_demand = Column(Float)
    losses = Column(Float)
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))


def get_engine(db_url="sqlite:///gridopt.db"):
    return create_engine(db_url)


def create_tables(engine):
    Base.metadata.create_all(engine)


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()


def init_db(db_url="sqlite:///gridopt.db"):
    engine = get_engine(db_url)
    create_tables(engine)
    return engine
