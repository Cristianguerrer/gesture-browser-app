import cv2
import mediapipe as mp
import keyboard
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

print("🎥 Usando cámara en el índice 0")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ No se pudo abrir la cámara.")
    exit()

zona_muerta_porcentaje = 0.10
z_presionada = False
flecha_izq_activa = False
flecha_der_activa = False

def is_fist(landmarks):
    finger_tips = [8, 12, 16, 20]
    folded = 0
    for tip in finger_tips:
        if landmarks[tip].y > landmarks[tip - 2].y:
            folded += 1
    return folded == 4

def is_index_only_extended(landmarks):
    index_extended = landmarks[8].y < landmarks[6].y
    middle_folded = landmarks[12].y > landmarks[10].y
    ring_folded = landmarks[16].y > landmarks[14].y
    pinky_folded = landmarks[20].y > landmarks[18].y
    return index_extended and middle_folded and ring_folded and pinky_folded

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    if not ret:
        print("❌ No se pudo leer el frame.")
        break

    height, width, _ = img.shape
    centro_pantalla = width // 2
    zona_muerta_px = int(width * zona_muerta_porcentaje)

    cv2.line(img, (centro_pantalla, 0), (centro_pantalla, height), (255, 255, 255), 2)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm = hand_landmarks.landmark

            hand_x_px = int(lm[0].x * width)

            # 🔄 CORREGIDO: invertir lógica de izquierda y derecha
            if hand_x_px < centro_pantalla - zona_muerta_px:
                if not flecha_izq_activa:
                    pyautogui.keyDown('left')
                    flecha_izq_activa = True
                if flecha_der_activa:
                    pyautogui.keyUp('right')
                    flecha_der_activa = False
                cv2.putText(img, 'Mano a la IZQUIERDA → FLECHA IZQ', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 255), 2)

            elif hand_x_px > centro_pantalla + zona_muerta_px:
                if not flecha_der_activa:
                    pyautogui.keyDown('right')
                    flecha_der_activa = True
                if flecha_izq_activa:
                    pyautogui.keyUp('left')
                    flecha_izq_activa = False
                cv2.putText(img, 'Mano a la DERECHA → FLECHA DER', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 255, 200), 2)

            else:
                if flecha_izq_activa:
                    pyautogui.keyUp('left')
                    flecha_izq_activa = False
                if flecha_der_activa:
                    pyautogui.keyUp('right')
                    flecha_der_activa = False
                cv2.putText(img, 'Zona central (sin movimiento)', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 255), 2)

            # ✊ Puño → A
            if is_fist(lm):
                keyboard.press('a')
                z_presionada = False
                cv2.putText(img, 'Puño -> A', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            # ✊ + ☝️ Índice → A + Z (Z una sola vez)
            elif is_index_only_extended(lm):
                keyboard.press('a')  # mantener A
                if not z_presionada:
                    pyautogui.keyDown('z')
                    time.sleep(0.1)
                    pyautogui.keyUp('z')
                    z_presionada = True
                cv2.putText(img, 'Puño + índice → A + Z (una vez)', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

            else:
                keyboard.release('a')
                z_presionada = False
                cv2.putText(img, 'Mano abierta', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    else:
        keyboard.release('a')
        z_presionada = False
        if flecha_izq_activa:
            pyautogui.keyUp('left')
            flecha_izq_activa = False
        if flecha_der_activa:
            pyautogui.keyUp('right')
            flecha_der_activa = False

    cv2.imshow("Control por gestos", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
