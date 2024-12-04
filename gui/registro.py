import logging
from tkinter import Toplevel, Label, Entry, Button, messagebox
from utils.camera import capturar_medidas
from utils.validation import validar_cpf
from firebase.firebase_utils import enviar_dados_firebase
from utils.window_utils import centralizar_janela


def tela_registro(root):
    """
    Cria a tela de registro do usuário.
    Permite o preenchimento do nome, CPF e captura de medidas faciais.
    """
    registro_window = Toplevel(root)
    registro_window.title("Registro de Usuário")
    registro_window.geometry("400x300")
    centralizar_janela(registro_window)

    # Labels e entradas para Nome e CPF
    Label(registro_window, text="Nome:").pack(pady=5)
    nome_entry = Entry(registro_window)
    nome_entry.pack(pady=5)

    Label(registro_window, text="CPF:").pack(pady=5)
    cpf_entry = Entry(registro_window)
    cpf_entry.pack(pady=5)

    # Função para processar o registro
    def processar_registro():
        nome = nome_entry.get().strip()
        cpf = cpf_entry.get().strip()

        if not nome or not validar_cpf(cpf):
            logging.warning("Tentativa de registro com campos inválidos: Nome ou CPF.")
            messagebox.showwarning("Atenção", "Preencha corretamente os campos Nome e CPF (11 dígitos).")
            return

        registrar_usuario(nome, cpf, registro_window)

    # Botões
    Button(registro_window, text="Capturar e Registrar", command=processar_registro).pack(pady=20)
    Button(registro_window, text="Cancelar", command=registro_window.destroy).pack(pady=10)


def registrar_usuario(nome, cpf, registro_window):
    """
    Captura as medidas faciais do usuário, valida os dados e registra no Firebase.
    """
    logging.info(f"Iniciando captura de medidas para o usuário: {nome} (CPF: {cpf})")

    # Criar janela para captura de medidas
    medidas_window = Toplevel(registro_window)
    medidas_window.title("Capturando Medidas")
    medidas_window.geometry("600x400")
    centralizar_janela(medidas_window)

    # Capturar medidas faciais
    medidas = capturar_medidas()
    medidas_window.destroy()  # Fechar a janela de captura

    if medidas:
        logging.info(f"Medidas capturadas com sucesso para o usuário {nome}: {medidas}")
        dados_usuario = {
            "nome_user": nome,
            "cpf_user": cpf,
            "olhos_user": medidas["olhos"],
            "boca_nariz_user": medidas["boca_nariz"],
            "testa_user": medidas["testa_queixo"],
            "orelha_user": medidas["orelha_orelha"]
        }

        # Enviar dados ao Firebase
        if enviar_dados_firebase("medida_usuarios", dados_usuario):
            logging.info(f"Dados do usuário {nome} enviados ao Firebase com sucesso.")
            messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
        else:
            logging.error(f"Erro ao enviar dados do usuário {nome} para o Firebase.")
            messagebox.showerror("Erro", "Erro ao registrar usuário no banco de dados.")
    else:
        logging.warning(f"Falha na captura de medidas para o usuário {nome}.")
        messagebox.showwarning("Atenção", "Falha na captura de medidas faciais.")
