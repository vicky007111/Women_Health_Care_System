# setup_database.py
from pymongo import MongoClient
import os

# Load environment variables
DATABASE_URL = os.getenv('MONGODB_URI', 'mongodb+srv://vigneshselvaa9940:wPboi3avrKoZtjaE@cluster0.qlzkf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

# Create a MongoDB client
client = MongoClient(DATABASE_URL)

# Select the database
db = client.healthcare_system

# Define collections
users_collection = db.users
doctors_collection = db.doctors
patients_collection = db.patients
