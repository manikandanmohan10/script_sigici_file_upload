import psycopg2


host = "54.37.65.120"  # e.g., 'localhost', or the IP address of your EC2 instance
port = "5432"  # default PostgreSQL port
database = "sigici"
user = "postgres"
password = "A!6~4zm1Rl;5"

# Establishing the connection
try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        dbname=database,
        user=user,
        password=password
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Test the connection by running a query
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print(f"Connected to PostgreSQL database, version: {db_version[0]}")

except Exception as error:
    print(f"Error: {error}")
finally:
    # Close the cursor and the connection if it was successful
    if connection:
        cursor.close()
        connection.close()
