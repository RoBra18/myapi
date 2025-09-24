from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from descriptor import describir_entorno, only_chat, leer_OCR
#from getObjects import detectar_objetos_str
from getOCRText import detectCharacters, detectHuaweiObjects
from SMTPGmailSenderService import SMTPGmailSenderService
from HuaweiTokenManager import is_token_valid, getNewToken
import shutil
import os
import uuid
app = FastAPI()


(token, expires_at)= getNewToken()
#(token, expires_at)= (0,0)

sender = SMTPGmailSenderService()


@app.get("/")
def root():
    return {"message": "API is running 🚀"}

@app.post("/wantDescription")
async def return_description( description: str = ""):
    try:
       

        # Procesar imagen
        #objetos_str = detectar_objetos_str(filepath)
        #descr = get_Short_description(filepath)
        geratedDescription = only_chat(description)
        return {"descripcion":geratedDescription}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")




@app.post("/detect_objects")
async def detect_objects(file: UploadFile = File(...), description: str = Form("")):
    global token, expires_at
    try:
        print(description)
        # Guardar archivo temporal
        filename = f"temp_{uuid.uuid4().hex}.jpg"
        filepath = os.path.join("temp", filename)
        os.makedirs("temp", exist_ok=True)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Procesar imagen
       # objetos_str = detectar_objetos_str(filepath)
        if is_token_valid(expires_at) == False:
            (token, expires_at)= getNewToken()
        if(token != 0):

            objetos_str = detectHuaweiObjects(filepath, token)
            #descr = get_Short_description(filepath)
            geratedDescription = describir_entorno(objetos_str, description)

            os.remove(filepath)

            return {"descripcion":geratedDescription}
        else:
            os.remove(filepath)
            return {"descripcion":"I couldn't do it"}


    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")



@app.post("/read")
async def detect_ocr(file: UploadFile = File(...), description: str = Form("")):
    global token, expires_at
    try:
        print(description)
        # Guardar archivo temporal
        filename = f"temp_{uuid.uuid4().hex}.jpg"
        filepath = os.path.join("temp", filename)
        os.makedirs("temp", exist_ok=True)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if is_token_valid(expires_at) == False:
            (token, expires_at)= getNewToken()

        if token != 0:

            resultOCR = detectCharacters(filepath, token)
            resultLLM = leer_OCR( resultOCR, description)

            # Eliminar imagen temporal
            os.remove(filepath)

            return {"descripcion":resultLLM}
        else:
            os.remove(filepath)
            return {"descripcion":"There was an error"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")



@app.post("/sendEmail")
async def sendEmail(email = "", description: str = ""):
    try:
        sender.send(email, "EyeAssist", description)
        return {"descripcion": "The Email was sended succesfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


