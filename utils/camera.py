import cv2
import mediapipe as mp
import time

def capturar_medidas():
    """
    Captura medidas faciais usando a webcam. O retângulo maior captura mais detalhes do rosto.
    Texto dinâmico e estilizado orienta o usuário.
    :return: Dicionário com as medidas capturadas ou None em caso de falha.
    """
    webcam = cv2.VideoCapture(0)
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh()
    inicio_tempo = time.time()

    medidas = {}
    janela_camera = "Captura Facial"  # Nome da janela OpenCV

    while True:
        # Ler frame da webcam
        verificador, frame = webcam.read()
        if not verificador:
            print("Erro ao acessar a webcam.")
            break

        # Dimensões do frame
        altura, largura, _ = frame.shape

        # Aumentar o tamanho do retângulo
        margem = 150  # Valor ajustado para capturar mais detalhes do rosto
        retangulo_x1, retangulo_y1 = largura // 2 - margem, altura // 2 - margem
        retangulo_x2, retangulo_y2 = largura // 2 + margem, altura // 2 + margem

        # Processar o frame
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        # Determinar a cor do retângulo e a mensagem
        cor_retangulo = (0, 0, 255)  # Vermelho, padrão
        texto_status = "Posicione seu rosto dentro do quadrado"

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                pontos = face_landmarks.landmark
                dentro_retangulo = True

                # Verificar se todos os pontos estão dentro do retângulo
                for ponto in pontos:
                    ponto_x, ponto_y = int(ponto.x * largura), int(ponto.y * altura)
                    if not (retangulo_x1 <= ponto_x <= retangulo_x2 and retangulo_y1 <= ponto_y <= retangulo_y2):
                        dentro_retangulo = False
                        break

                # Se todos os pontos estão dentro, o retângulo fica verde e a mensagem muda
                if dentro_retangulo:
                    cor_retangulo = (0, 255, 0)  # Verde
                    texto_status = "Ótimo! Capturando medidas..."

                    # Capturar medidas apenas quando dentro do retângulo
                    olho_esquerdo = (int(pontos[33].x * largura), int(pontos[33].y * altura))
                    olho_direito = (int(pontos[263].x * largura), int(pontos[263].y * altura))
                    boca = (int(pontos[13].x * largura), int(pontos[13].y * altura))
                    nariz = (int(pontos[1].x * largura), int(pontos[1].y * altura))
                    testa = (int(pontos[10].x * largura), int(pontos[10].y * altura))
                    queixo = (int(pontos[152].x * largura), int(pontos[152].y * altura))
                    orelha_esquerda = (int(pontos[234].x * largura), int(pontos[234].y * altura))
                    orelha_direita = (int(pontos[454].x * largura), int(pontos[454].y * altura))

                    medidas = {
                        "olhos": cv2.norm(olho_esquerdo, olho_direito),
                        "boca_nariz": cv2.norm(boca, nariz),
                        "testa_queixo": cv2.norm(testa, queixo),
                        "orelha_orelha": cv2.norm(orelha_esquerda, orelha_direita),
                    }

        # Desenhar o retângulo
        cv2.rectangle(
            frame,
            (retangulo_x1, retangulo_y1),
            (retangulo_x2, retangulo_y2),
            cor_retangulo,
            2,
        )

        # Adicionar texto estilizado com sombra
        texto_x = largura // 2 - 200  # Centralizar horizontalmente
        texto_y = retangulo_y1 - 30  # Ajustado para o texto ficar acima do retângulo maior
        sombra_cor = (0, 0, 0)  # Preto para sombra

        # Sombra do texto
        cv2.putText(frame, texto_status, (texto_x + 2, texto_y + 2), cv2.FONT_HERSHEY_SIMPLEX, 0.8, sombra_cor, 3)
        # Texto principal
        cv2.putText(frame, texto_status, (texto_x, texto_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, cor_retangulo, 2)

        # Mostrar frame na janela OpenCV
        cv2.imshow(janela_camera, frame)

        # Sair ao pressionar ESC ou após 30 segundos
        if cv2.waitKey(5) == 27 or (time.time() - inicio_tempo) >= 30:
            break

    # Liberar recursos e fechar janela
    webcam.release()
    cv2.destroyAllWindows()

    return medidas if medidas else None
