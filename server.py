import firebase_admin
from firebase_admin import credentials, firestore
import threading
import time
from getRides import load_rides_from_file, save_rides_in_memory, check_for_matches, update_rides_in_memory_all_atr
from ScanConfirmation import ScanConfirmation

#Configura as credenciais para conectar ao Firebase
cred = credentials.Certificate("ucityventure-firebase-adminsdk-ieyv3-2d19b3f652.json")
firebase_admin.initialize_app(cred)

# Define o nome do arquivo onde as boleias serão salvas
filename = 'rides.json'


# Evento de sincronização de threads
callback_done = threading.Event()

# Cria o cliente Firestore
db = firestore.client()

# Obtém a coleção 'rides' do Firestore e faz o streaming dos documentos
rides_collection = db.collection('rides')
docs = rides_collection.stream()

# Imprime o que está guardado
print(docs)


# Salva os documentos em memória com o nome especificado
save_rides_in_memory(docs, filename)

# Carrega as corridas do ficheiro para a memória
rides_in_memory = load_rides_from_file(filename)


# Define a função que será chamada quando houver atualizações na coleção
def on_snapshot(col_snapshot, changes, read_time):
    # Nesta função é analisado se as boleias são validas
    for change in changes:
        # Verifica se o tipo de mudança é ADDED (documento adicionado)
        if change.type.name == 'ADDED':
            # Imprime o ID do novo documento
            print(f'New document: {change.document.id}')
            # Converte o documento para um dicionário
            doc = change.document.to_dict() 

            scan_confirmation = ScanConfirmation() 
            scan_confirmation.setPIN(doc.get('pin'))
            scan_confirmation.setProviderID(doc.get('providerID'))
            scan_confirmation.setUserID(doc.get('userID'))
            scan_confirmation.setStatus(doc.get('status'))

            # Se o estado da boleia ainda não foi mexido
            if(scan_confirmation.getStatus() == "0"):

                rides_list = load_rides_from_file('rides.json')
                print(len(rides_list))

                print(scan_confirmation.getUserID())
                print(scan_confirmation.getProviderID())

                # verifica se o utilizador que pediu a validação pertence à boleia
                status = check_for_matches(rides_list, scan_confirmation.getUserID(), scan_confirmation.getProviderID())

                # caso o utilizador esteja na lista dos que vão usufruir da boleia, o estado é 1, caso contrário é -1
                if(status == 1):
                    print("Match found")
                elif(status == -1):
                    print("Match not found")

                # atualizar o pedido de verificação de boleia com o novo estado

                scan_confirmation.setStatus(status)
                
                doc_ref = db.collection('myqrconfirmations').document(scan_confirmation.getPIN())

                # atualizar no documento
                doc_ref.update({
                    'status': str(status)
                })
                
            print(scan_confirmation)

    callback_done.set()

# A cada 30 segundos salvar em memória as boleias
def repeat_every_30_seconds():
    threading.Timer(30.0, repeat_every_30_seconds).start()
    print("Updating rides in memory")
    update_rides_in_memory_all_atr(db.collection('rides'), filename)

# Cria uma query na coleção 'myqrconfirmations'
col_query = db.collection('myqrconfirmations')
# Inicia a escuta de mudanças na coleção e associa à função on_snapshot
query_watch = col_query.on_snapshot(on_snapshot)

# Sempre que uma boleia é adicionada, atualiza as boleias em memória
def on_snapshotRides(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED':
            print(f'New Ride: {change.document.id}')
            update_rides_in_memory_all_atr(db.collection('rides'), filename)

            

col_queryRides = db.collection('rides')

# Anexa o listener à coleção de boleias
query_watch = col_queryRides.on_snapshot(on_snapshotRides)


repeat_every_30_seconds()

# Tenta executar indefinidamente até que um KeyboardInterrupt ocorra
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass  # Permite que uma interrupção de teclado (Ctrl+C) saia limpa do loop
