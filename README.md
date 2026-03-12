# LibrasVision — Real-time hand gesture detection for Brazilian Sign Language (Libras) using Java + Python/MediaPipe


![Image](https://github.com/user-attachments/assets/5db2e0df-b6f8-485a-8a3b-b8040eaecbc8)


🌍 Why it matters / Por que importa

In Brazil, over 10 million people have hearing impairment. Libras is their official language since 2002. LibrasVision uses AI to bridge the communication gap between the deaf community and the hearing world.

No Brasil, mais de 10 milhões de pessoas possuem deficiência auditiva. A Libras é sua língua oficial desde 2002. O LibrasVision usa IA para reduzir a barreira de comunicação entre a comunidade surda e o mundo ouvinte.

🏗️ How it works / Como funciona
Phone Camera (DroidCam)
        │ Wi-Fi Stream
        ▼
Python (MediaPipe) ──── detects 21 hand points + identifies letter
        │ TCP Socket :9999
        ▼
Java (JavaCV) ──── renders video + displays translated letter
Python handles AI detection. Java handles display. They communicate via TCP socket on port 9999 — Python sends the detected letter and hand coordinates every frame, Java reads and renders them.

🚀 How to run / Como rodar

bash# 1. Install Python deps

pip install mediapipe==0.10.13 opencv-python

# 2. Update your phone IP in mao.py

cap = cv2.VideoCapture("http://YOUR_IP:4747/video")

# 3. Run Python FIRST

python mao.py

# 4. Then run Java (IntelliJ)

# libras.java

⚠️ Always start Python before Java. Do not open DroidCam Client — Java connects directly via IP.


🤙 Supported gestures / Gestos suportados

LetterFingers upANone (fist)BIndex, Middle, Ring, Pinky5AllVIndex, MiddleLThumb, IndexIPinky onlyYThumb, Pinky

🔮 Future / Futuro

Full Libras alphabet with ML model

Word and sentence recognition

Text-to-speech output

Mobile app


<div align="center">
Made with 🤟 for the deaf community / Feito com 🤟 para a comunidade surda
</div>
