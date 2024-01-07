from flask import Flask, jsonify, request
import sqlite3
import pandas as pd

app = Flask(__name__)

# Define the path to your SQLite database file
database_path = "ev_stations.db"

# Define the columns that can be used for filtering
valid_columns = [
    "station_name",
    "city",
    "state",
    "zip",
    "latitude",
    "longitude",
    "access_code",
    "ev_network",
    "ev_connector_types",
    "status_code",
    "ev_pricing",
    "geocode_status",
]

@app.route('/')
def home():
    return "Welcome to the Fuel Stations API!"

@app.route('/fuel_stations', methods=['GET'])
def get_fuel_stations():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database_path)

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Get the query parameters from the request
        filters = {key: request.args.get(key) for key in request.args if key in valid_columns}

        # Build the SQL query based on the specified filters
        query = f"SELECT * FROM ev_stations WHERE {' AND '.join([f'{key}=?' for key in filters])};" if filters else "SELECT * FROM ev_stations;"

        # Execute the SQL query
        cursor.execute(query, tuple(filters.values()))

        # Fetch the results
        results = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Check if results exist
        if not results:
            return jsonify({"message": "No results found"}), 404

        # Convert the results to a Pandas DataFrame for easy manipulation
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(results, columns=columns)

        # Convert the DataFrame to JSON and return the response
        return jsonify(df.to_dict(orient='records'))

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/fuel_stations/city/Sacramento', methods=['GET'])
def get_fuel_stations_in_sacramento():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(database_path)

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Build the SQL query to get stations in Sacramento, CA
        query = "SELECT * FROM ev_stations WHERE city='Sacramento' AND state='CA';"

        # Execute the SQL query
        cursor.execute(query)

        # Fetch the results
        results = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Check if results exist
        if not results:
            return jsonify({"message": "No results found in Sacramento, CA"}), 404

        # Convert the results to a Pandas DataFrame for easy manipulation
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(results, columns=columns)

        # Convert the DataFrame to JSON and return the response
        return jsonify(df.to_dict(orient='records'))

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
