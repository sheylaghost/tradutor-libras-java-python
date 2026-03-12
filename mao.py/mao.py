import cv2
import mediapipe as mp
import socket

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 9999))
server.listen(1)
print("Aguardando conexao do Java...")
conn, addr = server.accept()
print("Java conectado!")

cap = cv2.VideoCapture("http://192.168.0.23:4747/video")

def dedos_levantados(lm):
    dedos = []
    # Polegar
    dedos.append(1 if lm[4].x < lm[3].x else 0)
    # Outros 4 dedos
    for tip, pip in [(8,6), (12,10), (16,14), (20,18)]:
        dedos.append(1 if lm[tip].y < lm[pip].y else 0)
    return dedos

def identificar_letra(dedos):
    d = dedos
    if d == [0,0,0,0,0]: return "A"
    if d == [0,1,1,1,1]: return "B"
    if d == [1,1,1,1,1]: return "5"
    if d == [0,1,0,0,0]: return "D"
    if d == [0,1,1,0,0]: return "V"
    if d == [1,1,0,0,0]: return "L"
    if d == [0,0,0,0,1]: return "I"
    if d == [1,0,0,0,1]: return "Y"
    if d == [1,1,1,0,0]: return "3"
    if d == [0,1,1,1,0]: return "W"
    return "?"

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = hands.process(rgb)

    dados = "NENHUMA_MAO"
    letra = ""

    if resultado.multi_hand_landmarks:
        for hand_landmarks in resultado.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            lm = hand_landmarks.landmark
            dedos = dedos_levantados(lm)
            letra = identificar_letra(dedos)

            cv2.putText(frame, f"Letra: {letra}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

            pontos = []
            for l in lm:
                pontos.append(f"{l.x:.4f},{l.y:.4f}")
            dados = letra + "|" + ";".join(pontos)

    try:
        conn.sendall((dados + "\n").encode())
    except:
        break

    cv2.imshow("Tradutor de Libras", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
conn.close()
server.close()