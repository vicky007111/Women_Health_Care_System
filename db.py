from pymongo import MongoClient
import os

def setup_database():
    # Load environment variables
    DATABASE_URL = os.getenv('MONGODB_URI', 'mongodb+srv://vigneshselvaa9940:iambatman@cluster0.qlzkf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

    try:
        # Create a MongoDB client
        client = MongoClient(DATABASE_URL)
        
        # Test the connection
        client.server_info()  # Forces a call to the server to check if the connection is successful
        
        # Select the database
        db = client.healthcare_system
        
        # Define collections
        users_collection = db.users
        doctors_collection = db.doctors
        patients_collection = db.patients

        print("Database and collections set up successfully.")
        return users_collection, doctors_collection, patients_collection
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None

# Call the setup function
users_collection, doctors_collection, patients_collection = setup_database()

