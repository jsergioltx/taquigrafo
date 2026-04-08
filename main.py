import tkinter as tk
from tkinter import ttk
import pyautogui
import pyperclip
import time
import configparser
import os
import sys

# Descobre a pasta onde o .exe está rodando
if getattr(sys, 'frozen', False):
    app_path = os.path.dirname(sys.executable)
else:
    app_path = os.path.dirname(os.path.abspath(__file__))

config_file = os.path.join(app_path, 'config.ini')
config = configparser.ConfigParser()

# Exames pré-configurados que você pediu (com valores padrão)
default_exams = {
    # Hemograma
    'HB': '', 'HT': '', 'GL': '', 'S': '', 'L': '', 'P': '',
    # Perfil Lipídico
    'CT': '', 'HDL': '', 'LDL': '', 'TG': '',
    # Perfil Glicêmico
    'GLI': '', 'A1C': '',
    # Função Renal e Eletrólitos
    'CR': '', 'AC UR': '', 'K': '', 'NA': '',
    # Função Hepática
    'TGO': '', 'TGP': '', 'GGT': '', 'FALC': '',
    # Vitaminas e Hormônios
    'TSH': '', '25OHD': '', 'B12': '',
    # Urina e Parasitológico
    'EAS': 'NDN', 'MIF': 'NEG', 'PSOF': 'NEG',
    # Sorologias
    'HCV': 'NR', 'HBSAG': 'NR', 'VDRL': 'NR', 'HIV': 'NR'
}

# Se não existir o config.ini, cria um com os padrões
if not os.path.exists(config_file):
    config['EXAMES'] = default_exams
    with open(config_file, 'w') as configfile:
        config.write(configfile)

# Lê o arquivo de configuração
config.read(config_file)
exames_config = config['EXAMES']

def disparar_texto(event=None):
    resultados = []
    for label, entry in campos.items():
        valor = entry.get().strip()
        if valor: # Só entra se não estiver em branco
            resultados.append(f"{label} {valor}")
    
    if resultados:
        texto_final = " / ".join(resultados) + " /"
        pyperclip.copy(texto_final)
    
    # Esconde a janela e foca no prontuário que estava atrás
    root.withdraw()
    time.sleep(0.3) # Tempo crítico para o Windows trocar o foco de janela
    
    if resultados:
        pyautogui.hotkey('ctrl', 'v')
    
    # Encerra o programa
    root.quit()

# --- Configuração da Interface (Estilo "Gov/Profissional") ---
root = tk.Tk()
root.title("Medical Lab Entry - Dept. 42")
root.attributes('-topmost', True)
root.resizable(False, False)

# Tema profissional
style = ttk.Style(root)
if 'clam' in style.theme_names():
    style.theme_use('clam')

# Cores e Fontes Estilo "Sistema Federal"
BG_COLOR = "#e8ecef"
HEADER_BG = "#2c3e50"
root.configure(bg=BG_COLOR)

# Cabeçalho
header = tk.Frame(root, bg=HEADER_BG, pady=10)
header.pack(fill='x')
tk.Label(header, text="LABORATORY DATA ENTRY SYSTEM", fg="white", bg=HEADER_BG, font=('Segoe UI', 11, 'bold')).pack()

# Container Principal
body = tk.Frame(root, bg=BG_COLOR, padx=20, pady=15)
body.pack(fill='both', expand=True)

campos = {}
MAX_ROWS = 12 # Quebra em colunas a cada 12 exames para não ficar muito alto

for i, (label_text, default_val) in enumerate(exames_config.items()):
    col = (i // MAX_ROWS) * 2
    row = i % MAX_ROWS
    
    # Rótulo (Label)
    lbl = ttk.Label(body, text=f"{label_text.upper()}:", background=BG_COLOR, font=('Segoe UI', 9, 'bold'))
    lbl.grid(row=row, column=col, sticky='e', padx=(15 if col > 0 else 0, 5), pady=4)
    
    # Campo de Texto (Entry)
    en = ttk.Entry(body, width=12, font=('Consolas', 10))
    en.insert(0, default_val) # Preenche com o valor padrão do .ini
    en.grid(row=row, column=col+1, sticky='w', pady=4)
    
    # Seleciona o texto se tiver valor padrão, para facilitar sobrescrever
    if default_val:
        en.bind("<FocusIn>", lambda e, widget=en: widget.select_range(0, tk.END))
        
    campos[label_text.upper()] = en

# Botão de Ação
footer = tk.Frame(root, bg=BG_COLOR, pady=10)
footer.pack(fill='x')
btn = ttk.Button(footer, text="SUBMIT & PASTE (ENTER)", command=disparar_texto)
btn.pack(ipady=2, ipadx=10)

root.bind('<Return>', disparar_texto)
root.bind('<Escape>', lambda e: root.quit()) # Esc fecha sem fazer nada

# Foca no primeiro campo ao abrir
first_field = list(campos.values())[0]
first_field.focus()

root.mainloop()