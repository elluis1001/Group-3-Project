# Group-3-Project

# Electric Vehicle Charging Stations

We obatined electric vehicle charging station data from https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/all/ via API and used it to create a SQLite database, a Flask API, and a web page with a variety of maps and graphs.

## Team Members
- Luis Rivera
- Beauty Simora 
- Felix Egwuagu
- Steven Miller
- Preeti Wadhwa


## Data
Our data was collected from https://developer.nrel.gov (GET /api/alt-fuel-stations/v1) for all electric charging locations in the United States. The API had data for all alternate fueling locations in US and Canada. The API query was filtered for Electric charging locations in United States. The data was collected for station counts and fields station record fields. Charging locations by State were pulled from the field station record for selected attributes. Based on the states with highest number of charging locations, the data was filtered for the State of CA. The data was then cleaned using Python and Pandas the exported to CSV and JSON files. The code to do this can be found in xxx.ipynb file. It can be pulled with an API key from nrel.gov. The API key for this code is stored in `api_keys.py`.


NREL is a national laboratory of the U.S. Department of Energy. The NREL Data Catalog is where descriptive information (i.e., metadata) is maintained about public data resulting from federally funded research conducted by the National Renewable Energy Laboratory (NREL) researchers and analysts. Due to various sources, the data is likely to have some inaccuracies due to inconsistent data entry or missing data.

## DataBase
A SQLite database was created using [`ev_station.db`] and the CSV files in `data-query`folder to hold the charging station data along with field atrributes data.

Steps to Use:
1. Run the `CREATE TABLE` connections and queries from [`ev_station.db`]
2. In SQLite, use the SQl command to populate the data to the correct tables
    - import `ev_station.db` 



## Flask API
A Flask API was created to showcase retrieving our data from an API. 

Steps to Use:
1. First create the SQLite database using [`Create_sqlite.py`]
2. Run the flask app with [`flask_app.py`](/flaskAPI/flask_app.py)

    

## Website



# Ethical considerations 
In the project, ethical considerations take center stage, emphasizing a commitment to safeguarding user privacy and ensuring responsible data practices. Anonymization of sensitive information is paramount, and the project prioritizes aggregated insights over individual data points. Informed consent is respected, and users are provided with clear explanations of data usage. Acknowledging potential biases, the project aims for transparency, documenting sources, methodologies, and any external code. Security measures are highlighted to protect data integrity, and a dedication to addressing community impact and feedback fosters an accountable and open approach. Continuous evaluation ensures ongoing ethical standards improvement throughout the project's lifecycle.

## Packages and Libraries
- Python
    - Pandas
    - Requests
    - SQLAlchemy
    - Flask
    - Matplotlib
- JavaScript
    - D3.js
    - Plotly
    - Leaflet
- SQLite