import cv2 as cv
import numpy as np
import os

def numero_de_arquivos(caminho):
    arquivos = [f for f in os.listdir(caminho) if os.path.isfile(os.path.join(caminho, f))]
    return len(arquivos)
# Variáveis para desenhar
canvas = None
prev_point = None

cap = cv.VideoCapture(0)  # Captura de vídeo

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv.flip(frame, 1)  # Espelhar imagem

    # Converter para escala de cinza e suavizar
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)

    # Localizar o ponto mais brilhante
    minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(gray)

    # Criar o canvas na primeira iteração
    if canvas is None:
        canvas = np.zeros_like(frame)

    # Se o ponto mais brilhante for suficientemente claro
    if maxVal > 240:
        # Desenhar um círculo no ponto mais brilhante
        cv.circle(frame, maxLoc, 10, (0, 255, 0), -1)

        # Desenhar uma linha no canvas, apenas se prev_point for válido
        if prev_point is not None:
            cv.line(canvas, prev_point, maxLoc, (255, 0, 0), 5)

        # Atualizar prev_point para o próximo frame
        prev_point = maxLoc
    else:
        prev_point = None  # Resetar prev_point se o ponto mais brilhante não for encontrado

    # Combinar o canvas com o frame
    combinados = cv.add(frame, canvas)

    # Mostrar o resultado
    cv.imshow("imagem", combinados)

    # Detectar entrada do teclado
    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):  # Pressione 'q' para sair
        break
    elif key== ord("c"):
        canvas=None
    elif key==ord('s'):
        caminho = "C:/Users/luma/Desktop/desenhar/desenhos/"
        n=numero_de_arquivos(caminho)
        caminho = f"C:/Users/luma/Desktop/desenhar/desenhos/desenho{n}.png"
        cv.imwrite(caminho, canvas)
        print(f"Desenho salvo em: {caminho}")

cap.release()
cv.destroyAllWindows()
