import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector

from app.database.SQLdatabase.tables.base import Base


class VectorCollection(Base):

    __tablename__ = "langchain_pg_collection"

    name = sa.Column(sa.VARCHAR, nullable=True)
    cmetadata = sa.Column(postgresql.JSON(astext_type=sa.Text), nullable=True)
    uuid = sa.Column(sa.UUID, nullable=False)

    __table_args__ = (
        sa.PrimaryKeyConstraint('uuid', name='langchain_pg_collection_pkey'),
        {"postgresql_ignore_search_path": False}
    )


class VectorEmbedding(Base):

    __tablename__ = "langchain_pg_embedding"

    collection_id = sa.Column(sa.UUID, nullable=True)
    embedding = sa.Column(Vector, nullable=True)
    document = sa.Column(sa.VARCHAR, nullable=True)
    cmetadata = sa.Column(postgresql.JSONB(astext_type=sa.Text), nullable=True)
    custom_id = sa.Column(sa.VARCHAR, nullable=True)
    uuid = sa.Column(sa.UUID, nullable=False)

    __table_args__ = (
        sa.Index('ix_cmetadata_gin', 'cmetadata', unique=False, postgresql_using='gin'),
        sa.ForeignKeyConstraint(
            ['collection_id'],
            [VectorCollection.uuid],
            name='langchain_pg_embedding_collection_id_fkey',
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('uuid', name='langchain_pg_embedding_pkey')
    )
