import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize Firebase app with credentials
cred = credentials.Certificate('/DATA/data/Database/Firebase/clovertest-a103f-firebase-adminsdk-ru8ro-896bc5ae46.json')
firebase_admin.initialize_app(cred)

# Get a reference to the Firestore database
db = firestore.client()