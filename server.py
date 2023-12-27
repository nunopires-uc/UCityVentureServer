import firebase_admin
from firebase_admin import credentials, firestore
import threading
import time
from getRides import update_rides_in_memory, load_rides_from_file, save_rides_in_memory, check_for_matches

# Initialize the Firebase admin SDK with your credentials
cred = credentials.Certificate("ucityventure-firebase-adminsdk-ieyv3-2d19b3f652.json")
firebase_admin.initialize_app(cred)


filename = 'rides.json'
# Call the function to load rides from the file
rides_in_memory = load_rides_from_file(filename)


'''
# Now rides_in_memory contains a list of ride dictionaries
for ride_dict in rides_in_memory:
    print(ride_dict)  # This will print out each ride's information as a dictionary
'''
# Transaction function

def transaction_update(doc_ref, token, updated_token):
   # Fetch the entire 'queue' array
   doc = doc_ref.get()
   queue = doc.get('queue')
   
   if queue: # Check if the queue is not empty
       # Find the index of the old token
       index = queue.index(token)

       # Replace the old token with the new one at the same position
       queue[index] = updated_token

       # Overwrite the entire 'queue' array in Firestore
       doc_ref.update({'queue': queue})



# Create a Firestore client
db = firestore.client()


rides_collection = db.collection('rides')
# Stream the documents in the 'rides' collection
docs = rides_collection.stream()
if(len(rides_in_memory) == 0):
    save_rides_in_memory(docs, filename)
    rides_in_memory = load_rides_from_file(filename)


# Thread synchronization event
callback_done = threading.Event()

def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(f"Received document snapshot: {doc.id}")
        # Access field_queue from the document, assuming field_queue is the correct field name
        field_queue = doc.get('queue')
        if field_queue:  # Check if the field_queue is not empty
            token = field_queue[-1]  # Access the last entry of the array list
            # Access the PIN field of the last entry
            print(f"Last entry: {token}")  # Print the last entry
            PIN = token.split("+")[0]
            ID_PASSENGER = token.split("+")[1]
            ID_PROVIDER = token.split("+")[2]
            STATUS = token.split("+")[3]
            if(STATUS == "0"):
                rides_list = load_rides_from_file('rides.json')
                status = check_for_matches(rides_list, ID_PASSENGER, ID_PROVIDER)
                
                if(status == 1):
                    print("Match found")
                elif(status == -1):
                    print("Match not found")

                new_token = PIN + "+" + ID_PASSENGER + "+" + ID_PROVIDER + "+" + str(status)

                transaction_update(doc_ref, token, new_token)
        else:
            print("field_queue is empty or does not exist.")
    callback_done.set()


def on_snapshotRides(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        rides_collection = db.collection('rides')

        # Stream the documents in the 'rides' collection
        docs = rides_collection.stream()
        
        print(f"Received document snapshot: {doc.id}")
        update_rides_in_memory(docs, filename)
    callback_done.set()


# Reference to the specific document in the 'transactions' collection
doc_ref = db.collection("transactions").document("MLRkVMuqJElVYxbD9jxP")

doc_refrides = db.collection("transactions").document("num_rides")

# Start listening to the document
doc_watch = doc_ref.on_snapshot(on_snapshot)
doc_watchrides = doc_refrides.on_snapshot(on_snapshotRides)

# Keep the main thread running to listen for changes until the process is terminated
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass  # Allow a keyboard interrupt (Ctrl+C) to cleanly exit the loop
