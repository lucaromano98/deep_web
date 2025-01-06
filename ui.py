import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from store_manager import load_store_data, save_store_data
from functools import partial
import os

# Colori della bandiera americana per la scritta lampeggiante
colors = ["#FF0000", "#FFFFFF", "#0000FF"]  # Rosso, Bianco, Blu

# Funzione per gestire l'acquisto
def purchase(store_name, product, product_quantity_label, buy_button, confirmation_label):
    # Carica i dati dello store per evitare conflitti di concorrenza
    store_data = load_store_data()
    products = store_data.get(store_name, [])

    # Cerca il prodotto specifico in base al nome
    for p in products:
        if p["name"] == product["name"]:
            # Verifica la disponibilità del prodotto
            if p["quantità"] > 0:
                p["quantità"] -= 1
                product_quantity_label.config(text=f"Quantità: {p['quantità']}")

                # Se la quantità raggiunge zero, disabilita il pulsante e aggiorna il messaggio
                if p["quantità"] == 0:
                    product_quantity_label.config(text="Prodotto non disponibile")
                    buy_button.config(state=tk.DISABLED)

                # Mostra il messaggio di conferma dell'acquisto direttamente nella pagina
                confirmation_label.config(text=f"Acquisto di {p['name']} effettuato, chiama un narratore.")

                # Salva i prodotti aggiornati nel file
                store_data[store_name] = products
                save_store_data(store_data)
            else:
                confirmation_label.config(text="Prodotto non disponibile.")
            break

# Funzione per verificare l'URL inserito e mostrare lo store
def check_url(root, url_entry, show_store):
    user_url = url_entry.get()  # Ottiene il valore inserito nel campo di input
    store_urls = {
        "www.armibuonepotenti.gre": "armibuonepotenti",
        "www.sietesolooggetti.gre": "sietesolooggetti"
    }

    store_name = store_urls.get(user_url)
    if store_name == "sietesolooggetti":
        show_store_sietesolooggetti(root, store_name, lambda: create_homepage(root, check_url, show_store))
    elif store_name:  # Per gli altri store generici
        show_store(root, store_name, lambda: create_homepage(root, check_url, show_store))
    else:
        messagebox.showerror("Errore", "URL non trovato.")  # Mostra un messaggio di errore


# Funzione per animare la scritta di benvenuto
def animate_label():
    current_color = colors[animate_label.color_index]
    welcome_label.config(fg=current_color)
    animate_label.color_index = (animate_label.color_index + 1) % len(colors)
    welcome_label.after(500, animate_label)  # Cambia colore ogni 500 ms

animate_label.color_index = 0

# Funzione per mostrare la homepage
def create_homepage(root, check_url, show_store):
    # Pulisce la finestra principale per mostrare la homepage
    for widget in root.winfo_children():
        widget.destroy()

    # Configura lo sfondo principale
    root.configure(bg="#2d0033")

    # Sezione centrale per la barra di ricerca
    middle_frame = tk.Frame(root, bg='#2d0033')
    middle_frame.pack(expand=True)

    # Carica l'immagine del logo della homepage
    try:
        logo_image = Image.open(os.path.join("assets", "corn_logo.png"))
        logo_image = logo_image.resize((200, 200), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(middle_frame, image=logo_photo, bg='#2d0033')
        logo_label.image = logo_photo
        logo_label.pack(pady=20)
    except Exception as e:
        print(f"Errore nel caricamento del logo: {e}")

    # Etichetta per l'URL
    url_label = tk.Label(middle_frame, text="Inserisci l'URL:", fg='#d1b3ff', bg='#2d0033', font=('Comic Sans MS', 16, 'bold'))
    url_label.pack(pady=10)

    # Campo di input per l'URL
    url_entry = tk.Entry(middle_frame, width=50, font=('Courier', 12), bg="#4b006e", fg="white", insertbackground="white")
    url_entry.pack(pady=10)

    # Pulsante "Vai"
    go_button = tk.Button(middle_frame, text="Vai", command=lambda: check_url(root, url_entry, show_store), font=('Comic Sans MS', 12, 'bold'), bg="#800080", fg="white", bd=5)
    go_button.pack(pady=5)

# Funzione per mostrare lo store sulla finestra principale
def show_store(root, store_name, show_home):
    # Pulisce la finestra principale per mostrare lo store
    for widget in root.winfo_children():
        widget.destroy()

    # Configura la finestra per lo store
    root.configure(bg="#3a003f")  # Sfondo viola scuro

    # Crea un canvas con uno scrollbar per contenere il main_frame
    canvas = tk.Canvas(root, bg="#3a003f")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Crea un frame per il contenuto centrale dello store
    main_frame = tk.Frame(canvas, bg="#3a003f")
    canvas_window = canvas.create_window((0, 0), window=main_frame, anchor='n')

    # Configura il canvas per adattarsi al contenuto del frame
    main_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Configura il canvas per adattarsi alla larghezza della finestra
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

    # Pulsante "Home" per tornare alla homepage
    home_button = tk.Button(main_frame, text="Home", font=('Comic Sans MS', 12, 'bold'), bg="#800080", fg="white", command=show_home)
    home_button.pack(pady=10, anchor='nw')

    # Scritta di benvenuto al centro dell'interfaccia dello store
    global welcome_label
    welcome_label = tk.Label(main_frame, text=f"BENVENUTO SU {store_name.upper()}", font=('Impact', 32, 'bold'), bg="#3a003f")
    welcome_label.pack(pady=10)

    # Inizia l'animazione della scritta di benvenuto
    animate_label()

    # Carica l'immagine della bandiera americana
    try:
        flag_image = Image.open(os.path.join("assets", "bandiera_armifighe.png"))
        flag_image = flag_image.resize((300, 150), Image.Resampling.LANCZOS)
        flag_photo = ImageTk.PhotoImage(flag_image)
        flag_label = tk.Label(main_frame, image=flag_photo, bg="#3a003f")
        flag_label.image = flag_photo
        flag_label.pack(pady=10)
    except Exception as e:
        print(f"Errore nel caricamento della bandiera: {e}")

    # Carica i prodotti dal file per lo store corrente
    store_data = load_store_data()
    products = store_data.get(store_name, [])

    # Mostra i prodotti come card disposte orizzontalmente e centrate
    if products:
        card_frame = tk.Frame(main_frame, bg="#3a003f")  # Frame per contenere tutte le card
        card_frame.pack(pady=20)

        # Etichetta per il messaggio di conferma dell'acquisto
        confirmation_label = tk.Label(main_frame, text="", font=('Comic Sans MS', 14), bg="#3a003f", fg="#d1b3ff")
        confirmation_label.pack(pady=20)

        for product in products:
            # Crea un frame per la card del prodotto
            product_frame = tk.Frame(card_frame, bg="#4b006e", bd=5, relief="groove")
            product_frame.pack(side=tk.LEFT, padx=20, pady=20)

            # Nome del prodotto
            product_name = tk.Label(product_frame, text=product["name"], font=('Comic Sans MS', 14, 'bold'), bg="#4b006e", fg="#d1b3ff")
            product_name.pack(pady=(10, 5))

          # Quantità del prodotto e gestione stato
            product_quantity_label = tk.Label(product_frame, font=('Comic Sans MS', 12), bg="#4b006e", fg="#d1b3ff")
            if product["quantità"] == "Esaurito":
                product_quantity_label.config(text="Esaurito")
                buy_button.config(state=tk.DISABLED)
            elif product["quantità"] > 0:
                product_quantity_label.config(text=f"Quantità: {product['quantità']}")
            else:
                product_quantity_label.config(text="Prodotto non disponibile")


            # Costo del prodotto
            product_price = tk.Label(product_frame, text=f"Costo: {product['costo']}", font=('Comic Sans MS', 12), bg="#4b006e", fg="#d1b3ff")
            product_price.pack(pady=(5, 10))

            # Pulsante di acquisto
            buy_button = tk.Button(
                product_frame,
                text="Acquista",
                font=('Comic Sans MS', 12, 'bold'),
                bg="#800080",
                fg="white"
            )
            buy_button.config(command=partial(purchase, store_name, product, product_quantity_label, buy_button, confirmation_label))

            # Se il prodotto non è disponibile, disabilita il pulsante di acquisto
            if product["quantità"] == 0:
                buy_button.config(state=tk.DISABLED)

            buy_button.pack(pady=5)
    else:
        no_products_label = tk.Label(main_frame, text="Nessun prodotto disponibile", font=('Comic Sans MS', 16), bg="#3a003f", fg="#d1b3ff")
        no_products_label.pack(pady=20)
        

# Funzione per mostrare lo store "Siete Solo Oggetti"
def show_store_sietesolooggetti(root, store_name, show_home):
    # Pulisce la finestra principale per mostrare lo store
    for widget in root.winfo_children():
        widget.destroy()

    # Configura la finestra per lo store "Siete Solo Oggetti"
    root.configure(bg="#0C0C0E")  # Sfondo dello stesso colore dell'immagine

    # Crea un canvas con uno scrollbar per contenere il main_frame
    canvas = tk.Canvas(root, bg="#0C0C0E", highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Crea un frame per il contenuto centrale dello store
    main_frame = tk.Frame(canvas, bg="#0C0C0E")
    canvas_window = canvas.create_window((0, 0), window=main_frame, anchor='n')

    # Configura il canvas per adattarsi al contenuto del frame
    main_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Configura il canvas per adattarsi alla larghezza della finestra
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

    # Pulsante "Home" per tornare alla homepage
    home_button = tk.Button(main_frame, text="Home", font=('Roboto', 12, 'bold'), bg="#FF0000", fg="white", command=show_home)
    home_button.pack(pady=10, anchor='nw')

    # Scritta di benvenuto con font robotico e colore verde fluorescente
    welcome_label = tk.Label(main_frame, text=f"⚠ BENVENUTO SU {store_name.upper()} ⚠", font=('Roboto', 28, 'bold'), fg="#00FF00", bg="#0C0C0E")
    welcome_label.pack(pady=20)

    # Carica il logo personalizzato
    try:
        logo_image = Image.open(os.path.join("assets", "sietesolooggetti_logo.png"))
        logo_image = logo_image.resize((400, 400), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(main_frame, image=logo_photo, bg="#0C0C0E")
        logo_label.image = logo_photo
        logo_label.pack(pady=20)
    except Exception as e:
        print(f"Errore nel caricamento del logo: {e}")

    # Carica i prodotti dallo store "Siete Solo Oggetti"
    store_data = load_store_data()
    products = store_data.get(store_name, [])

    # Mostra i prodotti come card
    if products:
        card_frame = tk.Frame(main_frame, bg="#0C0C0E")  # Frame per contenere tutte le card
        card_frame.pack(pady=20)

        confirmation_label = tk.Label(main_frame, text="", font=('Roboto', 14), bg="#0C0C0E", fg="#00FF00")
        confirmation_label.pack(pady=20)

        for product in products:
            product_frame = tk.Frame(card_frame, bg="#1E1E1E", bd=5, relief="ridge")
            product_frame.pack(side=tk.LEFT, padx=20, pady=20)

            # Nome del prodotto
            product_name = tk.Label(product_frame, text=product["name"], font=('Roboto', 14, 'bold'), bg="#1E1E1E", fg="#FFFFFF")
            product_name.pack(pady=(10, 5))

            # Quantità del prodotto
            product_quantity_label = tk.Label(product_frame, font=('Roboto', 12), bg="#1E1E1E", fg="#FFFFFF")
            if product["quantità"] == "Esaurito":
                product_quantity_label.config(text="Esaurito", fg="#FF0000")
            else:
                product_quantity_label.config(text=f"Quantità: {product['quantità']}")
            product_quantity_label.pack()

            # Costo del prodotto
            product_price = tk.Label(product_frame, text=f"Costo: {product['costo']}", font=('Roboto', 12), bg="#1E1E1E", fg="#FFFFFF")
            product_price.pack(pady=(5, 10))

            # Pulsante di acquisto
            buy_button = tk.Button(product_frame, text="Acquista", font=('Roboto', 12, 'bold'), bg="#FF0000", fg="white")
            if product["quantità"] == "Esaurito":
                buy_button.config(state=tk.DISABLED)
            buy_button.pack(pady=5)

    else:
        no_products_label = tk.Label(main_frame, text="Nessun prodotto disponibile", font=('Roboto', 16), bg="#0C0C0E", fg="#FF0000")
        no_products_label.pack(pady=20)



