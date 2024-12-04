import logging
from tkinter import Toplevel, messagebox
from utils.camera import capturar_medidas
from firebase.firebase_utils import obter_dados_firebase

def medidas_sao_compatíveis(medidas_capturadas, medidas_salvas, margem=0.15):
    """
    Compara medidas capturadas com medidas salvas, considerando uma margem de erro.
    Retorna True se forem compatíveis, False caso contrário.
    """
    for key in medidas_capturadas:
        capturada = medidas_capturadas[key]
        salva = medidas_salvas[key]
        if not (1 - margem) * salva <= capturada <= (1 + margem) * salva:
            logging.debug(f"Incompatível na medida '{key}': capturada={capturada}, salva={salva}")
            return False
    return True

def tela_login(root):
    login_window = Toplevel(root)
    login_window.title("Login")
    login_window.geometry("360x200")

    # Capturar medidas do usuário atual
    logging.info("Iniciando captura de medidas para login.")
    medidas_capturadas = capturar_medidas()

    if not medidas_capturadas:
        messagebox.showerror("Erro", "Não foi possível capturar medidas faciais.")
        logging.error("Falha na captura de medidas faciais.")
        return

    # Obter dados dos usuários salvos
    usuarios = obter_dados_firebase("medida_usuarios")
    if not usuarios:
        messagebox.showerror("Erro", "Erro ao acessar o banco de dados.")
        logging.error("Nenhum usuário encontrado no banco de dados.")
        return

    logging.debug(f"Medidas capturadas: {medidas_capturadas}")
    logging.debug(f"Usuários carregados do Firebase: {usuarios}")

    # Comparar medidas capturadas com as medidas dos usuários
    for user_id, dados_usuario in usuarios.items():
        medidas_salvas = {
            "olhos": dados_usuario["olhos_user"],
            "boca_nariz": dados_usuario["boca_nariz_user"],
            "testa_queixo": dados_usuario["testa_user"],
            "orelha_orelha": dados_usuario["orelha_user"]
        }

        if medidas_sao_compatíveis(medidas_capturadas, medidas_salvas):
            # Login bem-sucedido
            nome_usuario = dados_usuario["nome_user"]
            logging.info(f"Usuário reconhecido: {nome_usuario}")
            messagebox.showinfo("Login bem-sucedido", f"Bem-vindo, {nome_usuario}!")
            return

    # Caso nenhuma correspondência seja encontrada
    logging.warning("Nenhuma correspondência encontrada para as medidas capturadas.")
    messagebox.showerror("Erro", "Login não reconhecido. Medidas faciais não correspondem.")
