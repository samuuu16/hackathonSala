import requests
import pandas as pd
import time

# --- CONFIGURACIÓN ---
# ¡CAMBIAR POR EL NOMBRE REAL DEL CSV DEL RETO!
DATASET_FILE = "dataset.csv" 
API_URL = "http://127.0.0.1:8001/chat"

print("Iniciando evaluación del modelo...")

# Leer el CSV (Asumiendo que tiene columnas 'prompt' y 'label')
# Ajustad los nombres de las columnas si en vuestro CSV se llaman distinto
df = pd.read_csv(DATASET_FILE)

true_positives = 0
false_positives = 0
true_negatives = 0
false_negatives = 0
total_prompts = 0

for index, row in df.iterrows():
    total_prompts += 1
    texto = str(row['prompt']) # Cambiar 'prompt' si la columna se llama diferente
    etiqueta_real = str(row['label']).upper() # 'SAFE' o 'INJECTION'
    
    # Fingimos IPs distintas para que la blocklist no pare el test
    headers = {'X-Forwarded-For': f'192.168.1.{total_prompts}'} 
    payload = {"user_input": texto}
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            if etiqueta_real == "SAFE":
                true_negatives += 1
            else:
                false_negatives += 1
                
        elif response.status_code == 403:
             if etiqueta_real == "INJECTION":
                 true_positives += 1
             else:
                 false_positives += 1
                 
    except Exception as e:
        print(f"Error en la petición: {e}")
        break

# Imprimir resultados
print("\n--- RESULTADOS PARA EL README ---")
accuracy = (true_positives + true_negatives) / total_prompts if total_prompts > 0 else 0
fpr = false_positives / (false_positives + true_negatives) if (false_positives + true_negatives) > 0 else 0

print(f"Total analizados: {total_prompts}")
print(f"Accuracy: {accuracy:.2%}")
print(f"False Positive Rate (FPR): {fpr:.2%}")