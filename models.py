from email.policy import default
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Table, Numeric
from sqlalchemy.orm import relationship
from database import Base

# связующая таблица 
climber_climbing = Table('climber_climbing', Base.metadata,
    Column('climber_id', ForeignKey('climbers.id'), primary_key=True),
    Column('climbing_id', ForeignKey('climbings.id'), primary_key=True)    
)
    
# альпинист
class Climber(Base):
    __tablename__ = 'climbers'
    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String, nullable=True)
    name = Column(String, nullable=True)
    patronymic = Column(String, nullable=True)
    address = Column(String, nullable=True)
    climbings = relationship("Climbing", secondary="climber_climbing", back_populates="climbers") 

# восхождение
class Climbing(Base):
    __tablename__ = 'climbings'
    id = Column(Integer, primary_key=True, index=True)
    date_start = Column(Date, nullable=True, index=True)
    date_end = Column(Date, nullable=True, index=True)
    name_group = Column(String, nullable=True, unique=True, index=True)
    mountain_id = Column(Integer, ForeignKey("mountains.id"))
    mountains = relationship("Mountain")
    climbers = relationship("Climber", secondary="climber_climbing", back_populates="climbings")
    
# гора
class Mountain(Base):
    __tablename__ = 'mountains'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,  unique=True, index=True)
    height = Column(Numeric, default=0, nullable=True)
    country_district = Column(String, nullable=True)

# пользователь 
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(255))