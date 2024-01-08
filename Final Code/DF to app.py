from flask import Flask, render_template
import pandas as pd
import sqlite3
from io import BytesIO
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

# Function to fetch unique values from a column along with their counts
def fetch_values_with_counts():
    conn = sqlite3.connect('california2.db')  # Replace with your database path
    cursor = conn.cursor()

    query = 'SELECT city, COUNT(*) AS counts FROM California GROUP BY city'
    cursor.execute(query)
    values_counts = cursor.fetchall()  # Fetch unique values with their counts
    conn.close()

    # Create a DataFrame from the fetched values with counts
    df = pd.DataFrame(values_counts, columns=['City', 'EV Stations'])
    return df

# Function to fetch the types of EV Stations:
def fetch_ev_types():
    conn = sqlite3.connect('california2.db')
    query = 'SELECT owner_type_code, COUNT(*) AS counts FROM California GROUP BY owner_type_code'
    df_2 = pd.read_sql_query(query, conn)
    conn.close()
    return df_2

# Function to fetch the types of EV Stations in Los Angeles:
# def fetch_ev_types_LA():
#     conn = sqlite3.connect('california2.db')
#     query = '''
#         SELECT 
#             owner_type_code AS ev_type, 
#             COUNT(*) AS count
#         FROM 
#             California
#         WHERE 
#             city = 'Los Angeles'
#         GROUP BY 
#             owner_type_code
#     '''                
#     df_3 = pd.read_sql_query(query, conn)
#     conn.close()
#     return df_3

# Route to display the data, bar graph, pie chart, and dictionary
@app.route('/')
def display_data():
    df_values_counts = fetch_values_with_counts()
    df_ev_types = fetch_ev_types()

    # Sort DataFrame by counts and select the top 10 cities
    df_top_10 = df_values_counts.nlargest(10, 'EV Stations')

    # Display LA ev types
    #df_LA_ev = fetch_ev_types_LA
    
    # Generate bar graph for top 10 cities using Matplotlib
    plt.figure(figsize=(20, 10))

    # Bar chart for top 10 cities
    plt.subplot(1, 2, 1)
    plt.bar(df_top_10['City'], df_top_10['EV Stations'], width = 0.5)
    plt.xlabel('City')
    plt.ylabel('EV Stations')
    plt.title('Top 10 Cities by Counts')
    plt.xticks(rotation=45)

    # Pie chart for EV Types distribution
    plt.subplot(1, 2, 2)
    plt.pie(df_ev_types['counts'], labels=df_ev_types['owner_type_code'], autopct='%1.1f%%')
    plt.title('Distribution of EV Types')

    # Save the plots to a bytes object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    # Sample dictionary data
    EV_Dictionary = {
        'FG': 'Federal Government Owned',
        'J': 'Jointly Owned',
        'LG': 'Local/Municipal Government Owned',
        'SG': 'State/Provincial Government Owned',
        'T': 'Utility Owned',
        'P': 'Privately Owned'  # Add 'P' for 'Privately Owned'
    }

    # Create a DataFrame to display the dictionary
    df_EV_Dictionary = pd.DataFrame(list(EV_Dictionary.items()), columns=['Code', 'Description'])

    return render_template(
        'index.html',
        data_html=df_top_10.to_html(index=False),
        #df_LA_ev=df_LA_ev.to_html(index=False),  # Make sure 'df_LA_ev' is the correct variable name
        df_EV_Dictionary=df_EV_Dictionary.to_html(index=False),
        ev_types=df_ev_types.to_html(index=False),
        graph_url=graph_url
    )


if __name__ == '__main__':
    app.run(debug=True)







