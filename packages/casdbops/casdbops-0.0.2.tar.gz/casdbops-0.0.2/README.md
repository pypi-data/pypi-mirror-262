# casdbops: A Streamlined Python Library for Cassandra on AstraDB

## **Introduction**
casdbops is a user-friendly Python library designed to simplify interacting with Cassandra databases hosted on AstraDB, a cloud-based database service from DataStax. It streamlines common database operations, making it easier for developers to work with Cassandra without getting bogged down in low-level details.

#### **What can you do with casdbops?**

- #### **Effortless Database Management:**
  - Create and manage Cassandra databases on AstraDB with ease.
  - Provision databases programmatically as needed within your applications.
- #### **Seamless Data Interaction:**
  - Connect to existing databases using their API endpoints.
  - Create collections (tables) within your databases to organize data.
  - Insert data from CSV or Excel files into your collections for efficient storage.
  - Retrieve data from collections as pandas DataFrames for further analysis or manipulation.

#### **Benefits of using casdbops:**

- **Simplified Development:** Abstracted complexities of Cassandra interaction, allowing you to focus on your application logic.
- **Improved Efficiency:** Streamlined database operations lead to faster development and execution times.
- **Enhanced Readability:** Pythonic code with clear method names promotes code maintainability and comprehension.
- **Reduced Boilerplate:** Less code required for common tasks, minimizing redundancy and error potential.

#### **Who is casdbops for?**

- Python developers who need to interact with Cassandra databases on AstraDB.
- Data engineers and data scientists seeking a convenient way to manage and manipulate Cassandra data.
- Backend developers building applications that rely on Cassandra for persistent storage.

By leveraging casdbops, you can significantly streamline your Cassandra development experience on AstraDB, allowing you to focus on building innovative and high-performing applications.

## **Installation**

Install casdbops using pip:

```bash
pip install casdbops
```

## **Prerequisites**
Before using casdbops, you'll need an AstraDB account. Here's how to set one up:

- Visit https://www.datastax.com/products/datastax-astra.
- Create a free account.
- Create a database and note down the API endpoint and keyspace name.
- Generate an API token (select "Organization Admin" from the dropdown).


## **Usage**

### **Import the library:**

``` Python
from casdbops.cassandra_crud import cassandra_operation
```

### **Create a casdbops object:**
Provide your AstraDB API token as an argument:

```Python
obj = cassandra_operation("AstraCS:YOUR_CLIENT_ID:YOUR_TOKEN")
# Replace YOUR_CLIENT_ID and YOUR_TOKEN with your actual values.
```

### **Database Connection**

>Note:-  casdbops offers two ways to connect to a database:

1. ### Manual API Endpoint:
If you already have a database created, provide its API endpoint directly:

```Python
con_obj = obj.connect_to_database(api_endpoint="[https://your-database-endpoint.apps.astra.datastax.com](https://your-database-endpoint.apps.astra.datastax.com)")
```
2. ### Automatic Creation and Connection:
If you want to create a new database and connect to it seamlessly, provide your password along with the token:


```Python
con_obj = obj.create_database(
    database_name="your_database_name",
    passwd="your_database_password",
    connect_to_same_database=True # Automatically connects to the created database
)  
```

### **Creating Collections**

Use the `create_collection` method to create a collection within your database:

```Python
collection_obj = obj.create_collection("your_collection_name")
```

### **Inserting Data into the Collection**

Pass the path to your CSV or Excel dataset to the `insert_into_collection` method:

```Python
obj.insert_into_collection("path/to/your/dataset.csv")
# or
obj.insert_into_collection("path/to/your/dataset.xlsx")
```

### **Fetching Data from the Collection**

The `Fetch_data_from_collection` method retrieves data as a pandas DataFrame:

```Python
df = obj.Fetch_data_from_collection()
```

### **Code Prompts**

This section offers interactive code prompts to help you experiment with the library and explore its functionalities:

- ### Prompt 1: Connecting to an Existing Database

```Python
# Replace with your AstraDB API token
token = "YOUR_CLIENT_ID:YOUR_TOKEN"

# Replace with your database API endpoint
api_endpoint = "[https://your-database-endpoint.apps.astra.datastax.com](https://your-database-endpoint.apps.astra.datastax.com)"

from casdbops.cassandra_crud import cassandra_operation

# Create a casdbops object
obj = cassandra_operation(token)

# Connect to the database
try:
    con_obj = obj.connect_to_database(api_endpoint=api_endpoint)
    print("Successfully connected to database!")
except Exception as e:
    print("Connection error:", e)
```

- ### Prompt 2: Creating a New Database and Collection

```python
# Replace with your AstraDB API token
token = "YOUR_CLIENT_ID:YOUR_TOKEN"

from casdbops.cassandra_crud import cassandra_operation

# Create a casdbops object
obj = cassandra_operation(token)

# Create a new database (adjust name as needed)
try:
    con_obj = obj.create_database(
        database_name="my_new_database",
        passwd="your_strong_password",
        connect_to_same_database=True
        )
    print("Database created successfully!")
except Exception as e:
    print("Database creation error:", e)

# Create a collection within the new database
collection_obj = obj.create_collection("my_collection")
print("Collection created:", collection_obj.name)
``` 


### **Explanation:**

1.  **Replace placeholders** : Update `YOUR_CLIENT_ID:YOUR_TOKEN` with your AstraDB API token and `https://your-database-endpoint.apps.astra.datastax.com` with your database's API endpoint.
2. **Import necessary modules** : Include `cassandra_operation` from `casdbops`.
3. **Create a casdbops object** : Pass your `token` as an argument.
4. **Connect to the database** : Use `connect_to_database` with the API endpoint.
5. **Error handling** : Wrap the connection logic in a `try-except` block for graceful error handling.

