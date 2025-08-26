import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped

from app.database.SQLdatabase.tables.base import SQLBaseModel


class AccessTypes(SQLBaseModel):

    __tablename__ = "accesstypes"

    name = sa.Column(sa.Text, nullable = False)

    # Children
    useraccess:Mapped[list["UserAccess"]] = relationship(back_populates="accesstype")
