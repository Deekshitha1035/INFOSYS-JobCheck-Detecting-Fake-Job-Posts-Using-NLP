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
![Signup](https://1drv.ms/i/c/a0e59f011cf5dcf9/IQBWVhsF4BMARbFYxDnKFKBZAUXEQgcIVqrZnHTV35U9s9M?e=ldraEb)
![Loginin]((https://1drv.ms/i/c/a0e59f011cf5dcf9/IQBswi3Z5GlsQbOks6z8TeTFAYEHFh3OJVm6CBm-X3pdkwI?e=rBYnyU)))


### 🔍 Job Prediction Result
![Prediction](](https://1drv.ms/i/c/a0e59f011cf5dcf9/IQBONdhsFY_QQ6dieQCvXYEiAWzE0JFwDSC2TK38SePRBQQ?e=9UN9wX),<img width="1366" height="768" alt="2026-01-09 (5)" src="https://github.com/user-attachments/assets/8bd8cc3c-654c-40f9-bffa-74601f3f19c5" />
)

### 📊 Admin Dashboard
![Admin Dashboard](images/admin-dashboard.png)


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
