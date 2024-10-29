# Importa a biblioteca OpenCV para manipulação de imagens e vídeo e o modelo de detecção de mão
import cv2 as cv
import model 

# Define a resolução da câmera
wCam, hCam = 640, 480
cap = cv.VideoCapture(0)  # Inicia a captura de vídeo da câmera padrão (ID 0)
cap.set(3, wCam)  # Define a largura da câmera
cap.set(4, hCam)  # Define a altura da câmera

# Cria um objeto para detecção de mãos com um limite de confiança para detecção
detector = model.handDetector(detection_confidence=0.75)
# Lista de IDs das pontas dos dedos (polegar, indicador, médio, anelar e mindinho)
tipIds = [4, 8, 12, 16, 20]

# Variável para armazenar a contagem anterior de dedos levantados
previousFingersCount = -1  # Inicializamos com -1 para garantir que a primeira contagem seja impressa

# Loop principal do programa
while True:
    # Captura o frame da câmera
    success, img = cap.read()
    # Encontra e desenha as mãos detectadas na imagem
    img = detector.findhands(img)
    # Obtém a lista de posições dos pontos da mão
    lmList = detector.findPosition(img, draw=False)

    # Verifica se há alguma posição de pontos da mão detectada
    if len(lmList) != 0:
        fingers = []  # Lista para armazenar o estado de cada dedo (levantado ou não)

        # Verificação do polegar
        if lmList[tipIds[0]][1] < lmList[tipIds[4]][1]:  # Para uma mão com polegar à esquerda
            if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:  # Se o polegar está "levantado"
                fingers.append(1)
            else:
                fingers.append(0)
        else:  # Para uma mão com polegar à direita
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:  # Se o polegar está "levantado"
                fingers.append(1)
            else:
                fingers.append(0)

        # Verificação dos outros dedos, baseado na posição vertical
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # Conta o total de dedos levantados na lista 'fingers'
        totalFingers = fingers.count(1)
        
        # Verifica se a contagem mudou em relação ao estado anterior
        if totalFingers != previousFingersCount:
            print(totalFingers)  # Imprime a contagem de dedos levantados
            previousFingersCount = totalFingers  # Atualiza a contagem anterior

    # Exibe a imagem com as mãos detectadas
    cv.imshow("Image", img)
    # Se a tecla 'q' for pressionada, o loop é encerrado
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha todas as janelas
cap.release()
cv.destroyAllWindows()
