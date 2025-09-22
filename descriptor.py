import cohere

co = cohere.Client("6CGv06YoOolcxkKYVjc9edOVBHdnpe3dDmPfeWk5")

def describir_entorno(message_json: str, context: str) -> str:
    chat_history = [
        {
            "role": "system",
            "message": f"""You are an assistant that describes the surroundings for visually impaired people. I will give you a list of objects detected in an image along with their positions, expressed as bounding box coordinates [x1, y1, x2, y2], where (0,0) is the top-left corner.  
Please generate a clear, natural, and useful description that explains:  
- What objects are present and where they are located relative to the user  
- Which objects seem closest or largest  
- Any relevant spatial relationships between them  
- Keep it concise and easy for a visually impaired person to understand  
- Do not mention coordinates; instead, help the user understand the scene naturally  
- Consider the confidence in the detection when describing, but do not tell the user the confidence  
- Also, the visually impaired user tells you the following: {context}"""
        }
    ]
    '''
    response = co.chat(
        model="command-a-03-2025",
        chat_history=chat_history,
        message=message_json+"\nContexto: "+context,
       
    )
    '''
    response = co.chat(
            model="command-a-03-2025",
            chat_history=chat_history,
            message=message_json
        
        )
    return response.text




def leer_OCR(textGetted: str, context: str) -> str:
    chat_history = [
        {
            "role": "system",
            "message": f"""You are an assistant for visually impaired people. You receive the following result from an OCR reading: {textGetted}. Respond to what the user requests regarding the extracted text."""

        }
    ]

    response = co.chat(
            model="command-a-03-2025",
            chat_history=chat_history,
            message=context
        
        )
    return response.text





def only_chat(msg: str) -> str:
    chat_history = [
        {
            "role": "system",
         "message": "You are an assistant for a visually impaired person, and your name is ANA. The user will ask you a question. If you consider that fulfilling their request requires OCR (reading text from the environment), respond with 1. If you detect that they want to use computer vision to detect objects, respond with 0. If you think they just want to chat, answer their question without mentioning things they are not interested in knowing."
  }
    ]

    response = co.chat(
        model="command-a-03-2025",
        chat_history=chat_history,
        message=msg,
        
    )

    return response.text

