import cv2
import mediapipe as mp
import time

def capturar_medidas():
    """
    Captura medidas faciais usando a webcam. Otimizado para eficiência com processamento seletivo de frames.
    :return: Dicionário com as medidas capturadas ou None em caso de falha.
    """
    webcam = cv2.VideoCapture(0)
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    inicio_tempo = time.time()
    tempo_maximo = 10  # Tempo máximo de captura (em segundos)

    medidas = {}
    janela_camera = "Captura Facial"
    frame_interval = 3  # Processar 1 em cada 3 frames
    frame_count = 0

    while True:
        # Ler frame da webcam
        verificador, frame = webcam.read()
        if not verificador:
            print("Erro ao acessar a webcam.")
            break

        # Reduzir resolução para acelerar processamento
        frame_redimensionado = cv2.resize(frame, (640, 480))
        altura, largura, _ = frame_redimensionado.shape

        # Configurar retângulo
        margem = 150
        retangulo_x1, retangulo_y1 = largura // 2 - margem, altura // 2 - margem
        retangulo_x2, retangulo_y2 = largura // 2 + margem, altura // 2 + margem

        # Processar apenas 1 em cada `frame_interval` frames
        frame_count += 1
        if frame_count % frame_interval != 0:
            # Mostrar o retângulo mesmo sem processar
            cv2.rectangle(
                frame_redimensionado,
                (retangulo_x1, retangulo_y1),
                (retangulo_x2, retangulo_y2),
                (0, 0, 255),  # Vermelho por padrão
                2,
            )
            cv2.imshow(janela_camera, frame_redimensionado)
            if cv2.waitKey(5) == 27:
                break
            continue

        # Converter para RGB e processar o frame
        rgb_frame = cv2.cvtColor(frame_redimensionado, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        cor_retangulo = (0, 0, 255)  # Vermelho por padrão
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

                # Se todos os pontos estão dentro, capturar medidas
                if dentro_retangulo:
                    cor_retangulo = (0, 255, 0)  # Verde
                    texto_status = "Ótimo! Capturando medidas..."
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
                    break  # Parar o loop quando as medidas forem capturadas

        # Desenhar o retângulo
        cv2.rectangle(
            frame_redimensionado,
            (retangulo_x1, retangulo_y1),
            (retangulo_x2, retangulo_y2),
            cor_retangulo,
            2,
        )

        # Adicionar texto
        cv2.putText(
            frame_redimensionado,
            texto_status,
            (retangulo_x1, retangulo_y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            cor_retangulo,
            2,
        )

        # Mostrar frame na janela OpenCV
        cv2.imshow(janela_camera, frame_redimensionado)

        # Sair ao pressionar ESC ou após tempo máximo
        if cv2.waitKey(5) == 27 or (time.time() - inicio_tempo) >= tempo_maximo or medidas:
            break

    # Liberar recursos e fechar janela
    webcam.release()
    cv2.destroyAllWindows()

    return medidas if medidas else None
