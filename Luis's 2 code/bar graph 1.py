from flask import Flask, render_template
import sqlite3
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    # Retrieve data from SQLite database
    conn = sqlite3.connect('california2.db')
    cursor = conn.cursor()
    cursor.execute('SELECT city, y_column FROM your_table')  # Replace with your SQL query
    data = cursor.fetchall()
    conn.close()

    # Process data for plotting
    x_values = [row[0] for row in data]
    y_values = [row[1] for row in data]

    # Create a simple line plot using Matplotlib
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values)
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
    plt.title('Your Plot Title')

    # Convert plot to a base64 encoded image
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    # Render the HTML template with the graph
    return render_template('index.html', graph_url=graph_url)

if __name__ == '__main__':
    app.run(debug=True)
