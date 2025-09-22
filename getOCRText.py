# encoding:utf-8

import requests
import base64
from PIL import Image

url = "https://ocr.ap-southeast-1.myhuaweicloud.com/v2/bcc56b8e08d54369a28d55ad8e49c883/ocr/smart-document-recognizer"









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
