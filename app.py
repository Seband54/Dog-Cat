from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Inicializar la cámara
camera = cv2.VideoCapture(0)  # 0 = cámara predeterminada

def gen_frames():
    while True:
        success, frame = camera.read()  # Leer frame de la cámara
        if not success:
            break
        else:
            # 🔥 Aquí es donde pondrás tu IA para predecir perro/gato
            label = "Gato"  # Solo de ejemplo
            # Dibujamos la etiqueta en el frame
            cv2.putText(frame, label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0, 255, 0), 2, cv2.LINE_AA)

            # Codificar la imagen como JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Usamos yield para hacer streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    # Renderizar una simple página que muestre el stream
    return render_template('index.html')

@app.route('/video')
def video():
    # Devuelve el streaming de la cámara
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
