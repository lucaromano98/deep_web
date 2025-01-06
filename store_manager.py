import json
import os

STORE_FILE = "store_product.json"
default_stores = {
    "armibuonepotenti": [
        {"name": "Monocolpo", "quantità": 5, "costo": "50 Willie Coin"},
        {"name": "Pistola Semi-Automatica", "quantità": 5, "costo": "100 Willie Coin"},
        {"name": "Coltello", "quantità": 5, "costo": "10 Willie Coin"}
    ]
}

def load_store_data():
    if os.path.exists(STORE_FILE):
        try:
            with open(STORE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data
        except json.JSONDecodeError:
            print("Errore nella decodifica del file JSON. Caricamento dei dati predefiniti.")
            return default_stores
    else:
        return default_stores

def save_store_data(store_data):
    with open(STORE_FILE, "w", encoding="utf-8") as file:
        json.dump(store_data, file, indent=4)
