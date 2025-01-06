import tkinter as tk
from ui import create_homepage, show_store, check_url  # Importa check_url da ui.py
from store_manager import load_store_data, save_store_data

root = tk.Tk()
root.title("CORN!")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(True, True)

# Mostra la homepage
create_homepage(root, check_url)

root.mainloop()
