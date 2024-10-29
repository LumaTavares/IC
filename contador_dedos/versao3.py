import cv2 as cv
import model
import time  # Importa a biblioteca time para medir o intervalo

# Define a resolução da câmera
wCam, hCam = 640, 480
cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Cria um objeto para detecção de mãos com um limite de confiança para detecção
detector = model.handDetector(detection_confidence=0.75)
tipIds = [4, 8, 12, 16, 20]

# Variável para armazenar a contagem anterior de dedos levantados e o tempo do último print
previousFingersCount = -1
lastPrintTime = time.time()  # Armazena o horário inicial

while True:
    # Captura o frame da câmera
    success, img = cap.read()
    img = detector.findhands(img)
    lmList = detector.findPosition(img, draw=False)

    # Verifica se há alguma posição de pontos da mão detectada
    if len(lmList) != 0:
        fingers = []

        # Verificação do polegar
        if lmList[tipIds[0]][1] < lmList[tipIds[4]][1]:
            if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        # Verificação dos outros dedos
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)

        # Verifica se 10 segundos se passaram desde o último print
        currentTime = time.time()
        if currentTime - lastPrintTime >= 5:
            print(totalFingers)  # Imprime a contagem de dedos levantados
            lastPrintTime = currentTime  # Atualiza o tempo do último print

    # Exibe a imagem com as mãos detectadas
    cv.imshow("Image", img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

