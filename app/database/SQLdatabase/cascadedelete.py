import datetime
from typing import Union
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect

from app.database.SQLdatabase.tables.base import SQLBaseModel, SessionLocal
from app.database.SQLdatabase.sqldb import SQLBaseModel, SessionLocal, FilePages, Files, Assistants, Threads
from app.utils.openai import OpenAIer


def get_current_time(now:Union[datetime.datetime,None]) -> datetime.datetime:
    if now==None:
        now = datetime.datetime.utcnow()
    return now


def cascade_soft_delete(table:SQLBaseModel, now:Union[datetime.datetime,None]=None, db:Session=None):
    check = False
    if db==None:
        db = SessionLocal()
        check=True

    if isinstance(table, Assistants):
        if hasattr(table,'analysis_key'):
            if table.analysis_key:
                OpenAIer.assistant_delete(table)

    now = get_current_time(now)

    table.deleted=now

    child_tablenames : list[str] = [c.key for c in inspect(table).mapper.relationships if c.direction.value == 1]

    for child_tablename in child_tablenames:
        child_tables = getattr(table,child_tablename)

        if isinstance(child_tables, list):
            for child_table in child_tables:
                if not type(child_table)==type(None):

                    if isinstance(table, Assistants):

                        if isinstance(child_table, Files):
                            if hasattr(child_table,'analysis_key'):
                                if child_table.analysis_key:
                                    OpenAIer.file_delete(child_table, table)

                        elif isinstance(child_table, FilePages):
                            if hasattr(child_table,'analysis_key'):
                                if child_table.analysis_key:
                                    OpenAIer.file_delete(child_table, table)

                        elif isinstance(child_table, Threads):
                            if hasattr(child_table,'analysis_key'):
                                if child_table.analysis_key:
                                    OpenAIer.thread_delete(child_table)

                    cascade_soft_delete(child_table, now, db)

        else:
            if not type(child_tables)==type(None):
                cascade_soft_delete(child_tables, now, db)

    if check:
        db.commit()
