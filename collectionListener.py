import firebase_admin
from firebase_admin import firestore, credentials
import time
import ScanConfirmation

cred = credentials.Certificate("ucityventure-firebase-adminsdk-ieyv3-2d19b3f652.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Define the callback function
def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED':
            print(f'New document: {change.document.id}')
            doc = change.document.to_dict()  # Convert the document to a dictionary
            scan_confirmation = ScanConfirmation()  # Create a new ScanConfirmation object
            scan_confirmation.setPIN(doc.get('PIN'))  # Set the attributes using the document data
            scan_confirmation.setProviderID(doc.get('ProviderID'))
            scan_confirmation.setUserID(doc.get('UserID'))
            scan_confirmation.setStatus(doc.get('Status'))
            print(scan_confirmation)

# Specify the collection you want to listen to
col_query = db.collection('myqrconfirmations')

# Attach the listener to the collection
query_watch = col_query.on_snapshot(on_snapshot)

# Keep the script running
while True:
    time.sleep(1)
