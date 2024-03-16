# Controle de volume por meio de gestos das mãos 

Este é um projeto de controle de volume baseado em gestos de mão usando Python e a biblioteca MediaPipe. Ele permite controlar o volume do sistema operacional ajustando a distância entre dois dedos na frente da câmera.

## Requisitos

- Python 3.x
- OpenCV (`opencv-python`)
- MediaPipe (`mediapipe`)
- NumPy (`numpy`)
- PyCaw (`pycaw`)
- Comtypes (`comtypes`)

## Instalação

1. Certifique-se de ter Python 3.x instalado em seu sistema.
2. Instale as dependências usando pip:
   ```
   pip install opencv-python mediapipe numpy pycaw comtypes
   ```

## Como Usar

1. Execute o script `hand_gesture_volume_control.py`.
2. A câmera do seu computador será ativada.
3. Mantenha sua mão na frente da câmera.
4. Abra e feche os dedos para aumentar ou diminuir o volume do sistema.
5. Pressione a tecla 'Q' para sair do programa.

## Atalhos de Teclado

- Pressione 'Q' para sair do programa.

## Notas

- Certifique-se de que sua câmera esteja configurada corretamente e tenha boa iluminação para melhor detecção das mãos.
- Os gestos de mão podem variar em diferentes condições de iluminação e posições da câmera.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir problemas ou enviar solicitações de recebimento.
