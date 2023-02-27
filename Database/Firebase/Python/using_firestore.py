from Database.Firebase.Python.firestore_config import db

# Get a reference to the "users" collection
users_ref = db.collection("users")

# Add a new document to the "users" collection
users_ref.document("user1").set({
    "name": "John Doe",
    "email": "john.doe@example.com",
    "age": 30
})

# You can also update an existing document by using the update() method
# Update an existing document in the "users" collection
users_ref.document("user1").update({
    "age": 31
})
