from app.database.SQLdatabase.tables.access import AccessTypes
from app.database.SQLdatabase.tables.assistants import Assistants, AssistantAccess, AssistantTypes, GlobalAssistantAccess, SharedAssistantAccess, AssistantOwners, CustomAssistant
from app.database.SQLdatabase.tables.base import SessionLocal, SQLBaseModel, get_table_dict, Base, engine
from app.database.SQLdatabase.tables.files import FileExtensions, FilePages, Files, MessageFileExtensions
from app.database.SQLdatabase.tables.users import Users, UserAccess
from app.database.SQLdatabase.tables.threads import Threads, ThreadMessages, MessageTypes, MessageImages, MessageFiles, ThreadOwner, ThreadAccess, ThreadShared, PromptSuggestions
from app.database.SQLdatabase.tables.vector import VectorCollection, VectorEmbedding
from app.database.SQLdatabase.tables.connections import ConnectionOpenAI, ConnectionStatus, ConnectionDB

#from app.database.SQLdatabase.tables.migration import MigrationAssistants, MigrationThreads, MigrationFiles, MigrationMessages
