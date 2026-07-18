import os
from openai import OpenAI

# Intentar cargar variables desde el archivo .env si python-dotenv está disponible
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Fallback manual por si python-dotenv no está instalado
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip().strip("'\"")

# Obtener la API key desde las variables de entorno.
# Buscaremos nombres comunes como GEMINI_API_KEY, OPENAI_API_KEY o API_KEY
API_KEY = os.getenv("DEEPSEEK-API-KEY")
BASE_URL = 'https://api.deepseek.com' #'https://dashscope-intl.aliyuncs.com/compatible-mode/v1' #"https://generativelanguage.googleapis.com/v1beta/openai/"
MODEL = 'deepseek-v4-flash' #'qwen3.7-plus' #"gemini-3.5-flash"

def test_api():
    if not API_KEY:
        print("[ADVERTENCIA] No se pudo encontrar ninguna API key en las variables de entorno ni en el archivo .env.")
        print("Asegúrate de definir GEMINI_API_KEY, OPENAI_API_KEY o API_KEY en tu archivo .env.")
        return

    # Inicialización del cliente con la URL base y la clave configuradas
    client = OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL
    )

    print(f"Conectando a: {BASE_URL}")
    print(f"Modelo a utilizar: {MODEL}")
    print("Enviando prompt de prueba...")

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un asistente de inteligencia artificial altamente capacitado y especializado en redactar "
                        "explicaciones técnicas claras y completas para audiencias profesionales. Tu objetivo es proporcionar "
                        "respuestas detalladas, estructuradas y con un tono informativo y formal. Asegúrate de justificar tus "
                        "puntos con argumentos lógicos, evitar la redundancia y mantener un alto estándar de calidad redactora "
                        "en cada una de tus intervenciones."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        "Por favor, redacta un texto explicativo de aproximadamente 80 a 120 palabras sobre los principales "
                        "desafíos que presenta el cambio climático para la agricultura de precisión moderna. Describe al menos "
                        "dos de estos desafíos de manera detallada (por ejemplo, la predictibilidad del clima o la escasez de recursos hídricos) "
                        "y concluye con una breve reflexión sobre cómo la tecnología puede mitigar estos impactos."
                    )
                }
            ],
            temperature=0.7,
            reasoning_effort="low",
            extra_body={"thinking": {"type": "disabled"}}
        )
        
        # Obtener y mostrar la respuesta
        answer = response.choices[0].message.content
        print("\n=== RESPUESTA DE LA API ===")
        print(answer)
        print("===========================")
        
    except Exception as e:
        print(f"\n[ERROR] Ocurrió un fallo al comunicarse con la API: {e}")

if __name__ == "__main__":
    test_api()
