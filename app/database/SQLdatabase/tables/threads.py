import sqlalchemy as sa
from sqlalchemy.event import listen
from sqlalchemy.orm import relationship, Mapped, Session
from sqlalchemy.sql.functions import func

from app.database.SQLdatabase.tables.base import SQLBaseModel, SessionLocal
from app.database.SQLdatabase.tables.assistants import Assistants
from app.database.SQLdatabase.tables.users import Users
from app.database.SQLdatabase.tables.files import MessageFileExtensions


class MessageTypes(SQLBaseModel):

    __tablename__ = "messagetypes"

    name = sa.Column(sa.Text, nullable=False)

    # Children
    threadhistory:Mapped[list["ThreadMessages"]] = relationship(back_populates="messagetype")


class Threads(SQLBaseModel):

    __tablename__ = "threads"

    assistant_id = sa.Column(sa.Integer, sa.ForeignKey(Assistants.id), nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(Users.id), nullable=False) # owner's id

    thread_name = sa.Column(sa.Text, default = '')
    analysis_key = sa.Column(sa.Text, nullable=True, default=None)

    mongodb_id = sa.Column(sa.Text, nullable=True, default=None)

    is_named = sa.Column(sa.Boolean, nullable = True)

    # Parents
    assistant:Mapped["Assistants"] = relationship(back_populates="thread")
    user:Mapped["Users"] = relationship(back_populates="thread")
    # Children
    threadhistory:Mapped[list["ThreadMessages"]] = relationship(back_populates="thread")
    suggestions: Mapped[list["PromptSuggestions"]] = relationship(back_populates="thread")

class ThreadOwner(SQLBaseModel):

    __tablename__ = "threadowner"

    thread_id = sa.Column(sa.Integer, sa.ForeignKey(Threads.id), nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(Users.id), nullable=False)


class ThreadAccess(SQLBaseModel): # threads shared and accessed

    __tablename__ = "threadaccess"

    thread_id = sa.Column(sa.Integer, sa.ForeignKey(Threads.id), nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(Users.id), nullable=False)


class ThreadShared(SQLBaseModel): # threads shared but not yet accessed

    __tablename__ = "threadshared"

    thread_id = sa.Column(sa.Integer, sa.ForeignKey(Threads.id), nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(Users.id), nullable=False) # id of user who shared and who it was shared with


class ThreadMessages(SQLBaseModel): # messages for a specific thread

    __tablename__ = "threadhistory"

    thread_id = sa.Column(sa.Integer, sa.ForeignKey(Threads.id), nullable=False)
    messagetype_id = sa.Column(sa.Integer, sa.ForeignKey(MessageTypes.id), nullable=False)

    content = sa.Column(sa.Text, default = '', nullable=False)
    counter = sa.Column(sa.Integer, default = 1)
    analysis_key = sa.Column(sa.Text, nullable=True, default=None)

    user_liked = sa.Column(sa.Boolean, nullable=True, default=None)
    user_feedback = sa.Column(sa.Text, nullable=True, default=None)

    mongodb_id = sa.Column(sa.Text, nullable=True, default=None)

    __table_args__ = (sa.UniqueConstraint(thread_id, counter),)

    # Parents
    thread:Mapped["Threads"] = relationship(back_populates="threadhistory")
    messagetype:Mapped["MessageTypes"] = relationship(back_populates="threadhistory")
    # Children
    messagefile:Mapped[list["MessageFiles"]] = relationship(back_populates="threadhistory")
    messageimage:Mapped[list["MessageImages"]] = relationship(back_populates="threadhistory")
    suggestions:Mapped[list["PromptSuggestions"]] = relationship(back_populates="thread_message")

class MessageFiles(SQLBaseModel):

    __tablename__ = "messagefiles"

    threadmessage_id = sa.Column(sa.Integer, sa.ForeignKey(ThreadMessages.id), nullable=False)
    extension_id = sa.Column(sa.Integer, sa.ForeignKey(MessageFileExtensions.id), nullable=False)

    filename = sa.Column(sa.Text, nullable=False)
    save_name = sa.Column(sa.Text, nullable=False)
    total_page_num = sa.Column(sa.Integer, nullable=False)
    analysis_key = sa.Column(sa.Text, nullable=True, default=None)

    # Parents
    threadhistory:Mapped["ThreadMessages"] = relationship(back_populates="messagefile")
    messagefileextension:Mapped["MessageFileExtensions"] = relationship(back_populates="messagefile")


class MessageImages(SQLBaseModel):

    __tablename__ = "messageimages"

    threadmessage_id = sa.Column(sa.Integer, sa.ForeignKey(ThreadMessages.id), nullable=False)

    data_uri = sa.Column(sa.Text, nullable=False, default=None)
    analysis_key = sa.Column(sa.Text, nullable=True, default=None)

    # Parents
    threadhistory:Mapped["ThreadMessages"] = relationship(back_populates="messageimage")

class PromptSuggestions(SQLBaseModel):

    __tablename__ = "promptsuggestions"

    thread_id = sa.Column(sa.Integer, sa.ForeignKey(Threads.id), nullable=False)
    threadmessage_id = sa.Column(sa.Integer, sa.ForeignKey(ThreadMessages.id), nullable=True)

    user_text = sa.Column(sa.Text, nullable=False)
    prompt = sa.Column(sa.Text, nullable=False)

    # Parent relationships
    thread: Mapped["Threads"] = relationship(back_populates="suggestions")
    thread_message: Mapped["ThreadMessages"] = relationship(back_populates="suggestions")


def increment(mapper, connection, threadmessage:ThreadMessages):
    db : Session = SessionLocal()
    last = db.query(func.max(ThreadMessages.counter)).filter(ThreadMessages.thread_id== threadmessage.thread_id).scalar()
    threadmessage.counter = 1 + (last if last else 0)
    db.close()


listen(ThreadMessages, "before_insert", increment)
