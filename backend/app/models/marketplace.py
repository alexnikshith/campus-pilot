from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, Numeric, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User

class MarketplaceItem(Base, TimestampMixin):
    __tablename__ = "marketplace_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    seller_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    campus_name: Mapped[str] = mapped_column(String(120), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    category: Mapped[str] = mapped_column(
        String(50),
        index=True,
        nullable=False
    )  # books, calculators_lab, furniture, tutoring, electronics, services
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    condition: Mapped[str] = mapped_column(
        String(30),
        default="used_good",
        nullable=False
    )  # brand_new, like_new, used_good, used_fair
    contact_method: Mapped[str] = mapped_column(
        String(50),
        default="campus_email",
        nullable=False
    )  # campus_email, phone, hostel_room
    contact_details: Mapped[str] = mapped_column(String(255), nullable=False)
    images_json: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    status: Mapped[str] = mapped_column(
        String(30),
        default="available",
        index=True,
        nullable=False
    )  # available, reserved, sold, deactivated

    seller: Mapped["User"] = relationship("User", back_populates="marketplace_items")

    def __repr__(self) -> str:
        return f"<MarketplaceItem id={self.id} title='{self.title}' price={self.price} campus='{self.campus_name}'>"
