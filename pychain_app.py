import mysql.connector
import hashlib
import json
from datetime import datetime

# Function to generate hash for each transaction
def generate_hash(transaction):
    transaction_data = f"{transaction['Cr_amount']}-{transaction['Dr_amount']}-{transaction['Description']}-{transaction['Transaction_date']}"
    return hashlib.sha256(transaction_data.encode()).hexdigest()

# Connect to the database
connection = mysql.connector.connect(
    host="localhost",        # Host name (change if not localhost)
    port="3307",             # Port (if applicable)
    user="root",             # Username
    password="",             # Password (leave blank if not set)
    database="bnkms"         # Name of your database
)

# Create a cursor to execute SQL queries
cursor = connection.cursor()

# Specify the table name and fetch data
customer_id = input("Enter Customer ID: ")  # Prompt user for customer ID
table_name = f"passbook_{customer_id}"

query = f"SELECT Cr_amount, Dr_amount, Description, Transaction_date FROM {table_name}"
cursor.execute(query)

# Fetch the data
transactions = cursor.fetchall()

# Prepare the list of transactions with hashes
transaction_list = []
for row in transactions:
    # Ensure that the Transaction_date is correctly parsed (from string to datetime)
    try:
        # If it's a string, convert it to a datetime object using the correct format
        if isinstance(row[3], str):
            transaction_date = datetime.strptime(row[3], '%d/%m/%y %I:%M:%S %p')  # Adjusted format
        else:
            transaction_date = row[3]  # If it's already a datetime object, use it as is

        # Prepare the transaction dictionary
        transaction = {
            "Cr_amount": row[0],
            "Dr_amount": row[1],
            "Description": row[2],
            "Transaction_date": transaction_date.strftime('%Y-%m-%d %H:%M:%S'),  # Format the timestamp
            "hash": generate_hash({
                "Cr_amount": row[0],
                "Dr_amount": row[1],
                "Description": row[2],
                "Transaction_date": transaction_date.strftime('%Y-%m-%d %H:%M:%S')
            })
        }

        transaction_list.append(transaction)

    except Exception as e:
        print(f"Error processing transaction: {e}")
        continue

# Prepare the final output with only transaction details and hashes
output = {
    "transactions": transaction_list
}

# Display the output in JSON format
print(json.dumps(output, indent=2))

# Close the connection
cursor.close()
connection.close()
