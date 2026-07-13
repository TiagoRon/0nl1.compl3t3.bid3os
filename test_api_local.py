import os
from google import genai
from dotenv import load_dotenv

def test_api():
    # Load .env if it exists locally
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: No se encontró la variable GOOGLE_API_KEY. Asegúrate de tenerla en un archivo .env o configurada en tu sistema.")
        return
        
    print(f"Se encontró una API Key que empieza con: {api_key[:5]}...")
    
    try:
        print("Probando conexión con los servidores de Gemini (Google)...")
        client = genai.Client(api_key=api_key)
        
        # Test basic generation
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents='Responde con la palabra "EXITO" si recibes este mensaje.'
        )
        
        print(f"CONEXIÓN EXITOSA! Gemini respondió: {response.text.strip()}")
        
    except Exception as e:
        print(f"ERROR AL CONECTAR CON LA API:\n{e}")

if __name__ == "__main__":
    test_api()
