from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship, backref
from database.myEnums import OrderHistoryStatus, OrderType
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.connection import Base, engine

class Menu(Base):
    __tablename__ = "menu"
    
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name=Column(String)
    price = Column(Integer)
    item_group = Column(String)
    
    # order_history: Mapped[int] = relationship("OrderHistory", back_populates="menu")
    
class OrderHistory(Base):
    __tablename__ = "order_history"
    
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    order = Column(JSON, nullable=False)
    status: Mapped[OrderHistoryStatus] = mapped_column(default=OrderHistoryStatus.PROCESSING.value)
    type: Mapped[OrderType] = mapped_column(default=OrderType.DINE_IN)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    

    # menu = relationship("Menu", back_populates="order_history")
    
# Menu.metadata.create_all(engine)
OrderHistory.metadata.create_all(engine)
# OrderHistory.metadata.drop_all(bind=engine, tables=[OrderHistory.__table__])

    
    
