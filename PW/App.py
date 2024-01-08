from flask import Flask, render_template
import pandas as pd
import sqlite3
import folium
from io import BytesIO
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

# Function to fetch unique values from a column along with their counts
def fetch_values_with_counts():
    conn = sqlite3.connect('ev_stations.db')
    cursor = conn.cursor()

    # Replace 'your_column' and 'your_table' with your column and table names
    query = 'SELECT city, COUNT(*) AS counts FROM ev_stations GROUP BY city'

    cursor.execute(query)
    values_counts = cursor.fetchall()  # Fetch unique values with their counts

    conn.close()

    # Create a DataFrame from the fetched values with counts
    df = pd.DataFrame(values_counts, columns=['Value', 'Counts'])
    return df

# Function to fetch city locations from the database
def fetch_city_locations():
    conn = sqlite3.connect('ev_stations.db')  # Replace with your database path
    query = 'SELECT city, latitude, longitude FROM ev_stations GROUP BY city'  # Replace with your SQL query
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Route to display DataFrame data, total count, and a bar graph
@app.route('/')
def display_data():
    df_values_counts = fetch_values_with_counts()

    # Sort DataFrame by counts and select the top 10 cities
    df_top_10 = df_values_counts.nlargest(10, 'Counts')

    # Generate bar graph for top 10 cities using Matplotlib
    plt.figure(figsize=(10, 6))
    plt.bar(df_top_10['Value'], df_top_10['Counts'])
    plt.xlabel('City')
    plt.ylabel('Counts')
    plt.title('Top 10 Cities by Counts')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

    # Save the plot to a bytes object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    # Render DataFrame and bar graph in HTML format using Pandas' to_html() method
    data_html = df_top_10.to_html(index=False)

    # Fetch city locations and create a folium map
    df_city_locations = fetch_city_locations()
    map = folium.Map(location=[37.7749, -122.4194], zoom_start=6)  # Map centered at California

    # Add markers for city locations to the map
    for index, row in df_city_locations.iterrows():
        folium.Marker([row['latitude'], row['longitude']], popup=row['city']).add_to(map)

    # Save the map to an HTML file
    map.save('templates/map.html')

    # Pass DataFrame HTML representation, graph URL, and map HTML representation to the template
    return render_template('index.html', data_html=data_html, graph_url=graph_url, map_html='map.html')

if __name__ == '__main__':
    app.run(debug=True)


