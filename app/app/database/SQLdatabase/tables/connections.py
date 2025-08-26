import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped

from app.database.SQLdatabase.tables.base import SQLBaseModel


class ConnectionStatus(SQLBaseModel):

    __tablename__ = "connectionstatus"

    name = sa.Column(sa.Text, nullable=False)

    # Children
    connectionopenai:Mapped[list["ConnectionOpenAI"]] = relationship(back_populates="connectionstatus")


class ConnectionOpenAI(SQLBaseModel):

    __tablename__ = "connectionopenai"

    connectionstatus_id = sa.Column(sa.Integer, sa.ForeignKey(ConnectionStatus.id), nullable=False)
    errortext = sa.Column(sa.Text, nullable=False)

    # Parents
    connectionstatus:Mapped["ConnectionStatus"] = relationship(back_populates="connectionopenai")


class ConnectionDB(SQLBaseModel):

    __tablename__ = "connectiondb"

    execution_time = sa.Column(sa.Float, nullable=False)
