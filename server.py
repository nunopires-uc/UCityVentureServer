import firebase_admin
from firebase_admin import credentials, firestore
import threading
import time
from getRides import update_rides_in_memory, load_rides_from_file, save_rides_in_memory, check_for_matches, update_rides_in_memory_all_atr
from ScanConfirmation import ScanConfirmation

cred = credentials.Certificate("ucityventure-firebase-adminsdk-ieyv3-2d19b3f652.json")
firebase_admin.initialize_app(cred)


filename = 'rides.json'


# Thread synchronization event
callback_done = threading.Event()

# Create a Firestore client
db = firestore.client()


rides_collection = db.collection('rides')
docs = rides_collection.stream()

print(docs)

save_rides_in_memory(docs, filename)
rides_in_memory = load_rides_from_file(filename)



def on_snapshot(col_snapshot, changes, read_time):
    #
    for change in changes:
        if change.type.name == 'ADDED':
            
            print(f'New document: {change.document.id}')
            doc = change.document.to_dict()  # Convert the document to a dictionary
            scan_confirmation = ScanConfirmation()  # Create a new ScanConfirmation object
            scan_confirmation.setPIN(doc.get('pin'))  # Set the attributes using the document data
            scan_confirmation.setProviderID(doc.get('providerID'))
            scan_confirmation.setUserID(doc.get('userID'))
            scan_confirmation.setStatus(doc.get('status'))

            if(scan_confirmation.getStatus() == "0"):

                rides_list = load_rides_from_file('rides.json')
                print(len(rides_list))

                print(scan_confirmation.getUserID())
                print(scan_confirmation.getProviderID())
                status = check_for_matches(rides_list, scan_confirmation.getUserID(), scan_confirmation.getProviderID())

                if(status == 1):
                    print("Match found")
                elif(status == -1):
                    print("Match not found")

                scan_confirmation.setStatus(status)
                
                doc_ref = db.collection('myqrconfirmations').document(scan_confirmation.getPIN())

                
                doc_ref.update({
                    'status': str(status)
                })
                
            print(scan_confirmation)

    callback_done.set()


def repeat_every_30_seconds():
    threading.Timer(30.0, repeat_every_30_seconds).start()
    print("Updating rides in memory")
    update_rides_in_memory_all_atr(db.collection('rides'), filename)

col_query = db.collection('myqrconfirmations')

query_watch = col_query.on_snapshot(on_snapshot)


def on_snapshotRides(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED':
            print(f'New Ride: {change.document.id}')
            update_rides_in_memory_all_atr(db.collection('rides'), filename)

            

# Specify the collection you want to listen to
col_queryRides = db.collection('rides')

# Attach the listener to the collection
query_watch = col_queryRides.on_snapshot(on_snapshotRides)


repeat_every_30_seconds()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass  # Allow a keyboard interrupt (Ctrl+C) to cleanly exit the loop
