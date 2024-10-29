# Importa as bibliotecas necessárias
import cv2 as cv  # OpenCV para manipulação de imagem e vídeo
import mediapipe as mp  # MediaPipe para detecção de mãos

# Classe para detectar mãos usando MediaPipe
class handDetector():
    def __init__(self, mode=False, maxHands=1, modelComplexity=1, detection_confidence=0.5, tracking_confidence=0.5):
        # Inicializa parâmetros para detecção de mãos
        self.mode = mode  # Modo de imagem estática ou fluxo contínuo
        self.maxHands = maxHands  # Número máximo de mãos a detectar
        self.detection_confidence = detection_confidence  # Confiabilidade mínima para detecção inicial
        self.tracking_confidence = tracking_confidence  # Confiabilidade mínima para rastreamento de mãos detectadas
        self.modelComplexity = modelComplexity
        
        # Inicializa o módulo de mãos do MediaPipe
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,  # Define se é uma imagem estática
            max_num_hands=self.maxHands,  # Número máximo de mãos
            model_complexity=self.modelComplexity,  # Complexidade do modelo
            min_detection_confidence=self.detection_confidence,  # Confiança mínima para detecção
            min_tracking_confidence=self.tracking_confidence  # Confiança mínima para rastreamento
        )
        
        # Utilitário de desenho do MediaPipe para desenhar as conexões das mãos
        self.mpDraw = mp.solutions.drawing_utils

    # Função para encontrar as mãos na imagem e desenhar conexões (opcional)
    def findhands(self, img, draw=True):
        # Converte a imagem BGR para RGB, pois MediaPipe usa imagens RGB
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        # Processa a imagem para detectar as mãos
        self.results = self.hands.process(imgRGB)
        
        # Verifica se alguma mão foi detectada
        if self.results.multi_hand_landmarks:
            # Itera sobre cada mão detectada
            for handLms in self.results.multi_hand_landmarks:
                # Desenha as conexões das mãos, se 'draw' for True
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        # Retorna a imagem com as conexões desenhadas (se aplicável)
        return img
    
    # Função para encontrar a posição dos pontos de referência da mão
    def findPosition(self, img, handNo=0, draw=True):
        lmList = []  # Lista para armazenar as coordenadas dos pontos de referência
        # Verifica se existem pontos de referência detectados
        if self.results.multi_hand_landmarks:
            # Seleciona a mão específica
            myHand = self.results.multi_hand_landmarks[handNo]
            # Itera sobre os pontos de referência e calcula as coordenadas em pixels
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])  # Adiciona o ID do ponto e suas coordenadas
                # Desenha um círculo em cada ponto se 'draw' for True
                if draw:
                    cv.circle(img, (cx, cy), 7, (255, 0, 255), cv.FILLED)
        return lmList  # Retorna a lista de pontos de referência

# Função principal para capturar vídeo e aplicar a detecção de mãos
def main():
    # Inicia a captura de vídeo (câmera)
    cap = cv.VideoCapture(0)
    # Define a largura e altura da captura de vídeo (opcional)
    cap.set(3, 640)  # Largura
    cap.set(4, 480)  # Altura
    # Cria um objeto de detecção de mãos
    detector = handDetector()

    # Loop principal para processar cada frame da câmera
    while True:
        # Lê um frame da câmera
        success, img = cap.read()
        if not success:  # Verifica se a captura falhou
            print("Falha ao capturar a imagem")
            break
        # Aplica a detecção de mãos no frame
        img = detector.findhands(img)
        # Obtém a lista de pontos de referência da mão
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])  # Exibe a posição do ponto de referência com ID 4 (dedo polegar)
        
        # Mostra o frame na tela
        cv.imshow("Image", img)
        # Sai do loop se a tecla 'q' for pressionada
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera a câmera e fecha todas as janelas do OpenCV
    cap.release()
    cv.destroyAllWindows()

# Executa a função principal se o script for executado diretamente
if __name__ == "__main__":
    main()
