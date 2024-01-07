from flask import Flask, render_template
import pandas as pd
import sqlite3

app = Flask(__name__)

# Route to display DataFrame data
@app.route('/')
def display_data():
    # Connect to SQLite database and retrieve data into a DataFrame
    conn = sqlite3.connect('california2.db')  # Replace with your database path
    query = 'SELECT * FROM California'  # Replace with your SQL query
    df = pd.read_sql_query(query, conn)    
    conn.close()

    #remove duplicate variables:
    df = df.drop_duplicates()
   
    # Render DataFrame in HTML format using Pandas' to_html() method
    data_html = df.to_html(index=False)  # Set index=False to not display DataFrame index

    # Pass DataFrame HTML representation to the template
    return render_template('index.html', table=data_html)

# #Create a df for total amount of evs per city:
# # Function to fetch total count of values in a column and create a DataFrame
# def fetch_total_count():
#     conn = sqlite3.connect('california2.db')  # Replace with your database path
#     query = 'SELECT COUNT(*) AS total_count FROM california'  # Replace with your SQL query
#     cursor = conn.cursor()
#     cursor.execute(query)
#     total_count = cursor.fetchone()[0]
#     conn.close()

#     # Create DataFrame from the total count data
#     df_total_count = pd.DataFrame({'Total_Count': [total_count]})
#     return df_total_count

# # Route to display DataFrame data and total count
# @app.route('/')
# def display_data():
#     # Connect to SQLite database and retrieve data into a DataFrame
#     conn = sqlite3.connect('california2.db')  # Replace with your database path
#     query = 'SELECT * FROM California'  # Replace with your SQL query
#     df_from_db = pd.read_sql_query(query, conn)
#     conn.close()

#     # Remove duplicate values from the fetched DataFrame
#     df_from_db = df_from_db.drop_duplicates()

#     # Fetch the total count of values in the column
#     df_total_count = fetch_total_count()

#     # Render DataFrame in HTML format using Pandas' to_html() method
#     data_html_from_db = df_from_db.to_html(index=False)  # Set index=False to not display DataFrame index
#     data_html_total_count = df_total_count.to_html(index=False)

#     # Pass DataFrame HTML representations to the template
#     return render_template('index.html', data_html_from_db=data_html_from_db, data_html_total_count=data_html_total_count)


if __name__ == '__main__':
    app.run(debug=True)
