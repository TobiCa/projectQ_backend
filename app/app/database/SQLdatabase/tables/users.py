import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy.orm import relationship, Mapped

from app.database.SQLdatabase.tables.base import SQLBaseModel
from app.database.SQLdatabase.tables.access import AccessTypes


class Users(SQLBaseModel):

    __tablename__ = "users"

    name = sa.Column(sa.Text, nullable=False)
    email = sa.Column(sa.Text, nullable=False)
    last_logged_in = sa.Column(sa.DateTime, nullable=True)
    consent_accepted= sa.Column(sa.DateTime, nullable=True, default=None)
    consent_accepted_bool = sa.Column(sa.Boolean, nullable=True, default=None)

    # Children
    useraccess:Mapped[list["UserAccess"]] = relationship(back_populates="user")
    thread:Mapped[list["Threads"]] = relationship(back_populates="user")
    assistantaccess:Mapped[list["AssistantAccess"]] = relationship(back_populates="user")
    sharedassistantaccess:Mapped[list["SharedAssistantAccess"]] = relationship(back_populates="user")
    assistantowner:Mapped[list["AssistantOwners"]] = relationship(back_populates="user")


class UserAccess(SQLBaseModel):

    __tablename__ = "useraccess"

    access_id = sa.Column(sa.Integer, sa.ForeignKey(AccessTypes.id), nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(Users.id), nullable=False)

    # Parents
    accesstype:Mapped["AccessTypes"] = relationship(back_populates="useraccess")
    user:Mapped["Users"] = relationship(back_populates="useraccess")
