from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(80), nullable=False)
    admin: Mapped["Admin"] = relationship(back_populates="user")


class Admin(db.Model):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="admin")


class Config(db.Model):
    __tablename__ = "config"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    value: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(600), nullable=False)


class Period(db.Model):
    __tablename__ = "periods"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(600), nullable=False)


class Collection(db.Model):
    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(600), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    configs: Mapped[list["CollectionConfig"]] = relationship(back_populates="collection")
    periods: Mapped[list["PeriodCollection"]] = relationship(back_populates="collection")


class PeriodCollection(db.Model):
    __tablename__ = "period_collections"
    __table_args__ =  (UniqueConstraint("id_period", "id_collection", name="period_collection_unique_constraint"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    id_period: Mapped[int] = mapped_column(ForeignKey("periods.id"))
    id_collection: Mapped[int] = mapped_column(ForeignKey("collections.id"))
    collection: Mapped["Collection"] = relationship(back_populates="periods", uselist=False)
    period: Mapped["Period"] = relationship(uselist=False)
    assignments: Mapped[list["PeriodAssignment"]] = relationship(back_populates="period_collection")


class CollectionConfig(db.Model):
    __tablename__ = "collection_configs"
    __table_args__ = (UniqueConstraint("id_collection", "name", name="collection_config_unique_constraint"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    id_collection: Mapped[int] = mapped_column(ForeignKey("collections.id"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(600), nullable=False)
    collection: Mapped["Collection"] = relationship(back_populates="configs", uselist=False)


class PeriodAssignment(db.Model):
    __tablename__ = "period_assignments"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_period_collection: Mapped[int] = mapped_column(ForeignKey("period_collections.id"))
    attendant_name: Mapped[str] = mapped_column(String(100), nullable=False)
    attendant_email: Mapped[str | None] = mapped_column(String(80))
    attendant_phone_number: Mapped[str | None] = mapped_column(String(15))
    period_collection: Mapped["PeriodCollection"] = relationship(back_populates="assignments", uselist=False)
