# 🛡️ CyberChain Hackathon: LLM Firewall Gateway

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow)

## 📌 Challenge 1: LLM Firewall (Malicious Prompt Detection)
A real-time semantic filtering layer designed to protect Black-Box LLMs from malicious prompts (direct/indirect injections, jailbreaks) and prevent sensitive data extraction. 

## 🚀 Key Features & Real-World Deployment
We designed this firewall not just to pass a test, but to be a highly viable, real-world deployment proxy:
* **Dual-Layer Guard:** Intercepts both the `user_input` (Input Guard) and the `llm_response` (Output Guard).
* **High-Speed Semantic Filtering:** Uses an optimized Deep Learning model (`ProtectAI/deberta-v3-base-prompt-injection-v2`) to evaluate inputs and outputs accurately without the latency of calling an external LLM API.
* **Dynamic Threat Intelligence (IP Blocklist):** Pre-loaded with +27,000 known malicious IPs.
* **Auto-Ban Mechanism:** If a user attempts an injection, their IP is immediately added to the blocklist in real-time to prevent brute-force attacks.
* **Comprehensive Audit Logs:** Every pass, block, and ban is audited in a `firewall.log` file.

## 🏗️ Architecture & Tech Stack
* **Framework:** `FastAPI` (Python) - Chosen for its high performance and asynchronous capabilities, acting as the reverse proxy.
* **AI Engine:** HuggingFace `transformers` pipeline.
* **Security Model:** `ProtectAI/deberta-v3-base-prompt-injection-v2`.

## 🛠️ Installation & Setup (Verified Instructions)

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/samuuu16/hackathonSala.git](https://github.com/samuuu16/hackathonSala.git)
   cd hackathonSala
   
## 📊 Evaluation & Metrics
Based on our testing against the provided dataset:
* **Total analyzed:** 16
* **Accuracy:** 75.00%
* **False Positive Rate (FPR):** 33.33%

## 🤖 Uso de IA y Reglas de Participación
In accordance with the hackathon rules, this team declares the following:
* **Generative AI:** **We have used the Gemini AI to help us work on this challenge.** We used it as an assistant for brainstorming, structuring the FastApi proxy, and debugging the code.
* **Original Code:** The codebase was developed entirely during the hackathon.
* **Pre-trained Models:** We utilize the open-source library `FastAPI` and the pre-trained model `ProtectAI/deberta-v3-base-prompt-injection-v2` via HuggingFace `transformers`.

## 👥 Team Members
* Samuel Gil López
* Carlos Álvarez Martinez
* Marcos Fernandez
* Victor Martinez Vega
