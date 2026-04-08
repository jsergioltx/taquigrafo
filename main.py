import tkinter as tk
import pyautogui
import pyperclip
import time

def disparar_texto(event=None):
    resultados = []
    for label, entry in campos.items():
        valor = entry.get().strip()
        if valor:
            resultados.append(f"{label} {valor}")
    
    if not resultados:
        return

    # Formata como você gosta
    texto_final = " / ".join(resultados)
    
    # Copia para a área de transferência
    pyperclip.copy(texto_final)
    
    # Limpa os campos para o próximo paciente
    for entry in campos.values():
        entry.delete(0, tk.END)
    campos[labels[0]].focus() # Volta o cursor pro primeiro campo
    
    # Minimiza a janela (isso devolve o foco para o prontuário no Windows)
    root.iconify()
    
    # Espera meio segundo para o Windows processar a troca de janelas
    time.sleep(0.5)
    
    # Simula o teclado colando o texto onde o cursor estiver piscando
    pyautogui.hotkey('ctrl', 'v')

root = tk.Tk()
root.title("ESF")
root.attributes('-topmost', True) # Mantém sempre no topo

# Lista dos seus exames
labels = ["HB", "HT", "GL", "S", "L", "P", "VDRL", "HBSAG", "HCV", "HIV", "TSH", "CR"]
campos = {}

for i, L in enumerate(labels):
    tk.Label(root, text=L, font=('Arial', 10, 'bold')).grid(row=i, column=0, padx=5, pady=2, sticky='e')
    en = tk.Entry(root, width=15)
    en.grid(row=i, column=1, padx=5, pady=2)
    campos[L] = en

# Botão invisível acionado pelo Enter
root.bind('<Return>', disparar_texto)

root.mainloop()