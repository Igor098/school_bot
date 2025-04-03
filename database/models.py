from sqlalchemy import Integer, String, Boolean, ForeignKey, Index, DateTime, func
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    classes = relationship("UserClass", back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username}, telegram_id={self.telegram_id})>"


class Admin(Base):
    __tablename__ = 'admins'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    added_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    note: Mapped[str] = mapped_column(String, nullable=True)

    # Связь с пользователем
    user = relationship("User", backref="admin_record")

    def __repr__(self):
        return f"<Admin(user_id={self.user_id}, added_at={self.added_at})>"


class Class(Base):
    __tablename__ = 'classes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    identifier: Mapped[str] = mapped_column(String, nullable=True)

    lessons = relationship("Lesson", back_populates="class_")
    users = relationship("UserClass", back_populates="class_")


class UserClass(Base):
    __tablename__ = 'user_classes'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    class_id: Mapped[int] = mapped_column(Integer, ForeignKey("classes.id"), nullable=False)

    user = relationship("User", back_populates="classes")
    class_ = relationship("Class", back_populates="users")


class Day(Base):
    __tablename__ = 'days'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    lessons = relationship("Lesson", back_populates="day")


class Subject(Base):
    __tablename__ = 'subjects'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    lessons = relationship("Lesson", back_populates="subject")


class Lesson(Base):
    __tablename__ = 'lessons'
    __table_args__ = (
        Index('ix_class_day_period', 'class_id', 'day_id', 'period'),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    class_id: Mapped[int] = mapped_column(Integer, ForeignKey("classes.id"), nullable=False)
    day_id: Mapped[int] = mapped_column(Integer, ForeignKey("days.id"), nullable=False)
    period: Mapped[int] = mapped_column(Integer, nullable=False)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id"), nullable=False)
    is_canceled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    class_ = relationship("Class", back_populates="lessons")
    day = relationship("Day", back_populates="lessons")
    subject = relationship("Subject", back_populates="lessons")

    def __repr__(self):
        status = "отменён" if self.is_canceled else "запланирован"
        return f"<Lesson(class_id={self.class_id}, day_id={self.day_id}, period={self.period}, status={status})>"
