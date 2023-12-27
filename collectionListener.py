import firebase_admin
from firebase_admin import firestore, credentials
import time

cred = credentials.Certificate("ucityventure-firebase-adminsdk-ieyv3-2d19b3f652.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Define the callback function
def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED':
            print(f'New document: {change.document.id}')

# Specify the collection you want to listen to
col_query = db.collection('rides')

# Attach the listener to the collection
query_watch = col_query.on_snapshot(on_snapshot)

# Keep the script running
while True:
    time.sleep(1)
