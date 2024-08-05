from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String
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
    admin: Mapped["Admin"] = relationship(back_populates="users")


class Admin(db.Model):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="admins")


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
    config: Mapped["CollectionConfig"] = relationship(back_populates="collections", uselist=False)
    periods: Mapped[list["PeriodCollection"]] = relationship(back_populates="collections")


class PeriodCollection(db.Model):
    __tablename__ = "period_collections"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_period: Mapped[int] = mapped_column(ForeignKey("periods.id"))
    id_collection: Mapped[int] = mapped_column(ForeignKey("collections.id"))
    collection: Mapped["Collection"] = relationship(back_populates="period_collections")
    period: Mapped["Period"] = relationship(back_populates="period_collections")
    assignment: Mapped["PeriodAssignment"] = relationship(back_populates="period_collections")


class CollectionConfig(db.Model):
    __tablename__ = "collection_configs"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_collection: Mapped[int] = mapped_column(ForeignKey("collections.id"))
    collection: Mapped["Collection"] = relationship(back_populates="configs")
    config: Mapped["Config"] = relationship(back_populates="collections")


class PeriodAssignment(db.Model):
    __tablename__ = "period_assignments"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_period_collection: Mapped[int] = mapped_column(ForeignKey("period_collections.id"))
    attendant_name: Mapped[str] = mapped_column(String(100), nullable=False)
    attendant_email: Mapped[str] = mapped_column(String(80))
    attendant_phone_number: Mapped[str] = mapped_column(String(15))
    period_collection: Mapped["PeriodCollection"] = relationship(back_populates="period_assignments")
