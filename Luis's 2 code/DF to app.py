from flask import Flask, render_template
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Function to fetch unique values from a column along with their counts
def fetch_values_with_counts():
    conn = sqlite3.connect('california2.db')  # Replace with your database path
    cursor = conn.cursor()

    # Replace 'your_column' and 'your_table' with your column and table names
    query = 'SELECT city, COUNT(*) AS counts FROM California GROUP BY city'

    cursor.execute(query)
    values_counts = cursor.fetchall()  # Fetch unique values with their counts

    conn.close()

    # Create a DataFrame from the fetched values with counts
    df = pd.DataFrame(values_counts, columns=['Value', 'Counts'])
    return df

# Route to display DataFrame with values and their counts along with a bar graph of top 10 cities
@app.route('/')
def display_values_with_counts():
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

    # Pass DataFrame HTML representation and graph URL to the template
    return render_template('index.html', data_html=data_html, graph_url=graph_url)

if __name__ == '__main__':
    app.run(debug=True)

