import pandas as pd
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'

app = Flask(__name__)

# Configure SQLite database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ev_stations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create SQLAlchemy database instance
db = SQLAlchemy(app)

# Define the SQLAlchemy model for the 'ev_stations' table
class FuelStation(db.Model):
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

# Create database tables based on the model
db.create_all()

# Read in JSON data from the file
json_data_path = Path("data_query/fuel_stations_selected_by_CA_0106.json")

if json_data_path.exists():
    with json_data_path.open("r", encoding="utf8") as f:
        fuel_station_data = json.load(f)

    # Check if the necessary data is present in the loaded JSON
    if 'CA' in fuel_station_data:
        # Extract data for California from the loaded JSON
        ca_station_data = fuel_station_data['CA']

        # Create DataFrame
        fuel_station_df = pd.DataFrame(ca_station_data)

        # Clean the DataFrame (Add your DataFrame manipulation code here)

        # ... (remaining code for DataFrame manipulation)

        # Define the path to your SQLite database file
        database_path = Path("ev_stations.db")

        # Connect to the SQLite database
        conn = db.engine.connect()

        # Commit the changes and close the connection
        conn.close()

        print(f"The SQLite database has been created, and the DataFrame has been stored in the 'fuel_stations' table.")
    else:
        print(f"No data available for California in the loaded JSON.")
else:
    print(f"JSON data file not found.")

# Define a route to get all fuel stations
@app.route('/fuel_stations', methods=['GET'])
def get_fuel_stations():
    fuel_stations = FuelStation.query.all()
    fuel_stations_list = []

    for station in fuel_stations:
        fuel_stations_list.append({
            'id': station.id,
            'station_name': station.station_name,
            'street_address': station.street_address,
            'city': station.city,
            'state': station.state,
            'zip': station.zip,
            'latitude': station.latitude,
            'longitude': station.longitude,
            'access_code': station.access_code,
            'ev_network': station.ev_network,
            'ev_connector_types': station.ev_connector_types,
            'status_code': station.status_code,
            'ev_pricing': station.ev_pricing,
            'geocode_status': station.geocode_status
        })

    return jsonify({'fuel_stations': fuel_stations_list})

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
