import logging
import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from ai_guard import analyze_prompt # Importamos el modelo de Koke

# --- CONFIGURACIÓN DE LOGS ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("firewall.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="LLM Firewall Proxy con IP Blocklist")

# --- SISTEMA DE IP BLOCKLIST ---
BLOCKLIST_FILE = "blocklist.txt"
blocked_ips = set() # Usamos un 'set' para búsquedas ultrarrápidas

# Cargar la blocklist al iniciar
if os.path.exists(BLOCKLIST_FILE):
    with open(BLOCKLIST_FILE, "r") as f:
        for line in f:
            ip = line.strip()
            if ip:
                blocked_ips.add(ip)
    logger.info(f"Blocklist cargada con {len(blocked_ips)} IPs maliciosas.")

def ban_ip(ip: str):
    """Añade la IP a la memoria y la guarda en el .txt con salto de línea seguro"""
    if ip not in blocked_ips:
        blocked_ips.add(ip)
        
        # Leemos rápido si el archivo necesita un salto de línea previo
        needs_newline = False
        if os.path.exists(BLOCKLIST_FILE):
            with open(BLOCKLIST_FILE, "rb") as f:
                try:
                    f.seek(-1, os.SEEK_END)
                    if f.read(1) != b'\n':
                        needs_newline = True
                except OSError:
                    pass # Archivo vacío
                    
        # Añadimos la IP
        with open(BLOCKLIST_FILE, "a") as f:
            if needs_newline:
                f.write("\n")
            f.write(f"{ip}\n")
            
        logger.info(f"[NUEVO BANNED] La IP {ip} ha sido añadida a la blocklist permanentemente.")

# --- MODELOS DE DATOS ---
class PromptRequest(BaseModel):
    user_input: str

def call_black_box_llm(text: str) -> str:
    return f"Respuesta del LLM para: {text}"

# --- ENDPOINT PRINCIPAL ---
# OJO: Hemos añadido 'request: Request' para poder leer la IP del cliente
@app.post("/chat")
async def chat_endpoint(payload: PromptRequest, request: Request):
    client_ip = request.client.host
    
    # 0. FILTRO DE RED (IP Blocklist)
    if client_ip in blocked_ips:
        logger.warning(f"[BLOCK - IP] Intento de conexión rechazado. IP en blocklist: {client_ip}")
        raise HTTPException(status_code=403, detail="Access denied: Your IP is banned.")

    logger.info(f"[NUEVA PETICIÓN] IP: {client_ip} | Input: '{payload.user_input}'")
    
    # 1. FILTRO SEMÁNTICO (INPUT GUARD con IA)
    is_safe_input = analyze_prompt(payload.user_input)
    if not is_safe_input:
        logger.warning(f"[BLOCK - INPUT] Prompt malicioso detectado. Baneando a {client_ip}...")
        ban_ip(client_ip) # ¡Cazado! A la blocklist que se va
        raise HTTPException(status_code=403, detail="Malicious prompt detected. Blocked and IP Banned.")
    
    logger.info("[PASS - INPUT] Prompt seguro. Enviando al LLM...")
    
    # 2. CAJA NEGRA (LLM)
    llm_response = call_black_box_llm(payload.user_input)
    
    # 3. FILTRO SEMÁNTICO (OUTPUT GUARD con IA)
    is_safe_output = analyze_prompt(llm_response)
    if not is_safe_output:
         logger.warning(f"[BLOCK - OUTPUT] Fuga de datos del LLM detectada.")
         raise HTTPException(status_code=500, detail="Data leak detected in LLM output. Blocked.")

    logger.info("[PASS - OUTPUT] Respuesta segura. Enviando al usuario.")
    return {"status": "success", "response": llm_response}