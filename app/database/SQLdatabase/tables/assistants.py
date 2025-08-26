import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped

from app.database.SQLdatabase.tables.base import SQLBaseModel
from app.database.SQLdatabase.tables.users import Users


class AssistantTypes(SQLBaseModel):

    __tablename__ = "assistanttypes"

    name = sa.Column(sa.Text, nullable=False)

    display_name = sa.Column(sa.Text, nullable=False)
    icon = sa.Column(sa.Text, nullable=False)

    add_files = sa.Column(sa.Boolean, nullable=False, default=False)
    define_system_prompt = sa.Column(sa.Boolean, nullable=False, default=False)
    default_system_prompt = sa.Column(sa.Text, nullable=False, default='')
    description = sa.Column(sa.Text, nullable=False, default='')

    # Children
    assistant:Mapped[list["Assistants"]] = relationship(back_populates="assistanttype")


class Assistants(SQLBaseModel):

    __tablename__ = "assistants"

    assistanttype_id = sa.Column(sa.Integer, sa.ForeignKey(AssistantTypes.id), nullable=False)

    name = sa.Column(sa.Text, nullable=False)
    system_prompt = sa.Column(sa.Text, nullable=False)
    analysis_key = sa.Column(sa.Text, nullable=True, default=None)
    description = sa.Column(sa.Text, default='')

    user_liked = sa.Column(sa.Boolean, nullable=True, default=None)
    user_feedback = sa.Column(sa.Text, nullable=True, default=None)

    mongodb_id = sa.Column(sa.Text, default=None)

    # Parents
    assistanttype:Mapped["AssistantTypes"] = relationship(back_populates="assistant")
    # Children
    thread:Mapped[list["Threads"]] = relationship(back_populates="assistant")
    file:Mapped[list["Files"]] = relationship(back_populates="assistant")
    filepage:Mapped[list["FilePages"]] = relationship(back_populates="assistant")
    assistantaccess:Mapped[list["AssistantAccess"]] = relationship(back_populates="assistant")
    globalassistantaccess:Mapped[list["GlobalAssistantAccess"]] = relationship(back_populates="assistant")
    sharedassistantaccess:Mapped[list["SharedAssistantAccess"]] = relationship(back_populates="assistant")
    assistantowner:Mapped[list["AssistantOwners"]] = relationship(back_populates="assistant")
    customassistant:Mapped["CustomAssistant"] = relationship(back_populates="assistant")


class AssistantAccess(SQLBaseModel):

    __tablename__ = "assistantaccess"

    user_id = sa.Column(sa.Integer, sa.ForeignKey(Users.id), nullable=False)
    assistant_id = sa.Column(sa.Integer, sa.ForeignKey(Assistants.id), nullable=False)
    table_pinged = sa.Column(sa.DateTime, nullable=True, default = None)

    # Parents
    user:Mapped["Users"] = relationship(back_populates="assistantaccess")
    assistant:Mapped["Assistants"] = relationship(back_populates="assistantaccess")


class GlobalAssistantAccess(SQLBaseModel):

    __tablename__ = "globalassistantaccess"

    official_id = sa.Column(sa.UUID, nullable=True)
    assistant_id = sa.Column(sa.Integer, sa.ForeignKey(Assistants.id), nullable=False)

    # Parents
    assistant:Mapped["Assistants"] = relationship(back_populates="globalassistantaccess")


class SharedAssistantAccess(SQLBaseModel):

    __tablename__ = "sharedassistantaccess"

    user_id = sa.Column(sa.Integer, sa.ForeignKey(Users.id), nullable=False)
    assistant_id = sa.Column(sa.Integer, sa.ForeignKey(Assistants.id), nullable=False)

    # Parents
    user:Mapped["Users"] = relationship(back_populates="sharedassistantaccess")
    assistant:Mapped["Assistants"] = relationship(back_populates="sharedassistantaccess")


class CustomAssistant(SQLBaseModel):

    __tablename__ = "customassistant"

    custom_id = sa.Column(sa.UUID, nullable=True)
    assistant_id = sa.Column(sa.Integer, sa.ForeignKey(Assistants.id), nullable=False)

    # Parents
    assistant: Mapped["Assistants"] = relationship(back_populates="customassistant")


class AssistantOwners(SQLBaseModel):

    __tablename__ = "assistantowners"

    user_id = sa.Column(sa.Integer, sa.ForeignKey(Users.id), nullable=False)
    assistant_id = sa.Column(sa.Integer, sa.ForeignKey(Assistants.id), nullable=False)

    # Parents
    user:Mapped["Users"] = relationship(back_populates="assistantowner")
    assistant:Mapped["Assistants"] = relationship(back_populates="assistantowner")
