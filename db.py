from pymongo import MongoClient
import os

# Load environment variables
DATABASE_URL = os.getenv('MONGODB_URI', 'mongodb+srv://vigneshselvaa9940:iambatman@cluster0.qlzkf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

# Create a MongoDB client
client = MongoClient(DATABASE_URL)

# Select the database
db = client.healthcare_system

# Define collections
users_collection = db.users
doctors_collection = db.doctors
patients_collection = db.patients

# Ensure collections are initialized
assert users_collection is not None, "Users collection is not initialized"
assert doctors_collection is not None, "Doctors collection is not initialized"
assert patients_collection is not None, "Patients collection is not initialized"
