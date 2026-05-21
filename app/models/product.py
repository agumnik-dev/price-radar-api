from datetime import datetime
from sqlalchemy import String, Float, Integer, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (UniqueConstraint("product_id", "source"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)  # amazon | walmart
    title: Mapped[str | None] = mapped_column(String)
    url: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    prices: Mapped[list["PriceRecord"]] = relationship(back_populates="product", order_by="PriceRecord.scraped_at.desc()")


class PriceRecord(Base):
    __tablename__ = "price_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    price: Mapped[float | None] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String, default="USD")
    availability: Mapped[str | None] = mapped_column(String)
    scraped_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    product: Mapped["Product"] = relationship(back_populates="prices")
