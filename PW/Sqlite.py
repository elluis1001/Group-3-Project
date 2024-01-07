import pandas as pd
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class CAStations(Base):
    __tablename__ = 'Station_data'
    
    id = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.String, nullable=True)
    street_address = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    state = db.Column(db.String, nullable=True)
    zip = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    access_code = db.Column(db.String, nullable=True)
    ev_network = db.Column(db.String, nullable=True)
    ev_connector_types = db.Column(db.String, nullable=True)
    status_code = db.Column(db.String, nullable=True)
    ev_pricing = db.Column(db.String, nullable=True)
    geocode_status = db.Column(db.String, nullable=True)



class SQLiteManager:
    def __init__(self, database_path):
        self.database_path = database_path
        self.engine = create_engine(f"sqlite:///{self.database_path}")
        self.session = sessionmaker(bind=self.engine)()

    def create_database(self):
        Base.metadata.create_all(self.engine)

    def create_table(self):
        pass  # Table creation is handled by the mapped class definition

    def import_csv_to_table(self, csv_path):
        csv_data = pd.read_csv(csv_path)
        csv_data.to_sql("reduced_data", self.engine, if_exists='append', index=False)

    def execute_query(self, query):
        self.session.execute(query)
        self.session.commit()

    def close_connection(self):
        self.session.close()


# Usage example
database_path = "data_query/ev_stations.sqlite"
csv_path = "data_query/fuel_stations_ca.csv"

manager = SQLiteManager(database_path)
manager.create_database()
manager.import_csv_to_table(csv_path)

# Example query
# results = manager.session.query(ReducedData).filter_by(Town='YourTown').all()
# for result in results:
#     print(result.Title, result.AddressLine1)

manager.close_connection()