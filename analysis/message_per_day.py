import psycopg2
import matplotlib.pyplot as plt
from datetime import date, timedelta


from dotenv import load_dotenv
import os

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
# Database connection parameters
db_params = {
    'host': DB_HOST,
    'database': DB_NAME,
    'user': DB_USERNAME,
    'password': DB_PASSWORD,
}

# Connect to the database
connection = psycopg2.connect(**db_params)
cursor = connection.cursor()

# Date range for the past month
end_date = date.today()
start_date = end_date - timedelta(days=30)

# Execute SQL query to count message records per day
query = """
    SELECT DATE(create_on), COUNT(*) 
    FROM public.message
    WHERE DATE(create_on) BETWEEN %s AND %s
    GROUP BY DATE(create_on)
    ORDER BY DATE(create_on);
"""
cursor.execute(query, (start_date, end_date))
results = cursor.fetchall()

# Close the database connection
cursor.close()
connection.close()

# Extract dates and counts from query results
dates = [row[0] for row in results]
counts = [row[1] for row in results]

# Create a bar plot to visualize the data
plt.figure(figsize=(12, 6))
plt.bar(dates, counts)
plt.title('Message Records per Day for the Past Month')
plt.xlabel('Date')
plt.ylabel('Message Count')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot as a PNG file on the server
plt.savefig('/root/plot.png', format='png')

# Close the plot
plt.close()
