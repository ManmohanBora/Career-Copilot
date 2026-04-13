# 🚀 Career Copilot – AI-Based Career Guidance System

---

## 📌 Overview

**Career Copilot** is an intelligent web-based application that analyzes user resumes and provides personalized career insights, job matching scores, and skill gap analysis.

The system uses **Rule-Based NLP techniques** to extract skills from unstructured resume data and compare them with structured job requirements stored in a database.

---

## 🎯 Problem Statement

Many students and job seekers struggle to:

* Identify the right career path
* Understand required skills for specific roles
* Analyze gaps in their current skillset

👉 This project solves these problems by providing **automated, data-driven career guidance**.

---

## 💡 Solution

Career Copilot:

* Extracts skills from resumes
* Matches them with job roles
* Calculates compatibility score
* Identifies missing skills
* Provides actionable insights

---

## ✨ Features

| Feature               | Description                        |
| --------------------- | ---------------------------------- |
| 📄 Resume Parsing     | Extracts skills from resume text   |
| 🧠 NLP Engine         | Uses Regex + Keyword Matching      |
| 🎯 Job Matching       | Matches user skills with job roles |
| 📊 Score Calculation  | Provides match percentage          |
| ⚠️ Skill Gap Analysis | Identifies missing skills          |
| 📈 Visualization      | Displays insights using charts     |
| 💻 UI Interface       | Built with Streamlit               |

---

## 🏗️ System Architecture

| Layer                  | Description                       |
| ---------------------- | --------------------------------- |
| 🎨 Frontend            | Streamlit UI for user interaction |
| ⚙️ Processing Layer    | NLP + Matching Logic              |
| 🗄️ Database Layer     | SQLite for job & skill data       |
| 📊 Visualization Layer | Charts & insights display         |

---

## 🔄 Workflow

```
User Input (Resume)
        ↓
Text Preprocessing
        ↓
Skill Extraction (NLP + Regex)
        ↓
Fetch Job Data (SQLite)
        ↓
Skill Matching & Scoring
        ↓
Skill Gap Analysis
        ↓
Visualization & Results
```

---

## 🧠 Technologies Used

| Technology | Purpose            |
| ---------- | ------------------ |
| Python     | Core programming   |
| Streamlit  | Web application UI |
| SQLite     | Database           |
| Regex      | Skill extraction   |
| Pandas     | Data processing    |
| Plotly     | Visualization      |

---

## 🤖 AI Used

This project uses **Rule-Based NLP (Symbolic AI)**:

| Component        | Technique                |
| ---------------- | ------------------------ |
| Skill Extraction | Regex + Keyword Matching |
| Matching Logic   | Set Intersection         |
| Gap Analysis     | Set Difference           |

> ⚠️ Note: No Machine Learning models are used currently.
> The system is designed for future ML integration.

---

## ⚙️ Configuration

The application uses `config.toml` for customization:

| Setting | Purpose                  |
| ------- | ------------------------ |
| Theme   | UI colors and appearance |
| Server  | Deployment behavior      |

---

## 📂 Project Structure

```
career-copilot/
│
├── app.py
├── setup_db.py
├── career_copilot.db
├── config.toml
├── requirements.txt
└── README.md
```

---

## ▶️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ManmohanBora/Career-Copilot.git
cd career-copilot
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application

```bash
streamlit run app.py
```

---

## 📊 Output

* ✅ Match Score (%)
* 📉 Missing Skills
* 📈 Visual Insights
* 🎯 Career Recommendations

---

## 🚀 Future Scope

| Area           | Enhancement                       |
| -------------- | --------------------------------- |
| 🤖 AI          | Integrate Machine Learning models |
| 🌐 Integration | Connect with job APIs             |
| 📊 Analytics   | Advanced dashboards               |
| 📄 Resume      | Auto resume feedback              |
| ☁️ Deployment  | Cloud hosting                     |
| 🔐 Security    | User login & tracking             |

---

## 💪 Strengths

* Simple and efficient design
* Explainable AI approach
* Fast processing
* Scalable architecture

---

## ⚠️ Limitations

* No deep learning models
* Limited dataset
* Rule-based accuracy constraints

---

## 🏆 Hackathon Highlights

* Real-world problem solving
* AI-based implementation
* Clean modular architecture
* User-friendly design

---

## 📸 Screenshots

*Add your project screenshots here*

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Manmohan Bora**
🔗 GitHub: https://github.com/ManmohanBora
💼 LinkedIn: www.linkedin.com/in/manmohan-bora

---

## ⭐ Support

If you found this project useful:

👉 Give it a ⭐ on GitHub
👉 Share it with others

---

## 🔥 Final Note

> “This project transforms unstructured resume data into meaningful career insights using lightweight and explainable AI.”
