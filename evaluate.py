import requests
import pandas as pd
import time

# --- 1. CONFIGURACIÓN ---
DATASET_FILE = "dataset_hackathon.csv"
API_URL = "http://127.0.0.1:8001/chat"

print(f"Cargando dataset: {DATASET_FILE}...")

try:
    df = pd.read_csv(DATASET_FILE)
except FileNotFoundError:
    print("❌ ERROR: No se encuentra el archivo CSV. Comprueba el nombre.")
    exit()

# Intentamos adivinar las columnas si no se llaman 'prompt' y 'label'
col_texto = 'text' if 'text' in df.columns else 'prompt' if 'prompt' in df.columns else df.columns[0]
col_label = 'label' if 'label' in df.columns else 'etiqueta' if 'etiqueta' in df.columns else df.columns[1]

print(f"Usando columna de texto: '{col_texto}' y etiqueta: '{col_label}'")
print("Iniciando bombardeo a la API... (Esto puede tardar un par de minutos)")

true_positives = 0
false_positives = 0
true_negatives = 0
false_negatives = 0
total_prompts = 0

for index, row in df.iterrows():
    total_prompts += 1
    texto = str(row[col_texto])
    # Asumimos que la etiqueta de ataque contiene "INJECTION" o "JAILBREAK" o es "1"
    etiqueta_real = str(row[col_label]).upper() 
    es_ataque_real = "INJECTION" in etiqueta_real or "JAILBREAK" in etiqueta_real or etiqueta_real == "1"

    # Falsificamos la IP para que vuestra propia blocklist no os banee el test
    headers = {'X-Forwarded-For': f'10.0.0.{total_prompts % 250}'} 
    payload = {"user_input": texto}
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        
        if response.status_code == 200: # El firewall hizo PASS
            if not es_ataque_real:
                true_negatives += 1
            else:
                false_negatives += 1
                
        elif response.status_code == 403: # El firewall hizo BLOCK
             if es_ataque_real:
                 true_positives += 1
             else:
                 false_positives += 1
                 
    except Exception as e:
        print(f"❌ Error conectando a la API: {e}. ¿Está el servidor encendido?")
        break

    # Imprimir progreso cada 50 prompts para no agobiarnos
    if total_prompts % 50 == 0:
        print(f"Analizados: {total_prompts}/{len(df)}...")

# --- 3. RESULTADOS ---
print("\n" + "="*40)
print("🚀 RESULTADOS PARA EL README 🚀")
print("="*40)
accuracy = (true_positives + true_negatives) / total_prompts if total_prompts > 0 else 0
fpr = false_positives / (false_positives + true_negatives) if (false_positives + true_negatives) > 0 else 0

print(f"Total analizados: {total_prompts}")
print(f"Accuracy (Precisión): {accuracy:.2%}")
print(f"False Positive Rate (FPR): {fpr:.2%}")
print("="*40)