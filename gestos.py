# Importação de Bibliotecas
import cv2  # OpenCV para processamento de imagem
import mediapipe as mp  # MediaPipe para detecção de mãos
import numpy as np  # NumPy para manipulação de arrays
import math  # Biblioteca matemática para cálculos
import time  # Biblioteca para medição de tempo
from ctypes import cast, POINTER  # Para manipulação de áudio
from comtypes import CLSCTX_ALL  # Para manipulação de áudio
from pycaw.pycaw import *  # Para manipulação de áudio

# Obtenção dos dispositivos de áudio e inicialização da interface para controlar o volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
vc = cast(interface, POINTER(IAudioEndpointVolume))
Range = vc.GetVolumeRange()
minR, maxR = Range[0], Range[1]

# Inicialização do MediaPipe para detecção de mãos
mpHands = mp.solutions.hands
Hands = mpHands.Hands()
# Para desenhar os pontos de referência das mãos
mpDraw = mp.solutions.drawing_utils
PTime = 0  # Variável para armazenar o tempo anterior
vol = 0  # Variável para armazenar o volume
volBar = 400  # Variável para representar a posição da barra de volume
volPer = 0  # Variável para representar a porcentagem do volume
cap = cv2.VideoCapture(0)  # Inicialização da captura de vídeo da câmera

# Loop principal
while (cap.isOpened()):
    lmList = []  # Lista para armazenar os pontos de referência das mãos
    success, img = cap.read()  # Leitura de um frame da câmera
    # Conversão do formato de cores do frame
    converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Processamento do frame para detecção de mãos
    results = Hands.process(converted_image)

    if results.multi_hand_landmarks:
        # Desenho dos pontos de referência e conexões das mãos no frame
        for hand_in_frame in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, hand_in_frame, mpHands.HAND_CONNECTIONS)

        # Extração dos pontos de referência das mãos
        for id, lm in enumerate(results.multi_hand_landmarks[0].landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            lmList.append([cx, cy])

        if len(lmList) != 0:
            # Cálculo do comprimento entre dois pontos de referência para estimar o gesto da mão
            x1, y1 = lmList[4][0], lmList[4][1]
            x2, y2 = lmList[8][0], lmList[8][1]

            # Desenho de elementos visuais para representar os dedos
            cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3, cv2.FILLED)
            # Comprimento do gesto da mão
            length = math.hypot(x2-x1-30, y2-y1-30)

            # Interpolação do comprimento para ajustar o volume
            vol = np.interp(length, [50, 300], [minR, maxR])
            volBar = np.interp(length, [50, 300], [400, 150])
            volPer = np.interp(length, [50, 300], [0, 100])

            # Desenho da barra de volume e texto representando o volume atual
            cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0))
            cv2.rectangle(img, (50, int(volBar)), (85, 400),
                          (255, 0, 0), cv2.FILLED)
            cv2.putText(img, f'{int(volPer)} %', (85, 450),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
            vc.SetMasterVolumeLevel(vol, None)  # Ajuste do volume do sistema

    # Cálculo e exibição da taxa de quadros por segundo (FPS)
    CTime = time.time()
    fps = 1/(CTime-PTime)
    PTime = CTime
    cv2.putText(img, str(int(fps)), (40, 50),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # Exibição do frame
    cv2.imshow("Hand Tracking", img)

    # Condição de saída do loop
    if cv2.waitKey(1) == 113:  # 113 - Q
        break
