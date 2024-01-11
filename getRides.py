import json
from Ride import Ride
from datetime import datetime


# Função para carregar boleias de um ficheiro
def load_rides_from_file(filename):
    try:
        with open(filename, 'r') as f:
            if f.read(1):  # Verifica se o primeiro caractere do ficheiro é vazio
                f.seek(0)  # Volta para o início do arquivo
                return json.load(f)  # Retorna os dados JSON carregados
            else:
                return []  # Retorna uma lista vazia se o ficheiro estiver vazio
    except FileNotFoundError:
        return []   # Retorna uma lista vazia se o ficheiro não existir
    except json.JSONDecodeError:
        return []  # Retorna uma lista vazia se o ficheiro não contiver JSON válido

# Função para salvar boleias no ficheiro
def save_rides_to_file(rides, filename):
    with open(filename, 'w') as f:
        # assuming rides is a list of dicts that do not have a serialize() method
        json.dump(rides, f, indent=4)

# Função para salvar boleias na memória
def save_rides_in_memory(docs, filename):

    rides_to_save = []

    for doc in docs:
        doc_data = doc.to_dict()
        new_ride = Ride(
            destination=doc_data.get('destination'),
            info=doc_data.get('info'),
            license=doc_data.get('license'),
            origin=doc_data.get('origin'),
            origin_lat=doc_data.get('originLat'),
            origin_lon=doc_data.get('originLon'),
            provider=doc_data.get('provider'),
            ride_capacity=doc_data.get('rideCapacity'),
            ride_passengers=doc_data.get('ridePassangers'),
            state=doc_data.get('state'),
            time=doc_data.get('time'),
            id=doc.id
        )
        rides_to_save.append(new_ride)

    rides_to_save_dicts = [ride.to_dict() for ride in rides_to_save]
    
    # Save the list of ride dicts to file
    save_rides_to_file(rides_to_save_dicts, filename)

# Função para atualizar boleias na memória
def update_rides_in_memory(docs, filename):
    # Carrega as boleias existentes do arquivo
    existing_rides = load_rides_from_file(filename)
    #print(existing_rides)
    existing_ids = {ride['id'] for ride in existing_rides}
    #print(existing_ids)

    rides_to_save = []

    for doc in docs:
        doc_data = doc.to_dict()
        ride_id = doc.id
        # Verifica se a boleia não está já na memória
        if ride_id not in existing_ids:
            # Cria um novo objeto Ride com os dados do documento e o serializa
            new_ride = Ride(
                destination=doc_data.get('destination'),
                info=doc_data.get('info'),
                license=doc_data.get('license'),
                origin=doc_data.get('origin'),
                origin_lat=doc_data.get('originLat'),
                origin_lon=doc_data.get('originLon'),
                provider=doc_data.get('provider'),
                ride_capacity=doc_data.get('rideCapacity'),
                ride_passengers=doc_data.get('ridePassangers'),
                state=doc_data.get('state'),
                time=doc_data.get('time'),
                id=doc.id
            )
            rides_to_save.append(new_ride)

    # # Se encontrou novas boleias, adiciona-as às existentes e salva-se no ficheiro
    #print(rides_to_save)

    if rides_to_save:
        rides_to_save_dicts = [ride.to_dict() for ride in rides_to_save]
        new_rides = existing_rides + rides_to_save_dicts
        save_rides_to_file(new_rides, filename)

# Segunda versão da função de cima
def update_rides_in_memory_all_atr(rides_collection, filename):
    docs = rides_collection.stream()

    rides_to_save = []

    for doc in docs:
        doc_data = doc.to_dict()
        ride_id = doc.id

        new_ride = Ride(
            destination=doc_data.get('destination'),
            info=doc_data.get('info'),
            license=doc_data.get('license'),
            origin=doc_data.get('origin'),
            origin_lat=doc_data.get('originLat'),
            origin_lon=doc_data.get('originLon'),
            provider=doc_data.get('provider'),
            ride_capacity=doc_data.get('rideCapacity'),
            ride_passengers=doc_data.get('ridePassangers'),
            state=doc_data.get('state'),
            time=doc_data.get('time'),
            id=doc.id
        )
        rides_to_save.append(new_ride)

    # Convert the new rides to dicts
    new_rides_dicts = [ride.to_dict() for ride in rides_to_save]

    # Save the updated rides to the file
    save_rides_to_file(new_rides_dicts, filename)




# Função para verificar correspondências entre passageiros e criadores de boleias
def check_for_matches(ride_list, id_passenger, id_provider):

    today_str = datetime.now().strftime("%d/%m/%Y")
    for ride in ride_list:

        ride_date_str = ride['time'].split(' ')[0]
        print(ride_date_str)
        # Se a data da boleia não for hoje, continua para a próxima iteração
        # Verifica se o ID do fornecedor atual corresponde ao criador da boleia dado

        if ride['provider'] == id_provider:
            print(ride['id'])
            if ride_date_str == today_str:
            # Verifica se o ID do passageiro corresponde a algum na lista
                if id_passenger in ride['ride_passengers']:
                    return 1  # Match found
    return -1  # No match found