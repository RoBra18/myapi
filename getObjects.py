'''
from ultralytics import YOLO
from PIL import Image

model = YOLO('yolo11x.pt')

def detectar_objetos_str(ruta_imagen: str) -> str:
    image = Image.open(ruta_imagen)
    results = model(image)[0]  # Ejecuta detección, toma el primer resultado
    
    descripcion = ""
    boxes = results.boxes
    total = len(boxes)
    if(total > 0):
        for i, box in enumerate(boxes):
            cls = int(box.cls[0])
            nombre = model.names[cls]
            confianza = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            bbox = (x1, y1, x2, y2)
            descripcion += f"Objeto: {nombre} | Confianza: {confianza:.2f} | Posición: {bbox}"
            if i < total - 1:
                descripcion += "\n"
    else:
        descripcion = "No se detectaron objetos en la escena"
    
    return descripcion
'''