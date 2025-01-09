import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps, ImageDraw
from store_manager import load_store_data, save_store_data
from functools import partial
import os



# Colori della bandiera americana per la scritta lampeggiante
colors = ["#FF0000", "#FFFFFF", "#0000FF"]  # Rosso, Bianco, Blu

def create_circular_image_with_border(image_path, border_width=10, border_color="#FFFFFF", final_size=(200, 200)):
    """
    Ritaglia un'immagine in una forma circolare e aggiunge un bordo decorativo.
    :param image_path: Percorso dell'immagine originale.
    :param border_width: Larghezza del bordo.
    :param border_color: Colore del bordo.
    :param final_size: Dimensioni finali dell'immagine (larghezza, altezza).
    :return: Immagine circolare con bordo.
    """
    # Carica l'immagine originale
    img = Image.open(image_path).convert("RGBA")

    # Crea una maschera circolare
    size = (min(img.size),) * 2  # Rende l'immagine quadrata
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)

    # Ritaglia l'immagine
    img = ImageOps.fit(img, size, centering=(0.5, 0.5))
    img.putalpha(mask)

    # Aggiungi il bordo
    border_size = (size[0] + 2 * border_width, size[1] + 2 * border_width)
    bordered_img = Image.new("RGBA", border_size, (0, 0, 0, 0))  # Sfondo trasparente
    draw = ImageDraw.Draw(bordered_img)
    draw.ellipse((0, 0, border_size[0], border_size[1]), fill=border_color)
    bordered_img.paste(img, (border_width, border_width), mask=img)

    # Ridimensiona l'immagine al formato finale
    bordered_img = bordered_img.resize(final_size, Image.Resampling.LANCZOS)

    return bordered_img



def show_store(root, store_name, show_home):
    store_functions = {
        "armibuonepotenti": show_store_armibuonepotenti,
        "sietesolooggetti": show_store_sietesolooggetti,
        "farmaciamici": show_store_farmaciamici,
        "farciturespeciali": show_store_farciturespeciali,
        "droghe4ever": show_store_droghe4ever
    }

    show_function = store_functions.get(store_name)
    if show_function:
        show_function(root, store_name, show_home)
    else:
        messagebox.showerror("Errore", "Store non trovato.")


# Funzione per verificare l'URL inserito e mostrare lo store
def check_url(root, url_entry):
    user_url = url_entry.get()
    store_urls = {
        "www.armibuonepotenti.gre": "armibuonepotenti",
        "www.sietesolooggetti.gre": "sietesolooggetti",
        "www.farmaciamici.gre": "farmaciamici",
        "www.farciturespeciali.gre": "farciturespeciali",
        "www.droghe4ever.gre": "droghe4ever"
    }

    store_name = store_urls.get(user_url)
    if store_name:
        # Chiama la funzione generica `show_store`
        show_store(root, store_name, lambda: create_homepage(root, check_url))
    else:
        messagebox.showerror("Errore", "URL non trovato.")

def handle_purchase(store_name, product, quantity_label, buy_button, confirmation_label, confimation_color):
    """
    Gestisce l'acquisto di un prodotto:
    - Diminuisce la quantità.
    - Disabilita il pulsante "Acquista" se la quantità scende a 0.
    - Mostra un messaggio di conferma globale sotto tutte le card.
    """
    # Carica i dati dello store
    store_data = load_store_data()
    products = store_data.get(store_name, [])

    # Cerca il prodotto specifico
    for p in products:
        if p["name"] == product["name"]:
            # Controlla la disponibilità
            if isinstance(p["quantità"], int) and p["quantità"] > 0:
                # Riduci la quantità
                p["quantità"] -= 1

                # Aggiorna la quantità nel widget
                if p["quantità"] == 0:
                    p["quantità"] = "Esaurito"
                    quantity_label.config(text="Esaurito", fg="#FF0000")
                    buy_button.config(state=tk.DISABLED)  # Disabilita il pulsante
                else:
                    quantity_label.config(text=f"Quantità: {p['quantità']}")

                # Mostra il messaggio globale di conferma
                confirmation_label.config(
                    text=f"Acquisto di {p['name']} effettuato con successo! (CHIAMA UN NARRATORE!)",
                    fg= confimation_color  #colore custom
                )

                # Salva i prodotti aggiornati
                store_data[store_name] = products
                save_store_data(store_data)
            else:
                # Mostra un messaggio di errore globale
                confirmation_label.config(
                    text=f"Prodotto {p['name']} non disponibile.",
                    fg="#FF0000"  # Testo rosso
                )
            break



# Funzione per animare la scritta di benvenuto
def animate_label():
    current_color = colors[animate_label.color_index]
    welcome_label.config(fg=current_color)
    animate_label.color_index = (animate_label.color_index + 1) % len(colors)
    welcome_label.after(500, animate_label)  # Cambia colore ogni 500 ms

animate_label.color_index = 0

# Funzione per mostrare la homepage
def create_homepage(root, check_url):
    # Configura la finestra principale per la homepage
    root.configure(bg="#3a003f")

    # Rimuove tutti i widget attualmente presenti nella finestra
    for widget in root.winfo_children():
        widget.destroy()

    # Creazione del frame centrale (centrale alla pagina)
    middle_frame = tk.Frame(root, bg="#3a003f")
    middle_frame.pack(fill=tk.BOTH, expand=True)

    # Centrare tutto utilizzando un contenitore interno
    content_frame = tk.Frame(middle_frame, bg="#3a003f")
    content_frame.pack(expand=True)  # Centra il contenuto nella finestra

    # Aggiungi il logo
    try:
        logo_image = Image.open(os.path.join("assets", "corn_logo.png"))  # Modifica con il tuo file di logo
        logo_image = logo_image.resize((200, 200), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(content_frame, image=logo_photo, bg="#3a003f")
        logo_label.image = logo_photo  # Conserva il riferimento
        logo_label.pack(pady=20)  # Spaziatura verticale
    except Exception as e:
        print(f"Errore nel caricamento del logo: {e}")

    # Etichetta per l'URL
    url_label = tk.Label(
        content_frame,
        text="Inserisci URL:",
        font=('Comic Sans MS', 14),
        bg="#3a003f",
        fg="white"
    )
    url_label.pack(pady=10)

    # Campo di input per l'URL
    url_entry = tk.Entry(content_frame, font=('Comic Sans MS', 12), width=50)
    url_entry.pack(pady=10)

    # Pulsante "Vai"
    go_button = tk.Button(
        content_frame,
        text="Vai",
        command=lambda: check_url(root, url_entry),
        font=('Comic Sans MS', 12, 'bold'),
        bg="#800080",
        fg="white",
        bd=5,
        cursor = "hand2" 
    )
    go_button.pack(pady=10)



# Funzione per mostrare lo store di armi
def show_store_armibuonepotenti(root, store_name, show_home):
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
    home_button = tk.Button(
        main_frame, 
        text="Home", 
        font=('Comic Sans MS', 12, 'bold'), 
        bg="#800080", 
        fg="white", 
        cursor = "hand2",
        command=show_home
        )
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
            elif product["quantità"] > 0:
                product_quantity_label.config(text=f"Quantità: {product['quantità']}")
            else:
                product_quantity_label.config(text="Prodotto non disponibile")
            product_quantity_label.pack()

            # Costo del prodotto
            product_price = tk.Label(product_frame, text=f"Costo: {product['costo']}", font=('Comic Sans MS', 12), bg="#4b006e", fg="#d1b3ff")
            product_price.pack(pady=(5, 10))

            # Pulsante di acquisto
            buy_button = tk.Button(
                product_frame,
                text="Acquista",
                font=('Impact', 12, 'bold'),
                bg="#800080",  # Colore viola per il pulsante
                fg="#FFFFFF",  # Testo bianco
                cursor = "hand2" 
            )
            buy_button.config(
                command=partial(handle_purchase, store_name, product, product_quantity_label, buy_button, confirmation_label, "#FF4500")
            )
            buy_button.pack(pady=5)  # Posiziona il pulsante



           

# Funzione per mostrare lo store di traffico umano
def show_store_sietesolooggetti(root, store_name, show_home):
    # Pulisce la finestra principale per mostrare lo store
    for widget in root.winfo_children():
        widget.destroy()

    # Configura la finestra per lo store "Siete Solo Oggetti"
    root.configure(bg="#0C0C0E")  # Sfondo nero

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
    home_button = tk.Button(
        main_frame, 
        text="Home", 
        font=('Roboto', 12, 'bold'), 
        bg="#FF0000", 
        fg="white", 
        cursor = "hand2",
        command=show_home 
        )
    home_button.pack(pady=10, anchor='nw')

    # Carica il logo personalizzato
    try:
        logo_image = Image.open(os.path.join("assets", "sietesolooggetti_logo.png"))  # Assicurati di avere questa immagine
        logo_image = logo_image.resize((400, 400), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(main_frame, image=logo_photo, bg="#0C0C0E")
        logo_label.image = logo_photo
        logo_label.pack(pady=20)
    except Exception as e:
        print(f"Errore nel caricamento del logo: {e}")
    # Scritta di benvenuto con font robotico e colore verde fluorescente
    welcome_label = tk.Label(main_frame, text=f"⚠ BENVENUTO SU {store_name.upper()} ⚠", font=('Roboto', 28, 'bold'), fg="#00FF00", bg="#0C0C0E")
    welcome_label.pack(pady=20)


    # Carica i prodotti dallo store "Siete Solo Oggetti"
    store_data = load_store_data()
    products = store_data.get(store_name, [])

    # Mostra i prodotti come card
    if products:
        card_frame = tk.Frame(main_frame, bg="#0C0C0E")  # Frame per contenere tutte le card
        card_frame.pack(pady=20)


        for product in products:
    # Frame della card per ciascun prodotto
            product_frame = tk.Frame(card_frame, bg="#222222", bd=5, relief="ridge")
            product_frame.pack(side=tk.LEFT, padx=20, pady=20)

            # Nome del prodotto
            product_name = tk.Label(
                product_frame,
                text=product["name"],
                font=('Roboto', 14, 'bold'),
                bg="#222222",
                fg="#FFFFFF"
            )
            product_name.pack(pady=(10, 5))

            # Quantità del prodotto
            product_quantity_label = tk.Label(
                product_frame,
                font=('Roboto', 12),
                bg="#222222",
                fg="#FFFFFF"
            )
            if product["quantità"] == "Esaurito":
                product_quantity_label.config(text="Esaurito", fg="#FF0000")
            else:
                product_quantity_label.config(text=f"Quantità: {product['quantità']}")
            product_quantity_label.pack()

            # Costo del prodotto
            product_price = tk.Label(
                product_frame,
                text=f"Costo: {product['costo']}",
                font=('Roboto', 12),
                bg="#222222",
                fg="#FFFFFF"
            )
            product_price.pack(pady=(5, 10))

            confirmation_label = tk.Label(
                main_frame,
                text="",
                font=('Roboto', 16, 'bold'),
                bg="#0C0C0E",  # Sfondo nero scuro
                fg="#00FF00",  # Testo verde brillante
                pady=10
            )
            confirmation_label.pack(pady=20)

            # Pulsante di acquisto
            buy_button = tk.Button(
                product_frame,
                text="Prenota",
                font=('Roboto', 12, 'bold'),
                bg="#FF0000",  # Colore rosso per il pulsante
                fg="#FFFFFF",   # Testo bianco
                cursor = "hand2"            
            )
            if product["quantità"] == "Esaurito" or product["quantità"] == 0:
                buy_button.config(state=tk.DISABLED)  # Disabilita il pulsante se il prodotto è esaurito
            else:
                buy_button.config(
                    command=partial(handle_purchase, store_name, product, product_quantity_label, buy_button, confirmation_label, "00FF00")
                )
            buy_button.pack(pady=5)  # Posiziona il pulsante





#Store Farmaci quest El Chapo
def show_store_farmaciamici(root, store_name, show_home):
    # Pulisce la finestra principale per mostrare lo store
    for widget in root.winfo_children():
        widget.destroy()

    # Configura la finestra per lo store "Farmacia Amici"
    root.configure(bg="#E0F7FA")  # Sfondo azzurro chiaro

    # Crea un canvas con uno scrollbar per contenere il main_frame
    canvas = tk.Canvas(root, bg="#E0F7FA", highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Crea un frame per il contenuto centrale dello store
    main_frame = tk.Frame(canvas, bg="#E0F7FA")
    canvas_window = canvas.create_window((0, 0), window=main_frame, anchor='n')

    # Configura il canvas per adattarsi al contenuto del frame
    main_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

    # Pulsante "Home" per tornare alla homepage
    home_button = tk.Button (
        main_frame, 
        text="Home", 
        font=('Helvetica', 12, 'bold'), 
        bg="#00897B", 
        fg="white",
        cursor = "hand2",  
        command=show_home
        )
    home_button.pack(pady=10, anchor='nw')

    # Icona a tema medico
    try:
        icon_path = os.path.join("assets", "farmaciamici_logo.png")  # Assicurati di avere questa immagine
        icon_image = Image.open(icon_path)
        icon_image = icon_image.resize((400, 400), Image.Resampling.LANCZOS)
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label = tk.Label(main_frame, image=icon_photo, bg="#E0F7FA")
        icon_label.image = icon_photo
        icon_label.pack(pady=20)
    except Exception as e:
        print(f"Errore nel caricamento dell'icona: {e}")
    # Scritta di benvenuto
    welcome_label = tk.Label(main_frame, text=f"Benvenuto su {store_name.upper()} :D", font=('Helvetica', 28, 'bold'), fg="#004D40", bg="#E0F7FA",)
    welcome_label.pack(pady=20)


    # Carica i prodotti dello store "Farmacia Amici"
    store_data = load_store_data()
    products = store_data.get(store_name, [])

    # Mostra i prodotti
    if products:
        card_frame = tk.Frame(main_frame, bg="#E0F7FA")  # Frame per contenere tutte le card
        card_frame.pack(pady=20)

        for product in products:
            # Frame della card per ciascun prodotto
            product_frame = tk.Frame(card_frame, bg="#FFFFFF", bd=2, relief="solid")
            product_frame.pack(side=tk.LEFT, padx=15, pady=15)

            # Nome del prodotto
            product_name = tk.Label(
                product_frame,
                text=product["name"],
                font=('Helvetica', 14, 'bold'),
                bg="#FFFFFF",
                fg="#004D40"
            )
            product_name.pack(pady=(10, 5))

            # Quantità del prodotto
            product_quantity_label = tk.Label(
                product_frame,
                font=('Helvetica', 12),
                bg="#FFFFFF",
                fg="#004D40"
            )
            if product["quantità"] == "Esaurito":
                product_quantity_label.config(text="Esaurito", fg="#FF0000")
            else:
                product_quantity_label.config(text=f"Quantità: {product['quantità']}")
            product_quantity_label.pack()

            # Costo del prodotto
            product_price = tk.Label(
                product_frame,
                text=f"Costo: {product['costo']}",
                font=('Helvetica', 12),
                bg="#FFFFFF",
                fg="#004D40"
            )
            product_price.pack(pady=(5, 10))

            # Messaggio di conferma
            
            confirmation_label = tk.Label(
                main_frame,
                text="",
                font=('Roboto', 16, 'bold'),
                bg="#FFFFFF",  # Sfondo chiaro per visibilità
                fg="#004D40",  # Testo verde scuro
                pady=10
                )
            confirmation_label.pack(pady=20)

            # Pulsante di acquisto
            buy_button = tk.Button(
                product_frame,
                text="Acquista",
                font=('Helvetica', 12, 'bold'),
                bg="#00897B",  # Colore verde acqua come il pulsante "Home"
                fg="white", # Testo bianco
                cursor = "hand2"      
            )
            if product["quantità"] == "Esaurito" or product["quantità"] == 0:
                buy_button.config(state=tk.DISABLED)  # Disabilita il pulsante se il prodotto è esaurito
            else:
                buy_button.config(
                    command=partial(handle_purchase, store_name, product, product_quantity_label, buy_button, confirmation_label, "#00BFFF")
                )
            buy_button.pack(pady=5)  # Posiziona il pulsante

def show_store_farciturespeciali(root, store_name, show_home):
    # Pulisce la finestra principale per mostrare lo store
    for widget in root.winfo_children():
        widget.destroy()

    # Configura la finestra per lo store "Farciture Speciali"
    root.configure(bg="#FFF7E0")  # Sfondo beige chiaro

    # Crea un canvas con uno scrollbar per contenere il main_frame
    canvas = tk.Canvas(root, bg="#FFF7E0", highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Crea un frame per il contenuto centrale dello store
    main_frame = tk.Frame(canvas, bg="#FFF7E0")
    canvas_window = canvas.create_window((0, 0), window=main_frame, anchor='n')

    # Configura il canvas per adattarsi al contenuto del frame
    main_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Configura il canvas per adattarsi alla larghezza della finestra
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

    # Pulsante "Home" per tornare alla homepage
    home_button = tk.Button (
        main_frame, 
        text="Home", 
        font=('Comic Sans MS', 12, 'bold'), 
        bg="#FFCC80", 
        fg="#000000", cursor = "hand2", 
        command=show_home
        )
    
    home_button.pack(pady=10, anchor='nw')

    # Carica il logo personalizzato
    try:
        logo_image = Image.open(os.path.join("assets", "farciture_speciali_logo.png"))  # Assicurati di avere questa immagine
        logo_image = logo_image.resize((400, 400), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(main_frame, image=logo_photo, bg="#FFF7E0")
        logo_label.image = logo_photo
        logo_label.pack(pady=20)
    except Exception as e:
        print(f"Errore nel caricamento del logo: {e}")

    # Scritta di benvenuto con font giocoso e colore arancione brillante
    welcome_label = tk.Label(main_frame, text=f"⚡ BENVENUTO SU {store_name.upper()} ⚡", font=('Comic Sans MS', 28, 'bold'), fg="#FF5722", bg="#FFF7E0")
    welcome_label.pack(pady=20)

    # Carica i prodotti dallo store "Farciture Speciali"
    store_data = load_store_data()
    products = store_data.get(store_name, [])

    # Mostra i prodotti come card
    if products:
        card_frame = tk.Frame(main_frame, bg="#FFF7E0")  # Frame per contenere tutte le card
        card_frame.pack(pady=20)

        # Etichetta per il messaggio di conferma dell'acquisto
        confirmation_label = tk.Label(
            main_frame,
            text="",
            font=('Comic Sans MS', 16, 'bold'),
            bg="#FFF7E0",  # Sfondo beige
            fg="#4CAF50",  # Testo verde per conferma
            pady=10
        )
        confirmation_label.pack(pady=20)

        for product in products:
            # Frame della card per ciascun prodotto
            product_frame = tk.Frame(card_frame, bg="#FFEBB0", bd=5, relief="ridge")
            product_frame.pack(side=tk.LEFT, padx=20, pady=20)

            # Nome del prodotto
            product_name = tk.Label(
                product_frame,
                text=product["name"],
                font=('Comic Sans MS', 14, 'bold'),
                bg="#FFEBB0",
                fg="#000000"
            )
            product_name.pack(pady=(10, 5))

            # Quantità del prodotto
            product_quantity_label = tk.Label(
                product_frame,
                font=('Comic Sans MS', 12),
                bg="#FFEBB0",
                fg="#000000"
            )
            if product["quantità"] == "Esaurito":
                product_quantity_label.config(text="Esaurito", fg="#FF0000")
            else:
                product_quantity_label.config(text=f"Quantità: {product['quantità']}")
            product_quantity_label.pack()

            # Costo del prodotto
            product_price = tk.Label(
                product_frame,
                text=f"Costo: {product['costo']}",
                font=('Comic Sans MS', 12),
                bg="#FFEBB0",
                fg="#000000"
            )
            product_price.pack(pady=(5, 10))

            # Pulsante di acquisto
            buy_button = tk.Button(
                product_frame,
                text="Acquista",
                font=('Comic Sans MS', 12, 'bold'),
                bg="#FFCC80",  # Colore arancione pastello
                fg="#000000",   # Testo nero
                cursor = "hand2" 
            )
            if product["quantità"] == "Esaurito" or product["quantità"] == 0:
                buy_button.config(state=tk.DISABLED)  # Disabilita il pulsante se il prodotto è esaurito
            else:
                buy_button.config(
                    command=partial(handle_purchase, store_name, product, product_quantity_label, buy_button, confirmation_label, "#4CAF50")
                )
            buy_button.pack(pady=5)  # Posiziona il pulsante

def show_store_droghe4ever(root, store_name, show_home):
    # Pulisce la finestra principale per mostrare lo store
    for widget in root.winfo_children():
        widget.destroy()

    # Configura la finestra per lo store "Droghe4Ever"
    root.configure(bg="#3A0CA3")  # Sfondo viola scuro

    # Crea un canvas con uno scrollbar per contenere il main_frame
    canvas = tk.Canvas(root, bg="#3A0CA3", highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Crea un frame per il contenuto centrale dello store
    main_frame = tk.Frame(canvas, bg="#3A0CA3")
    canvas_window = canvas.create_window((0, 0), window=main_frame, anchor='n')

    # Configura il canvas per adattarsi al contenuto del frame
    main_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Configura il canvas per adattarsi alla larghezza della finestra
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

    # Pulsante "Home" per tornare alla homepage
    home_button = tk.Button (
        main_frame, 
        text="Home", 
        font=('Verdana', 12, 'bold'), 
        bg="#39FF14", 
        fg="#000000",
        cursor = "hand2", 
        command=show_home
        )
    home_button.pack(pady=10, anchor='nw')

    # Carica il logo personalizzato
    try:
        # Crea un'immagine circolare con bordo
        circular_logo = create_circular_image_with_border("assets/droghe4ever_logo.png", border_width=15, border_color="#39FF14")
        
        # Converti l'immagine per Tkinter
        logo_photo = ImageTk.PhotoImage(circular_logo)
        
        # Mostra il logo
        logo_label = tk.Label(main_frame, image=logo_photo, bg="#3A0CA3")
        logo_label.image = logo_photo  # Salva un riferimento per evitare che l'immagine venga cancellata
        logo_label.pack(pady=20)
    except Exception as e:
        print(f"Errore nel caricamento del logo: {e}")


    # Scritta di benvenuto con font luminoso e colore verde neon
    welcome_label = tk.Label(main_frame, text=f"💊 BENVENUTO SU {store_name.upper()} 💊", font=('Verdana', 28, 'bold'), fg="#FF69B4", bg="#3A0CA3")
    welcome_label.pack(pady=20)

    # Carica i prodotti dallo store "Droghe4Ever"
    store_data = load_store_data()
    products = store_data.get(store_name, [])

    # Mostra i prodotti come card
    if products:
        card_frame = tk.Frame(main_frame, bg="#3A0CA3")  # Frame per contenere tutte le card
        card_frame.pack(pady=20)

        # Etichetta per il messaggio di conferma dell'acquisto
        confirmation_label = tk.Label(
            main_frame,
            text="",
            font=('Verdana', 16, 'bold'),
            bg="#3A0CA3",  # Sfondo viola scuro
            fg="#39FF14",  # Testo verde neon
            pady=10
        )
        confirmation_label.pack(pady=20)

        for product in products:
            # Frame della card per ciascun prodotto
            product_frame = tk.Frame(card_frame, bg="#240046", bd=5, relief="ridge")
            product_frame.pack(side=tk.LEFT, padx=20, pady=20)

            # Nome del prodotto
            product_name = tk.Label(
                product_frame,
                text=product["name"],
                font=('Verdana', 14, 'bold'),
                bg="#240046",
                fg="#FFFFFF"
            )
            product_name.pack(pady=(10, 5))

            # Quantità del prodotto
            product_quantity_label = tk.Label(
                product_frame,
                font=('Verdana', 12),
                bg="#240046",
                fg="#FFFFFF"
            )
            if product["quantità"] == "Esaurito":
                product_quantity_label.config(text="Esaurito", fg="#FF0000")
            else:
                product_quantity_label.config(text=f"Quantità: {product['quantità']}")
            product_quantity_label.pack()

            # Costo del prodotto
            product_price = tk.Label(
                product_frame,
                text=f"Costo: {product['costo']}",
                font=('Verdana', 12),
                bg="#240046",
                fg="#FFFFFF"
            )
            product_price.pack(pady=(5, 10))

            # Pulsante di acquisto
            buy_button = tk.Button(
                product_frame,
                text="Pagamento \n alla Consegna!",
                font=('Verdana', 12, 'bold'),
                bg="#39FF14",  # Verde neon
                fg="#000000", # Testo nero
                cursor = "hand2" 
            )
            if product["quantità"] == "Esaurito" or product["quantità"] == 0:
                buy_button.config(state=tk.DISABLED)  # Disabilita il pulsante se il prodotto è esaurito
            else:
                buy_button.config(
                    command=partial(handle_purchase, store_name, product, product_quantity_label, buy_button, confirmation_label, "#39FF14")
                )
            buy_button.pack(pady=5)  # Posiziona il pulsante


