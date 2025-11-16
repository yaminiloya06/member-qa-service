# 🧠 Member Question-Answering API  
A lightweight FastAPI service that answers natural-language questions about members using data from a public API.

The service exposes a single endpoint `/ask` that accepts a question and returns an answer inferred *strictly* from the member messages provided by the external API.

---

## 🚀 Features
- Fetches member messages from a public API  
- Uses **Llama-3.1-70B** via Fireworks API for natural-language reasoning  
- Strict hallucination control (LLM is forced to answer *only* from provided messages)  
- Fully asynchronous FastAPI backend  
- Simple, clean JSON output:

```json
{ "answer": "..." }
```

---

## 📌 API Endpoints

### **Health Check**
```
GET /health
```
Response:
```json
{ "status": "ok" }
```

### **Ask a Question**
```
POST /ask
```
Body:
```json
{
  "question": "Who need orchestra seats?"
}
```

Response:
```json
{
  "answer": "Layla Kawaguchi"
}
```

---

## ⚙️ Tech Stack
- **FastAPI** – API framework  
- **HTTPX** – For async calls to external API  
- **Fireworks.ai** – LLM provider (Llama-3.1-70B)  
- **Pydantic** – Request/response validation  

---

## 📥 Setup Instructions (Local Development)

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/member-qa-service.git
cd member-qa-service
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Export Fireworks API key
```bash
export FIREWORKS_API_KEY=fw_3ZGrSKBwjetRRwxvq7xhzXFm 
```

### 5. Run the API
```bash
uvicorn main:app --reload port 8000
```


# 🔍 Bonus 1: Design Notes (Alternative Approaches Considered)

### **1. Direct keyword-based search (rejected)**
- Simple string matching  
- No reasoning ability  

### **2. Vector embeddings + semantic search**
- Embedding each message  
- Retrieve top-K relevant  
- Then use LLM  

### **3. Fine-tuned QA model**
- Not practical due to limited dataset  

### **4. Chosen Method: In-context LLM QA**
- Pass all messages to LLM  
- Constrain with strong system prompt  
- Best balance of accuracy + simplicity  

---

# 🔍 Bonus 2: Data Insights (Anomalies & Observations)

### **1. Repeated messages**
Some messages appear duplicated or similar.

### **2. Inconsistent date formats**
Different formats mixed together.

### **3. Ambiguous references**
Words like:
- “partner”
- “friend”
- “sister”
lack context.

### **4. Typos / informal writing**
Informal messages, emojis, inconsistent punctuation.

---

## 📁 Project Structure
```
.
├── main.py
├── requirements.txt
├── README.md
└── venv/
```

---

## 👍 Conclusion
This project provides a clean, reliable, LLM-powered question-answering system built with FastAPI. It is simple, efficient, and easily deployable.
