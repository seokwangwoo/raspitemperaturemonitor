from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Float, DateTime

SQLALCHEMY_DATABASE_URL = "sqlite:///monitoring_data.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class MonitoringData(Base):
    __tablename__ = "monitoring_data"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime)
    temperature = Column(Float)
    huminity = Column(Float)

    def __repr__(self):
        return f"MonitoringData(id={self.id!r}, datetime={self.datetime!r}, temperature={self.temperature!r}, huminity={self.huminity!r})"


Base.metadata.create_all(bind=engine)


def add_data(temperature, huminity):
    db = SessionLocal()
    new_data = MonitoringData(
        datetime=datetime.now(),
        temperature=temperature,
        huminity=huminity,
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    db.close()


def get_data():
    db = SessionLocal()
    data = db.query(MonitoringData).all()
    db.close()
    return data


def get_last_data():
    db = SessionLocal()
    data = db.query(MonitoringData).order_by(MonitoringData.id.desc()).first()
    db.close()
    return data


def get_datetime_range(
    start_datetime: datetime = datetime(1970, 1, 1),
    end_datetime: datetime = datetime.now(),
):
    if not start_datetime:
        start_datetime = datetime(1970, 1, 1)
    if not end_datetime:
        end_datetime = datetime.now()

    db = SessionLocal()
    data = (
        db.query(MonitoringData)
        .filter(
            MonitoringData.datetime >= start_datetime,
            MonitoringData.datetime <= end_datetime,
        )
        .all()
    )
    db.close()
    return data
