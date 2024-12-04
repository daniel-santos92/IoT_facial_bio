import tkinter as tk
from gui.login import tela_login
from gui.registro import tela_registro
from utils.logger import setup_logging
from utils.window_utils import centralizar_janela
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv(dotenv_path=".env")

# Configurar logs
debug_mode = os.getenv("DEBUG_MODE", "False").lower() == "true"
setup_logging(debug=debug_mode)

for key, value in os.environ.items():
    print(f"{key}: {value}")
    
def main():
    root = tk.Tk()
    root.title("Autenticação Facial")
    root.geometry("360x180")  # Tamanho inicial da janela

    # Centralizar a janela principal
    centralizar_janela(root)

    tk.Button(root, text="Login", command=lambda: tela_login(root)).pack(pady=10)
    tk.Button(root, text="Registrar", command=lambda: tela_registro(root)).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
