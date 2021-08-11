import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker


def connect_db(db_path: str):
    engine = sa.create_engine(
        'sqlite:///' + db_path,
        echo=True
    )
    session = sessionmaker(bind=engine)()
    connection = engine.connect()
    return session, connection
