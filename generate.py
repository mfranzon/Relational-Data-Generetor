#from sqlalchemy import MetaData
#from sqlmodel import create_engine 


# REAL CASE with connection and getting metadata
# connect = create_engine()
# metadata = Metadata(bind=connect)
# metadata.reflect()
# metadata[table].to_dict() -> implementing a function to convert sqlalchemy object into sdv.dataset.metadata


# MOCK DB connection passing the metadat and data as variable

def mock_db(metadata, tables, num_rows=10):
    from sdv.relational import HMA1

    model = HMA1(metadata)
    model.fit(tables)
    new_data = model.sample(num_rows=num_rows)
    return new_data

