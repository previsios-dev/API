import uuid
from sqlalchemy import Column, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from datetime import datetime
from zoneinfo import ZoneInfo
from app.db import Base

SAO_PAULO_TZ = ZoneInfo("America/Sao_Paulo")


def now_sao_paulo():
    return datetime.now(SAO_PAULO_TZ)


class Previsao(Base):
    __tablename__ = "prevision" 

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prevision_value = Column(Float) 
    created_at = Column(DateTime(timezone=True), default=now_sao_paulo, server_default=func.now())
    reservoir_id = Column(UUID(as_uuid=True)) 
    min_value = Column(Float) 
    max_value = Column(Float) 
