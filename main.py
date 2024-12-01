import requests
import json
import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time

# Configuração Firebase
firebase_url = "https://pythonfirebase-a5fcd-default-rtdb.firebaseio.com/"

# Função para enviar dados ao Firebase
def enviar_dados_firebase(tabela, dados):
    response = requests.post(f'{firebase_url}/{tabela}/.json', data=json.dumps(dados))
    return response.ok

# Função para capturar medidas faciais com limite de 30 segundos ou até ESC
def capturar_medidas():
    webcam = cv2.VideoCapture(0)
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh()
    inicio_tempo = time.time()

    medidas = {}

    while True:
        verificador, frame = webcam.read()
        if not verificador:
            break

        altura, largura, _ = frame.shape
        margem = 100
        cv2.rectangle(frame, 
                      (largura // 2 - margem, altura // 2 - margem), 
                      (largura // 2 + margem, altura // 2 + margem), 
                      (0, 255, 0), 2)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                pontos = face_landmarks.landmark

                olho_esquerdo = (int(pontos[33].x * largura), int(pontos[33].y * altura))
                olho_direito = (int(pontos[263].x * largura), int(pontos[263].y * altura))
                boca = (int(pontos[13].x * largura), int(pontos[13].y * altura))
                nariz = (int(pontos[1].x * largura), int(pontos[1].y * altura))
                testa = (int(pontos[10].x * largura), int(pontos[10].y * altura))
                queixo = (int(pontos[152].x * largura), int(pontos[152].y * altura))
                orelha_esquerda = (int(pontos[234].x * largura), int(pontos[234].y * altura))
                orelha_direita = (int(pontos[454].x * largura), int(pontos[454].y * altura))

                medidas = {
                    "olhos": np.linalg.norm(np.array(olho_esquerdo) - np.array(olho_direito)),
                    "boca_nariz": np.linalg.norm(np.array(boca) - np.array(nariz)),
                    "testa_queixo": np.linalg.norm(np.array(testa) - np.array(queixo)),
                    "orelha_orelha": np.linalg.norm(np.array(orelha_esquerda) - np.array(orelha_direita))
                }

                cv2.imshow("Rostos da webcam", frame)

        # Condições de saída: ESC pressionado ou 30 segundos passados
        if cv2.waitKey(5) == 27 or (time.time() - inicio_tempo) >= 30:
            break

    webcam.release()
    cv2.destroyAllWindows()
    return medidas

# Tela de Cadastro de Usuário
def tela_registro():
    registro_window = tk.Toplevel(root)
    registro_window.title("Registro de Usuário")

    def registrar_usuario():
        nome = nome_entry.get()
        cpf = cpf_entry.get()
        medidas = capturar_medidas()

        if nome and cpf and medidas:
            dados_usuario = {
                "nome_user": nome,
                "cpf_user": cpf,
                "olhos_user": medidas["olhos"],
                "boca_nariz_user": medidas["boca_nariz"],
                "testa_user": medidas["testa_queixo"],
                "orelha_user": medidas["orelha_orelha"]
            }
            if enviar_dados_firebase("medida_usuarios", dados_usuario):
                messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao registrar usuário no banco de dados.")
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos e capture as medidas.")

    tk.Label(registro_window, text="Nome:").pack()
    nome_entry = tk.Entry(registro_window)
    nome_entry.pack()

    tk.Label(registro_window, text="CPF:").pack()
    cpf_entry = tk.Entry(registro_window)
    cpf_entry.pack()

    tk.Button(registro_window, text="Registrar e Capturar Medidas", command=registrar_usuario).pack()

# Função para comparar as medidas faciais com a margem de erro
def medidas_sao_compatíveis(medidas_capturadas, medidas_salvas, margem=0.15):
    for key in medidas_capturadas:
        if not (1 - margem) * medidas_salvas[key] <= medidas_capturadas[key] <= (1 + margem) * medidas_salvas[key]:
            return False
    return True

# Tela de Login
def tela_login():
    medidas_capturadas = capturar_medidas()

    if medidas_capturadas:
        # Obter todos os usuários cadastrados
        response = requests.get(f"{firebase_url}/medida_usuarios.json")
        usuarios = response.json()

        for user_id, dados_usuario in usuarios.items():
            medidas_salvas = {
                "olhos": dados_usuario["olhos_user"],
                "boca_nariz": dados_usuario["boca_nariz_user"],
                "testa_queixo": dados_usuario["testa_user"],
                "orelha_orelha": dados_usuario["orelha_user"]
            }

            if medidas_sao_compatíveis(medidas_capturadas, medidas_salvas):
                # Registrar o check-in
                checkin_data = {
                    "cpf": dados_usuario["cpf_user"],
                    "horario_checkin": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                if enviar_dados_firebase("checkin_user", checkin_data):
                    messagebox.showinfo("Login bem-sucedido", f"Bem-vindo, {dados_usuario['nome_user']}!")
                else:
                    messagebox.showerror("Erro", "Erro ao registrar o check-in.")
                return

        messagebox.showerror("Erro", "Login não reconhecido. Medidas faciais não correspondem.")

# Tela Inicial com botões de Login e Registro
root = tk.Tk()
root.title("Autenticação Facial")
root.geometry("360x180")

tk.Button(root, text="Login", command=tela_login).pack(pady=10)
tk.Button(root, text="Registrar", command=tela_registro).pack(pady=10)

root.mainloop()