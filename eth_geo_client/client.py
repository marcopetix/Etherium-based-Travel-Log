import requests
import pprint
import geo_test
import webbrowser

from  geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="PathFinder")


url = "http://localhost:5000"
op = 0
progress_status = ["START", "TRAVELLING", "END"]


while True:

    op = int(input("\nPremi:\n\n1) per visualizzare gli spostamenti degli utenti\n2) per registrare una nuova posizione\n3) per registrare una posizione manualmente\n4) per mostrare l'interfaccia web\n5) per uscire\n"))

    if op == 1:
        URL = url + "/markers"

        r = requests.get(url = URL)

        data = r.json()

        if(data['data'] != []):
            p = pprint.PrettyPrinter()
            p.pprint(data)
        else:
            print("\nNessuno spostamento è stato ancora registrato sulla blockchain")

    elif op == 2:
        latitude, longitude = geo_test.getLocation()
        print("\nLatitudine: ", latitude)
        print("Longitudine: ", longitude)

        description = input("\nInserisci una descrizione: ")

        progress = input("\n\nPremi: \n\n1) per START\n2) per TRAVELLING,\n3) per END\n")
        progress = progress_status[int(progress) - 1]

        pk = input("\nInserisci la private key: ")

        if progress == "END":

            data = {'longitude': str(longitude),
                    'latitude': str(latitude)}

            URL = url + "/check_arrived"

            r = requests.post(url = URL, json = data)

            response = r.json()

            status = response['status']
        else:
            status = "FALSE"

        data = {'description': description,
                'longitude': str(longitude),
                'latitude': str(latitude),
                'progress':str(progress),
                'status': str(status),
                'private_key': pk}

        URL = url + "/new_marker"
        r = requests.post(url = URL, json = data)

    elif op == 3:
        latitude = input("\nLatitudine: ")
        longitude = input("\nLongitudine: ")

        description = input("\nInserisci una descrizione: ")

        progress = input("\n\nPremi: \n\n1) per START\n2) per TRAVELLING,\n3) per END\n")
        progress = progress_status[int(progress) - 1]

        pk = input("\nInserisci la private key: ")

        if progress == "END":

            data = {'longitude': str(longitude),
                    'latitude': str(latitude)}

            URL = url + "/check_arrived"

            r = requests.post(url = URL, json = data)

            response = r.json()

            status = response['status']
        else:
            status = "FALSE"

        data = {'description': description,
                'longitude': str(longitude),
                'latitude': str(latitude),
                'progress':str(progress),
                'status': str(status),
                'private_key': pk}

        URL = url + "/new_marker"
        r = requests.post(url = URL, json = data)


    elif op == 4:
        url_interface = 'file:///C:/Users/markp/EthereumProjects/pathfinder_bis/interface.html'
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url_interface)

    elif op == 5:
        print("Ciao")
        break

    else:

        print("Valore non previsto")
