from sqlalchemy import Column, Integer, String, Float
from database import Base

class Function(Base):
    __tablename__ = "functions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String)  # Store code or file path
    language = Column(String)
    timeout = Column(Float)
    virtualization_type = Column(String)  # e.g., docker or gvisor

class ExecutionMetrics(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True)
    function_id = Column(Integer)
    exec_time = Column(Float)
    error = Column(String)
