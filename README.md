# ⚡ CCLambda – Serverless Function Execution Platform

**CCLambda** is a lightweight, custom-built serverless platform inspired by **AWS Lambda**. It allows users to upload, deploy, execute, and monitor small code functions in **Python** and **JavaScript**, using simulated runtimes like **Docker** and **gVisor**.

---

## 🚀 Features

- 🔐 **JWT-based user authentication**
- 📁 **Upload code files** (Python/JS) for deployment
- ✏️ **Paste and execute code snippets directly**
- ⚡ **Simulated function execution** using Docker/gVisor
- 📊 **Real-time dashboard** for monitoring executions
- 🌐 **Frontend** built with Streamlit
- ⚙️ **Backend** built with FastAPI

---

## 🛠️ Tech Stack

| Component | Technology                      |
|-----------|----------------------------------|
| **Frontend** | Streamlit                    |
| **Backend**  | FastAPI                      |
| **Runtimes** | Docker, gVisor (simulated)   |
| **Auth**     | OAuth2 with JWT Tokens       |
| **Charts**   | Plotly, Pandas               |

---
## 📦 Setup Instructions (macOS/Linux)

### 1. Clone the Repository
git clone https://github.com/SpurtiBhat/CCLambda----Serverless-Function-Execution-Platform.git
cd CCLambda----Serverless-Function-Execution-Platform

### 2. Set Up a Virtual Environment
python3 -m venv venv
source venv/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt
⚠️ Make sure Python 3.8+ is installed
Check your version with:
python3 --version
### 4. Run the Backend (FastAPI)
uvicorn main:app --reload
API available at: http://localhost:8000

API docs: http://localhost:8000/docs

### 5. 🌐 Run the Frontend (Streamlit)
streamlit run frontend.py
UI available at: http://localhost:8501

Use the sidebar to log in, deploy, and run functions.

🧪 Example Python Function
def handler(event):
    a = event.get("a", 1)
    b = event.get("b", 1)
    return {"result": a * b}
📊 Monitor Dashboard

### 6. Navigate to the Monitor tab to view:

✅ Total deployed functions

🌍 Most used languages

📈 Bar graph of execution times per function

