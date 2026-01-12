INFOSYS-JobCheck Detecting Fake Job Posts Using NLP
📌 Project Overview

In today’s digital era, fake job postings have become a serious threat to job seekers, especially students and fresh graduates. These fraudulent postings often lead to financial loss, identity theft, and emotional distress.

INFOSYS-JobCheck is an intelligent system that uses Natural Language Processing (NLP) and Machine Learning techniques to analyze job descriptions and determine whether a job post is real or fake. The system aims to help users make safer career decisions and improve trust in online recruitment platforms.

🎯 Objectives

Detect fake job postings using NLP and ML models

Protect job seekers from fraud and scams

Improve awareness and trust in online job portals

Provide explainable results for predictions

🧠 Key Features

🔍 Text Analysis using NLP

🤖 Machine Learning–based classification

📊 Admin Dashboard for analytics

🔐 Authentication & Authorization (JWT)

📈 Visualization of fake vs real job trends

⚡ FastAPI backend

🌐 User-friendly web interface

🛠️ Technologies Used
🔹 Backend

Python

FastAPI

Machine Learning (Scikit-learn)

NLP (TF-IDF / CountVectorizer)

JWT Authentication

🔹 Frontend

HTML

CSS

JavaScript

🔹 Database

PostgreSQL / SQLite (as applicable)

🔹 Tools & Libraries

Pandas

NumPy

Scikit-learn

Chart.js

🏗️ System Architecture

User submits a job description

Text is preprocessed using NLP techniques

ML model predicts Real / Fake

Result is displayed on the UI

Admin dashboard tracks analytics

🚀 How to Run the Project
1️⃣ Clone the Repository
git clone https://github.com/Deekshitha1035/INFOSYS-JobCheck-Detecting-Fake-Job-Posts-Using-NLP.git
cd INFOSYS-JobCheck-Detecting-Fake-Job-Posts-Using-NLP

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the Backend
uvicorn main:app --reload

5️⃣ Open Frontend

Open index.html in your browser or run via Live Server.

📊 Model Details

Text Vectorization: TF-IDF

Algorithms Used:

Logistic Regression

Naive Bayes (optional)

Output:

Real Job

Fake Job
## 📸 Project Screenshots

### 🏠 
![Signup](<img width="1366" height="768" alt="2026-01-09 (1)" src="https://github.com/user-attachments/assets/62982637-2e21-4962-92a7-d10da5188bdc" />
)
![Loginin](<img width="1366" height="768" alt="2026-01-09 (2)" src="https://github.com/user-attachments/assets/15b0759b-c1b8-4951-a1b3-9eaf4f5cc03d" />
)


### 🔍 Job Prediction Result
![Prediction](<img width="1366" height="768" alt="2026-01-09 (4)" src="https://github.com/user-attachments/assets/54bc9a5a-cf9b-4c5c-906b-476c9629709e" />
,<img width="1366" height="768" alt="2026-01-09 (5)" src="https://github.com/user-attachments/assets/8bd8cc3c-654c-40f9-bffa-74601f3f19c5" />
)

### 📊 Admin Dashboard
![Admin Dashboard](<img width="1366" height="768" alt="2026-01-09 (6)" src="https://github.com/user-attachments/assets/273da0bd-0184-4a6d-acc9-be83d75e4d4a" /> ,<img width="1366" height="768" alt="2026-01-09 (7)" src="https://github.com/user-attachments/assets/5c44d4f2-5101-4c87-b687-8a12e2a7ae0a" /> ,<img width="1366" height="768" alt="2026-01-09 (8)" src="https://github.com/user-attachments/assets/fcb6ceec-b4a3-4506-98f8-5fa2ec18a8e8" />


)


🔒 Security Features

Password hashing

JWT-based authentication

Role-based access (Admin / User)

Secure API endpoints

📌 Use Cases

Students & fresh graduates

Job seekers

Educational institutions

Recruitment platforms

📄 License

This project is licensed under the MIT License.
See the LICENSE file for details.

👩‍💻 Author

Jilika Deekshitha Sri
GitHub: Deekshitha1035

⭐ Acknowledgements

Infosys Springboard Virtual Internship

Open-source NLP and ML libraries

Online datasets for fake job detection
