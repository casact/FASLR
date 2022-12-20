# import sqlalchemy as sa
#
# from faslr import schema
# from faslr.schema import UserTable, CountryTable, LocationTable
# from sqlalchemy.orm import sessionmaker
#
# engine = sa.create_engine(
#     'sqlite:///test_schema.db',
#     echo=True
# )
#
# schema.Base.metadata.create_all(engine)
# session = sessionmaker(bind=engine)()
# connection = engine.connect()
#
# country_text = 'USA'
# country_query = session.query(CountryTable).filter(CountryTable.country_name == country_text)
#
# session.query(LocationTable)
# session.commit()
#
# connection.close()
