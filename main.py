import tkinter as tk
from tkinter import ttk
import pyautogui
import pyperclip
import time
import configparser
import os
import sys

if getattr(sys, 'frozen', False):
    app_path = os.path.dirname(sys.executable)
else:
    app_path = os.path.dirname(os.path.abspath(__file__))

config_file = os.path.join(app_path, 'config.ini')
config = configparser.ConfigParser(allow_no_value=True)

default_config = {
    'HEMOGRAMA': {'hb': '', 'ht': '', 'gl': '', 's': '', 'l': '', 'p': ''},
    'LIPIDOGRAMA': {'ct': '', 'hdl': '', 'ldl': '', 'tg': ''},
    'GLICEMIA': {'gli': '', 'a1c': ''},
    'RENAL E ELETROLITOS': {'cr': '', 'ur': '', 'ac ur': '', 'k': '', 'na': '', 'mg': '', 'cl': '', 'ca': '', 'ca tot': ''},
    'HEPATICO E HORMONAL': {'tgo': '', 'tgp': '', 'ggt': '', 'falc': '', 'tsh': '', 'pth': '', 'vit d': '', 'b12': ''},
    'SOROLOGIAS E MARCADORES': {'hcv': 'NR', 'hbsag': 'NR', 'vdrl': 'NR', 'hiv': 'NR', 'psa': ''},
    'URINA E FEZES': {'eas': 'NDN', 'mif': 'NEG', 'psof': 'NEG'}
}

if not os.path.exists(config_file):
    for sec, items in default_config.items():
        config[sec] = items
    with open(config_file, 'w') as configfile:
        config.write(configfile)

config.read(config_file)

def disparar_texto(event=None):
    resultados = []
    for label, entry in campos.items():
        valor = entry.get().strip()
        if valor:
            resultados.append(f"{label} {valor}")
    
    if resultados:
        texto_final = " / ".join(resultados) + " /"
        pyperclip.copy(texto_final)
    
    root.withdraw()
    time.sleep(0.3)
    
    if resultados:
        pyautogui.hotkey('ctrl', 'v')
    
    root.quit()

# Funções de Navegação e Foco
def move_up(event):
    event.widget.tk_focusPrev().focus()
    return "break"

def move_down(event):
    event.widget.tk_focusNext().focus()
    return "break"

def on_focus_in(event):
    event.widget.configure(background="#fffacd") # Fica amarelo claro ao focar
    event.widget.select_range(0, tk.END) # Seleciona tudo para sobrescrever fácil

def on_focus_out(event):
    event.widget.configure(background="white") # Volta a cor normal

# --- Configuração da Interface ---
root = tk.Tk()
root.title("Medical Lab Entry - Dept. 42")
root.attributes('-topmost', True)
root.resizable(False, False)

style = ttk.Style(root)
if 'clam' in style.theme_names():
    style.theme_use('clam')

BG_COLOR = "#e8ecef"
HEADER_BG = "#2c3e50"
SECTION_COLOR = "#34495e"
root.configure(bg=BG_COLOR)

header = tk.Frame(root, bg=HEADER_BG, pady=8)
header.pack(fill='x')
tk.Label(header, text="LABORATORY DATA ENTRY", fg="white", bg=HEADER_BG, font=('Segoe UI', 11, 'bold')).pack()

body = tk.Frame(root, bg=BG_COLOR, padx=15, pady=10)
body.pack(fill='both', expand=True)

campos = {}
current_col = 0
current_row = 0
MAX_ROWS_PER_COLUMN = 20 

for section in config.sections():
    if current_row >= MAX_ROWS_PER_COLUMN - 3:
        current_col += 2
        current_row = 0
    
    sec_lbl = tk.Label(body, text=section.upper(), font=('Segoe UI', 9, 'bold'), bg=BG_COLOR, fg=SECTION_COLOR)
    sec_lbl.grid(row=current_row, column=current_col, columnspan=2, sticky='w', pady=(8, 0), padx=5)
    
    sep = ttk.Separator(body, orient='horizontal')
    sep.grid(row=current_row+1, column=current_col, columnspan=2, sticky='ew', padx=5, pady=(2, 6))
    current_row += 2
    
    for key, default_val in config.items(section):
        if current_row >= MAX_ROWS_PER_COLUMN:
            current_col += 2
            current_row = 0
            
        lbl = ttk.Label(body, text=f"{key.upper()}:", background=BG_COLOR, font=('Segoe UI', 9, 'bold'))
        lbl.grid(row=current_row, column=current_col, sticky='e', padx=(10, 5), pady=3)
        
        en = tk.Entry(body, width=10, font=('Consolas', 11, 'bold'), relief='solid', borderwidth=1)
        if default_val:
            en.insert(0, default_val)
        
        # Binds de atalhos e cores
        en.bind("<FocusIn>", on_focus_in)
        en.bind("<FocusOut>", on_focus_out)
        en.bind("<Up>", move_up)
        en.bind("<Down>", move_down)
        
        en.grid(row=current_row, column=current_col+1, sticky='w', pady=3, padx=(0, 10))
        
        campos[key.upper()] = en
        current_row += 1

footer = tk.Frame(root, bg=BG_COLOR, pady=10)
footer.pack(fill='x')
btn = ttk.Button(footer, text="SUBMIT & PASTE (ENTER)", command=disparar_texto)
btn.pack(ipady=2, ipadx=10)

root.bind('<Return>', disparar_texto)
root.bind('<Escape>', lambda e: root.quit())

# Foca no primeiro campo ao abrir
first_field = list(campos.values())[0]
first_field.focus()

root.mainloop()f