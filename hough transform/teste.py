import cv2 as cv
import numpy as np

def main():
    # Carregar a imagem
    img = cv.imread("imagem7.jpg")
    if img is None:
        print('Error opening image!')
        return -1
    
    # Converter para o espaço de cores HSV
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # Definir a faixa de cor da caneta (exemplo: caneta azul)
    lower_blue = np.array([ 38, 126, 15])  # Ajuste conforme necessário
    upper_blue = np.array([ 58, 146, 230])  # Ajuste conforme necessário

    # Criar uma máscara para a cor da caneta
    mask = cv.inRange(hsv, lower_blue, upper_blue)

    edges= cv.Canny(mask, 55,200)

    lines=cv.HoughLinesP(edges,1,np.pi/180,4,maxLineGap=5)
    if lines is not None:   #linhas para videos -saber se ainda existe alguma linha
        for line in lines:
            x1,y1,x2,y2=line[0]
            cv.line(img,(x1,y1),(x2,y2),(0,255,0),5)









    """# Encontrar contornos na máscara
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Se houver contornos, desenhe um retângulo em torno do maior contorno
    if contours:
        largest_contour = max(contours, key=cv.contourArea)
        x, y, w, h = cv.boundingRect(largest_contour)
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Desenhar um retângulo verde"""

    # Mostrar a imagem original com a caneta detectada
    cv.imshow("Detected Pen", img)
    cv.imshow("edges", edges)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
