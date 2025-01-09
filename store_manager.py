import json
import os
import sys

STORE_FILE = "store_product.json"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # Ambiente dell'eseguibile
    except AttributeError:
        base_path = os.path.abspath(".")  # Ambiente di sviluppo
    return os.path.join(base_path, relative_path)


default_stores = {
    "armibuonepotenti": [
        {"name": "Monocolpo", "quantità": 5, "costo": "50 Willie Coin"},
        {"name": "Pistola Semi-Automatica", "quantità": 5, "costo": "100 Willie Coin"},
        {"name": "Coltello", "quantità": 5, "costo": "10 Willie Coin"}
    ]
}
def save_store_data(store_data):
    """
    Salva i dati dello store nel file JSON.
    """
    store_file_path = resource_path("store_product.json")
    try:
        with open(store_file_path, "w", encoding="utf-8") as file:
            json.dump(store_data, file, indent=4)
            print("Dati salvati correttamente.")
    except Exception as e:
        print(f"Errore durante il salvataggio dei dati: {e}")


def load_store_data():
    store_file_path = resource_path(STORE_FILE)
    if os.path.exists(store_file_path):
        try:
            with open(store_file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                print(f"Dati caricati correttamente: {data}")  # Debug
                return data
        except json.JSONDecodeError as e:
            print(f"Errore nella decodifica del file JSON: {e}")
            return default_stores
    else:
        print(f"File JSON non trovato: {store_file_path}")
        return default_stores

