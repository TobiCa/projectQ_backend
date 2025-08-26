import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped

from app.database.SQLdatabase.tables.base import SQLBaseModel
from app.database.SQLdatabase.tables.assistants import Assistants


class FileExtensions(SQLBaseModel):

    __tablename__ = "fileextensions"

    name = sa.Column(sa.Text, nullable=False)

    # Children
    file:Mapped[list["Files"]] = relationship(back_populates="fileextension")
    filepage:Mapped[list["FilePages"]] = relationship(back_populates="fileextensions")


class MessageFileExtensions(SQLBaseModel):

    __tablename__ = "messagefileextensions"

    name = sa.Column(sa.Text, nullable=False)

    # Children
    messagefile:Mapped[list["MessageFiles"]] = relationship(back_populates="messagefileextension")


class Files(SQLBaseModel):

    __tablename__ = "files"

    assistant_id = sa.Column(sa.Integer, sa.ForeignKey(Assistants.id), nullable=False)
    extension_id = sa.Column(sa.Integer, sa.ForeignKey(FileExtensions.id), nullable=False)

    filename = sa.Column(sa.Text, nullable=False)
    save_name = sa.Column(sa.Text, nullable=False)
    total_page_num = sa.Column(sa.Integer, nullable=False)
    analysis_key = sa.Column(sa.Text, nullable=True, default=None)

    mongodb_id = sa.Column(sa.Text, default=None)

    # Parents
    assistant:Mapped["Assistants"] = relationship(back_populates="file")
    fileextension:Mapped["FileExtensions"] = relationship(back_populates="file")
    # Children
    filepage:Mapped[list["FilePages"]] = relationship(back_populates="file")



class FilePages(SQLBaseModel):

    __tablename__ = "filepages"

    assistant_id = sa.Column(sa.Integer, sa.ForeignKey(Assistants.id), nullable=False)
    extension_id = sa.Column(sa.Integer, sa.ForeignKey(FileExtensions.id), nullable=False)
    file_id = sa.Column(sa.Integer, sa.ForeignKey(Files.id), nullable=False)

    text_content = sa.Column(sa.Text, nullable = False)
    page_num = sa.Column(sa.Integer, nullable=False)
    total_page_num = sa.Column(sa.Integer, nullable=False)
    analysis_key = sa.Column(sa.Text, nullable=True, default=None)

    # Parents
    assistant:Mapped["Assistants"] = relationship(back_populates="filepage")
    fileextensions:Mapped["FileExtensions"] = relationship(back_populates="filepage")
    file:Mapped["Files"] = relationship(back_populates="filepage")
