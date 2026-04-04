🚀 DeepTrace – AI-Powered Deepfake & Plagiarism Detection System
📌 Overview
DeepTrace is a cybersecurity-based web application that detects:

🎥 Deepfake videos

🖼️ Fake images

📝 AI-generated text

📄 Plagiarized content (with web detection)

It uses machine learning models and real-time web search to analyze and verify content authenticity.

🔥 Features
✅ Deepfake Detection
Image deepfake detection

Video deepfake detection (frame-based analysis)

Text authenticity detection

✅ Plagiarism Detection
Local similarity checking (TF-IDF)

Real-time web plagiarism detection (SerpAPI)

AI vs Human content estimation

✅ Authentication System
User Signup

User Login

Secure password hashing

🧠 Tech Stack
Backend
FastAPI

Python

Uvicorn

AI / ML
PyTorch (image/video models)

Scikit-learn (text & plagiarism)

OpenCV (video frame processing)

APIs
SerpAPI (Google Search for plagiarism)

📁 Project Structure
app/
│
├── routes/
│     ├── image.py
│     ├── video.py
│     ├── text.py
│     ├── plagiarism.py
│     └── auth.py
│
├── services/
│     ├── image_service.py
│     ├── video_service.py
│     ├── text_service.py
│     ├── plagiarism_service.py
│     └── web_search_service.py
│
├── models/
│     └── user_model.py
│
├── model_loader.py
├── main.py
│
data/   (stores uploaded files)
⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/your-username/DeepTrace.git
cd DeepTrace
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
Or manually:

pip install fastapi uvicorn torch opencv-python scikit-learn passlib[bcrypt] google-search-results
4️⃣ Add SerpAPI Key
In:

app/services/web_search_service.py
API_KEY = "YOUR_API_KEY"
5️⃣ Run Server
uvicorn app.main:app --reload
6️⃣ Open API Docs
http://127.0.0.1:8000/docs
🧪 API Endpoints
🔹 Authentication
POST /signup

POST /login

🔹 Deepfake Detection
POST /image

POST /video

POST /text

🔹 Plagiarism Detection
POST /plagiarism

📊 Example Output
{
  "plagiarism": "YES",
  "source": "https://example.com",
  "similarity": 68.2,
  "ai_generated_percentage": 72.5,
  "human_written_percentage": 27.5
}
🎯 Demo Workflow
Upload image/video/text/file

System processes input

Model analyzes authenticity

Result displayed with probability

⚠️ Limitations (Prototype)
Supports .txt files only (for plagiarism)

Basic AI detection heuristic

Limited API calls (SerpAPI free tier)

🚀 Future Improvements
PDF & DOCX support

Advanced transformer-based AI detection

Database integration (PostgreSQL)

JWT authentication

Highlight plagiarized sentences

Real-time streaming detection

🧠 Use Case
Fake news detection

Social media verification

Academic plagiarism checking

Cybersecurity applications

👨‍💻 Author
Ashish Pathak

⭐ Final Note
This project is designed as a hackathon-ready prototype with scalable architecture that can be extended into a production-level system.

