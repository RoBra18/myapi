# encoding:utf-8

import requests
import base64
from PIL import Image

url = "https://ocr.ap-southeast-1.myhuaweicloud.com/v2/bcc56b8e08d54369a28d55ad8e49c883/ocr/smart-document-recognizer"


urlImage = "https://image.ap-southeast-1.myhuaweicloud.com/v2/bcc56b8e08d54369a28d55ad8e49c883/image/tagging"







def detectCharacters (rutaImagen, token):
     #image = Image.open(ruta_imagen)
     #imagepath = r'https://i.ibb.co/HLt9rxBX/image.png'

    headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
    try:
        with open(rutaImagen, "rb") as bin_data:
            image_data = bin_data.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")  # Use Base64 encoding of images.
        
        data= {
            "data": image_base64,
            "single_orientation_mode":False
            }  # Set either the URL or the image.

        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()
        if(response.status_code == 200 or response.status_code == 201):
            print(response.text)
            result = ocr_to_paragraph(response.json())
            return result
        else:
            return "Without results"
    except:
        return "Error detecting Text"






def detectHuaweiObjects (rutaImagen, token):
     #image = Image.open(ruta_imagen)
     #imagepath = r'https://i.ibb.co/HLt9rxBX/image.png'

    headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
    try:
        with open(rutaImagen, "rb") as bin_data:
            image_data = bin_data.read()
        image_base64 = base64.b64encode(image_data).decode("utf-8")  # Use Base64 encoding of images.
        
        data= {
            "image": image_base64,
          "language":"en"
            }  # Set either the URL or the image.

        response = requests.post(urlImage, headers=headers, json=data, verify=False)
        response.raise_for_status()
        if(response.status_code == 200 or response.status_code == 201):
            print(response.text)
            result = summarize_tags_with_limit(response.text)
            return result
        else:
            return "Without results"
    except:
        return "Error detecting Image Scene"






def ocr_to_paragraph(ocr_json: dict) -> str:
    """
    Convierte la salida JSON del OCR en un párrafo de texto.
    Maneja casos donde no haya resultados o listas vacías.
    """
    if not isinstance(ocr_json, dict):
        return "Entrada inválida: no es un diccionario."

    results = ocr_json.get("result", [])
    if not results:
        return "No se encontraron resultados de OCR."

    ocr_result = results[0].get("ocr_result", {})
    words_blocks = ocr_result.get("words_block_list", [])

    if not words_blocks:
        return "El OCR no devolvió texto."

    # Extraer los textos en orden
    text_lines = [block.get("words", "").strip() for block in words_blocks if block.get("words")]
    
    if not text_lines:
        return "El OCR no detectó palabras reconocibles."

    # Unir en un párrafo (respetando espacios)
    paragraph = " ".join(text_lines)
    return paragraph





import json
def summarize_tags_with_limit(json_str, char_limit=350):
    """
    Summarizes tags and instances into text with a maximum character limit.
    Stops adding lines when the limit is reached and truncates the last line if necessary.
    """
    summary_lines = []
    total_chars = 0

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON → {e}"

    tags = data.get("result", {}).get("tags", [])

    for idx, tag in enumerate(tags):
        tag_type = tag.get("type", "Unknown")
        tag_name = tag.get("tag", "Unknown")
        tag_confidence = round(float(tag.get("confidence", 0)), 2)
        instances = tag.get("instances", [])

        if instances and isinstance(instances, list):
            for inst in instances:
                bbox = inst.get("bounding_box", {})
                location = (
                    bbox.get("top_left_x"),
                    bbox.get("top_left_y"),
                    bbox.get("width"),
                    bbox.get("height")
                ) if bbox else None

                inst_conf = inst.get("confidence", tag_confidence)
                try:
                    inst_conf = round(float(inst_conf), 2)
                except:
                    inst_conf = tag_confidence

                line = f"Type: {tag_type}, TAG: {tag_name}, Confidence: {inst_conf}, Location: {location}"
                if total_chars + len(line) + 1 > char_limit:
                    # Truncamos la línea si pasa el límite
                    remaining = char_limit - total_chars
                    summary_lines.append(line[:remaining])
                    return "\n".join(summary_lines)
                summary_lines.append(line)
                total_chars += len(line) + 1  # +1 para el salto de línea
        else:
            line = f"Type: {tag_type}, TAG: {tag_name}, Confidence: {tag_confidence}, Location: None"
            if total_chars + len(line) + 1 > char_limit:
                remaining = char_limit - total_chars
                summary_lines.append(line[:remaining])
                return "\n".join(summary_lines)
            summary_lines.append(line)
            total_chars += len(line) + 1

    return "\n".join(summary_lines)

