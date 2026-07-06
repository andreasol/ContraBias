import json
import os
import openai
from tqdm import tqdm
import time

# ==============================================================================
# CONFIGURACIÓN PARA NVIDIA NIM API
# ==============================================================================
# Reemplaza 'TU_API_KEY_AQUI' con la API Key oficial de Nvidia
NVIDIA_API_KEY = "TU_API_KEY" 

# Arreglo con los 5 mejores modelos Texto a Texto de tu lista
MODELS = [
    "meta/llama-3.3-70b-instruct",                   
    "mistralai/mistral-large-3-675b-instruct-2512",  
    "qwen/qwen3.5-397b-a17b",                        
    "nvidia/llama-3.3-nemotron-super-49b-v1",        
    "mistralai/mixtral-8x7b-instruct-v0.1"           
]

def load_plugin_rules():
    """Carga las reglas contrafactuales desde el archivo del plugin."""
    plugin_path = os.path.join(os.path.dirname(__file__), '..', 'plugin', 'system_prompt.txt')
    with open(plugin_path, 'r', encoding='utf-8') as f:
        return f.read()

def evaluate_translation(client, model_name, sentence_data, use_plugin=False):
    """
    Envía la frase a la API de Nvidia usando un modelo específico del arreglo.
    """
    sentence = sentence_data["english_sentence"]
    user_prompt = f'Traduce la siguiente oración al español. Evita explicaciones largas, responde con la traducción directa: "{sentence}"'
    
    messages = []
    
    if use_plugin:
        messages.append({"role": "system", "content": load_plugin_rules()})
    else:
        messages.append({"role": "system", "content": "Eres un traductor experto de inglés a español."})
        
    messages.append({"role": "user", "content": user_prompt})
    
    try:
        response = client.chat.completions.create(
            model=model_name, 
            messages=messages,
            temperature=0.1, 
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error API] Ocurrió un problema con el modelo {model_name}. Detalles: {e}"

def run_experiment():
    print("Iniciando Evaluación Científica Multi-Modelo (Benchmarking)")
    
    if NVIDIA_API_KEY == "TU_API_KEY_AQUI":
        print("¡ALTO! Tienes que abrir este archivo (run_multi_model_nvidia.py) y pegar tu API KEY de Nvidia en la línea 10.")
        return

    client = openai.OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=NVIDIA_API_KEY
    )

    dataset_path = os.path.join(os.path.dirname(__file__), 'dataset', 'winomt_sample.json')
    with open(dataset_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for model_name in MODELS:
        print("\n" + "=" * 80)
        print(f">>> INICIANDO BATERÍA DE PRUEBAS CON EL MODELO: {model_name}")
        print("=" * 80)
        
        for item in data:
            print(f"\nFRASE ORIGINAL : {item['english_sentence']}")
            print(f"GÉNERO ESPERADO: {item['expected_gender_in_context'].upper()}")
            print("-" * 60)
            
            # 1. Baseline
            print(f">> PROCESANDO BASELINE (Sin Plugin)...")
            res_baseline = evaluate_translation(client, model_name, item, use_plugin=False)
            print(f"[Baseline]: {res_baseline}\n")
            time.sleep(2) # Pausa para Rate Limit
                
            # 2. Plugin
            print(f">> PROCESANDO CON PLUGIN...")
            res_plugin = evaluate_translation(client, model_name, item, use_plugin=True)
            print(f"[Plugin]  : {res_plugin}\n")
            time.sleep(2) # Pausa para Rate Limit

    print("\n" + "=" * 80)
    print("Benchmarking Multi-Modelo terminado exitosamente.")
    
if __name__ == "__main__":
    run_experiment()
