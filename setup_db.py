"""
AI Career Copilot - Database Setup & Seeding
Run this ONCE to create and populate career_copilot.db
"""

import sqlite3
import json
import os
from pathlib import Path

DB_PATH = Path(__file__).parent / "career_copilot.db"

def create_tables(conn):
    c = conn.cursor()
    c.executescript("""
        DROP TABLE IF EXISTS jobs;
        DROP TABLE IF EXISTS skills;
        DROP TABLE IF EXISTS career_paths;
        DROP TABLE IF EXISTS courses;
        DROP TABLE IF EXISTS interview_questions;

        CREATE TABLE jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            required_skills TEXT NOT NULL,
            avg_salary_lpa REAL NOT NULL,
            demand_score INTEGER NOT NULL,
            description TEXT
        );

        CREATE TABLE skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            demand_score INTEGER NOT NULL,
            difficulty INTEGER NOT NULL,
            description TEXT
        );

        CREATE TABLE career_paths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_role TEXT NOT NULL,
            to_role TEXT NOT NULL,
            skills_to_add TEXT NOT NULL,
            months_min INTEGER,
            months_max INTEGER,
            difficulty TEXT
        );

        CREATE TABLE courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT NOT NULL,
            course_name TEXT NOT NULL,
            platform TEXT NOT NULL,
            duration TEXT NOT NULL,
            level TEXT NOT NULL,
            url TEXT
        );

        CREATE TABLE interview_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            question TEXT NOT NULL,
            category TEXT NOT NULL,
            difficulty TEXT NOT NULL
        );
    """)
    conn.commit()

def seed_jobs(conn):
    jobs = [
        ("Data Scientist", "Data Science",
         json.dumps(["python","machine learning","statistics","pandas","numpy","scikit-learn","sql","data visualization","matplotlib","seaborn","feature engineering","jupyter"]),
         14.0, 10, "Analyze complex datasets to extract actionable insights and build predictive models."),

        ("Machine Learning Engineer", "AI/ML",
         json.dumps(["python","machine learning","deep learning","tensorflow","pytorch","docker","aws","mlflow","git","ci/cd","algorithms","scikit-learn"]),
         20.0, 10, "Design, train, deploy and monitor ML models in production environments."),

        ("Data Analyst", "Data Analytics",
         json.dumps(["sql","python","excel","tableau","power bi","statistics","data visualization","pandas","reporting","business intelligence"]),
         8.0, 9, "Transform raw data into business insights through analysis and visualization."),

        ("Data Engineer", "Data Engineering",
         json.dumps(["python","sql","apache spark","kafka","airflow","aws","docker","etl","scala","data pipeline","postgresql"]),
         17.0, 9, "Build and maintain scalable data pipelines and infrastructure."),

        ("NLP Engineer", "AI/ML",
         json.dumps(["python","nlp","bert","transformers","huggingface","tensorflow","pytorch","text classification","spacy","nltk","llm"]),
         18.0, 8, "Build NLP models for text understanding, generation, and classification."),

        ("Computer Vision Engineer", "AI/ML",
         json.dumps(["python","computer vision","opencv","tensorflow","pytorch","deep learning","image processing","yolo","cnn"]),
         18.0, 7, "Develop visual recognition and image processing systems using deep learning."),

        ("AI Researcher", "Research",
         json.dumps(["python","deep learning","machine learning","mathematics","statistics","pytorch","tensorflow","research","linear algebra","calculus"]),
         22.0, 6, "Advance the state of AI through novel research and publications."),

        ("MLOps Engineer", "AI/ML",
         json.dumps(["python","docker","kubernetes","mlflow","airflow","aws","ci/cd","git","model deployment","monitoring","terraform"]),
         19.0, 8, "Bridge gap between ML research and production deployment at scale."),

        ("Prompt Engineer", "AI/ML",
         json.dumps(["llm","prompt engineering","python","nlp","langchain","openai api","gpt","chatgpt","rag"]),
         13.0, 8, "Design and optimize prompts for large language models to achieve specific outcomes."),

        ("AI Product Manager", "Product",
         json.dumps(["product management","machine learning","agile","scrum","roadmap","stakeholder management","data analysis","strategy","presentation"]),
         25.0, 6, "Lead AI product strategy, bridging technical teams with business objectives."),

        ("Software Engineer", "Engineering",
         json.dumps(["python","java","javascript","git","data structures","algorithms","oop","testing","agile","rest api","postgresql"]),
         11.0, 10, "Design and build scalable software systems and applications."),

        ("Backend Developer", "Engineering",
         json.dumps(["python","java","node.js","rest api","sql","docker","git","microservices","redis","postgresql","postgresql"]),
         13.0, 9, "Build server-side logic, APIs, and database integrations."),

        ("Frontend Developer", "Engineering",
         json.dumps(["javascript","typescript","react","vue","css","html","git","rest api","responsive design","ux"]),
         11.0, 9, "Build user interfaces and interactive web experiences."),

        ("Full Stack Developer", "Engineering",
         json.dumps(["javascript","python","react","node.js","sql","docker","git","rest api","html","css","postgresql"]),
         15.0, 8, "Handle both frontend and backend development across the entire stack."),

        ("DevOps Engineer", "Infrastructure",
         json.dumps(["docker","kubernetes","aws","ci/cd","terraform","linux","git","monitoring","bash","jenkins"]),
         16.0, 8, "Automate and optimize software delivery and infrastructure management."),

        ("Cloud Engineer", "Infrastructure",
         json.dumps(["aws","gcp","azure","terraform","kubernetes","docker","networking","security","linux","python"]),
         17.0, 8, "Design, deploy, and manage cloud infrastructure and services."),

        ("Business Analyst", "Business",
         json.dumps(["sql","excel","power bi","tableau","business requirements","stakeholder management","agile","data analysis","reporting","presentation"]),
         9.0, 8, "Bridge business needs and technical solutions through data-driven analysis."),

        ("BI Developer", "Data Analytics",
         json.dumps(["sql","power bi","tableau","data warehouse","etl","reporting","dax","python","excel","data modeling"]),
         12.0, 7, "Build business intelligence dashboards and data warehouse solutions."),

        ("Database Administrator", "Data Engineering",
         json.dumps(["sql","postgresql","mysql","mongodb","database design","performance tuning","backup","security","oracle"]),
         11.0, 6, "Manage, secure, and optimize database systems and performance."),

        ("Cybersecurity Analyst", "Security",
         json.dumps(["networking","security","python","penetration testing","firewall","siem","incident response","linux","compliance","risk assessment"]),
         14.0, 7, "Protect systems and data from cyber threats and vulnerabilities."),

        ("Product Manager", "Product",
         json.dumps(["product management","agile","scrum","roadmap","user research","data analysis","stakeholder management","strategy","presentation","jira"]),
         20.0, 7, "Define product vision, strategy, and roadmap to deliver customer value."),

        ("Quantitative Analyst", "Finance",
         json.dumps(["python","r","statistics","mathematics","machine learning","time series","sql","financial modeling","risk management","scipy"]),
         22.0, 5, "Apply quantitative methods to solve complex financial and risk problems."),

        ("Site Reliability Engineer", "Infrastructure",
         json.dumps(["python","kubernetes","docker","aws","monitoring","linux","ci/cd","bash","performance","reliability"]),
         18.0, 6, "Ensure system reliability, scalability and performance in production."),

        ("Mobile Developer", "Engineering",
         json.dumps(["java","kotlin","swift","react native","flutter","mobile development","rest api","git","ux"]),
         13.0, 7, "Build native and cross-platform mobile applications for iOS and Android."),

        ("Blockchain Developer", "Engineering",
         json.dumps(["solidity","python","javascript","ethereum","smart contracts","web3","cryptography","blockchain"]),
         20.0, 4, "Develop decentralized applications and smart contracts on blockchain platforms."),

        ("Data Architect", "Data Engineering",
         json.dumps(["sql","data modeling","data warehouse","cloud architecture","etl","apache spark","aws","snowflake","python","bigquery"]),
         24.0, 5, "Design enterprise-scale data systems, lakes, and warehouse architectures."),

        ("AI Ethics Researcher", "Research",
         json.dumps(["machine learning","research","statistics","bias detection","fairness","python","communication","policy","presentation"]),
         16.0, 4, "Study and mitigate ethical implications of AI systems in society."),

        ("Robotics Engineer", "Engineering",
         json.dumps(["python","c++","ros","control systems","computer vision","machine learning","mathematics","embedded systems"]),
         17.0, 4, "Design and develop robotic systems combining hardware and AI software."),

        ("IoT Engineer", "Engineering",
         json.dumps(["python","c++","embedded systems","mqtt","networking","aws","docker","sensors","linux","edge computing"]),
         14.0, 5, "Build connected device ecosystems and edge computing solutions."),

        ("AR/VR Developer", "Engineering",
         json.dumps(["unity","c#","3d modeling","computer vision","opengl","python","javascript","ux","spatial computing"]),
         15.0, 4, "Create immersive augmented and virtual reality experiences."),
    ]
    conn.executemany(
        "INSERT INTO jobs (title, category, required_skills, avg_salary_lpa, demand_score, description) VALUES (?,?,?,?,?,?)",
        jobs
    )
    conn.commit()

def seed_skills(conn):
    skills = [
        # Programming Languages
        ("python", "Programming", 10, 2, "Most popular language for data science and AI"),
        ("sql", "Programming", 9, 3, "Essential for querying and managing relational databases"),
        ("r", "Programming", 7, 4, "Statistical computing language used in academia and research"),
        ("java", "Programming", 8, 4, "Enterprise-grade object-oriented programming language"),
        ("javascript", "Programming", 8, 3, "Dominant language for web development, frontend and backend"),
        ("typescript", "Programming", 7, 4, "Typed superset of JavaScript for large applications"),
        ("scala", "Programming", 7, 6, "JVM language popular for big data processing with Spark"),
        ("c++", "Programming", 7, 7, "High-performance language for systems and robotics"),
        ("c#", "Programming", 6, 5, "Microsoft's OOP language, widely used in enterprise and gaming"),
        ("matlab", "Programming", 5, 5, "Numerical computing language used in engineering and academia"),
        ("julia", "Programming", 5, 5, "High-performance language for numerical and scientific computing"),
        ("bash", "Programming", 7, 4, "Unix shell scripting for automation and system administration"),

        # Machine Learning & AI
        ("machine learning", "AI/ML", 10, 5, "Core discipline of training algorithms to learn from data"),
        ("deep learning", "AI/ML", 9, 7, "ML using multi-layered neural networks for complex pattern recognition"),
        ("nlp", "AI/ML", 9, 6, "Processing and understanding human language using AI"),
        ("computer vision", "AI/ML", 8, 7, "Teaching machines to interpret and understand visual data"),
        ("scikit-learn", "AI/ML", 9, 3, "Python's premier ML library with simple, consistent API"),
        ("tensorflow", "AI/ML", 8, 6, "Google's open-source ML framework for production AI"),
        ("pytorch", "AI/ML", 9, 5, "Facebook's flexible ML framework preferred in research"),
        ("xgboost", "AI/ML", 8, 4, "Powerful gradient boosting algorithm, dominant in tabular data"),
        ("lightgbm", "AI/ML", 7, 4, "Fast, efficient gradient boosting framework by Microsoft"),
        ("bert", "AI/ML", 8, 7, "Bidirectional transformer model revolutionizing NLP tasks"),
        ("transformers", "AI/ML", 8, 7, "Architecture behind GPT, BERT and modern large language models"),
        ("llm", "AI/ML", 9, 6, "Large Language Models - the foundation of modern AI assistants"),
        ("langchain", "AI/ML", 8, 5, "Framework for building LLM-powered applications and agents"),
        ("huggingface", "AI/ML", 8, 4, "Platform and library for state-of-the-art NLP models"),
        ("openai api", "AI/ML", 8, 3, "OpenAI's API for accessing GPT-4, DALL-E, and Whisper"),
        ("prompt engineering", "AI/ML", 8, 3, "Craft effective instructions to elicit optimal AI responses"),
        ("rag", "AI/ML", 7, 5, "Retrieval-Augmented Generation for grounded LLM responses"),
        ("reinforcement learning", "AI/ML", 6, 9, "Training agents via reward signals to learn optimal behavior"),
        ("feature engineering", "AI/ML", 9, 5, "Creating meaningful features from raw data to improve ML models"),

        # Data Processing
        ("pandas", "Data", 9, 2, "Python's core data manipulation and analysis library"),
        ("numpy", "Data", 9, 2, "Fundamental package for numerical computing in Python"),
        ("apache spark", "Data", 8, 7, "Distributed data processing engine for big data workloads"),
        ("kafka", "Data", 7, 7, "Distributed event streaming platform for real-time data pipelines"),
        ("airflow", "Data", 8, 6, "Platform to programmatically author, schedule, and monitor workflows"),
        ("etl", "Data", 8, 5, "Extract, Transform, Load process for data integration pipelines"),
        ("data pipeline", "Data", 8, 5, "Automated series of data processing steps from source to destination"),
        ("dbt", "Data", 7, 4, "Tool for transforming data in the warehouse using SQL"),
        ("scipy", "Data", 7, 4, "Scientific computing library built on NumPy for Python"),
        ("spacy", "Data", 6, 4, "Industrial-strength NLP library for Python"),
        ("nltk", "Data", 6, 3, "Python toolkit for natural language processing tasks"),

        # Visualization
        ("matplotlib", "Visualization", 8, 2, "Python's foundational plotting library"),
        ("seaborn", "Visualization", 8, 2, "Statistical data visualization built on matplotlib"),
        ("plotly", "Visualization", 8, 2, "Interactive visualization library for Python and web"),
        ("tableau", "Visualization", 8, 3, "Industry-leading BI and data visualization platform"),
        ("power bi", "Visualization", 8, 3, "Microsoft's business analytics and visualization solution"),
        ("data visualization", "Visualization", 9, 3, "Graphical representation of data to communicate insights"),
        ("streamlit", "Visualization", 7, 2, "Fast way to build and deploy Python-powered data apps"),
        ("dash", "Visualization", 6, 3, "Python framework for building analytical web applications"),
        ("business intelligence", "Visualization", 8, 4, "Strategies and technologies for enterprise data analysis"),
        ("dax", "Visualization", 6, 5, "Data Analysis Expressions language used in Power BI"),

        # Cloud & Infrastructure
        ("aws", "Cloud", 9, 5, "Amazon's comprehensive cloud platform with 200+ services"),
        ("gcp", "Cloud", 8, 5, "Google Cloud Platform for data, AI, and infrastructure"),
        ("azure", "Cloud", 8, 5, "Microsoft Azure cloud computing platform and services"),
        ("docker", "Cloud", 9, 4, "Platform for containerizing applications for portability"),
        ("kubernetes", "Cloud", 8, 7, "Container orchestration system for automating deployment"),
        ("terraform", "Cloud", 7, 6, "Infrastructure as Code tool for cloud resource management"),
        ("linux", "Cloud", 8, 4, "Open-source OS essential for server and cloud environments"),
        ("ci/cd", "Cloud", 8, 5, "Continuous Integration/Delivery for automated software delivery"),
        ("mlflow", "Cloud", 7, 4, "Open-source platform for managing the ML lifecycle"),
        ("monitoring", "Cloud", 7, 4, "Tracking system health, performance, and ML model behavior"),
        ("edge computing", "Cloud", 6, 7, "Processing data near the source rather than centralized cloud"),

        # Databases
        ("postgresql", "Database", 8, 4, "Advanced open-source relational database system"),
        ("mysql", "Database", 8, 3, "World's most popular open-source relational database"),
        ("mongodb", "Database", 7, 4, "Leading NoSQL document database for flexible data models"),
        ("redis", "Database", 7, 5, "In-memory data store for caching and real-time applications"),
        ("elasticsearch", "Database", 6, 6, "Distributed search and analytics engine"),
        ("snowflake", "Database", 7, 5, "Cloud-native data warehouse for analytics at scale"),
        ("bigquery", "Database", 7, 4, "Google's serverless, scalable data warehouse"),
        ("oracle", "Database", 6, 5, "Enterprise relational database management system"),
        ("database design", "Database", 8, 5, "Structuring data models for efficient storage and retrieval"),
        ("data warehouse", "Database", 8, 5, "Centralized repository for structured, filtered historical data"),
        ("data modeling", "Database", 7, 5, "Process of creating data models for information systems"),

        # Statistics & Mathematics
        ("statistics", "Math & Stats", 9, 5, "Mathematical science for data collection, analysis, and inference"),
        ("probability", "Math & Stats", 8, 5, "Mathematical study of random phenomena and uncertainty"),
        ("linear algebra", "Math & Stats", 8, 7, "Mathematics of vectors and matrices, core to ML algorithms"),
        ("calculus", "Math & Stats", 6, 7, "Mathematical study of continuous change, basis for optimization"),
        ("a/b testing", "Math & Stats", 8, 4, "Controlled experiments to compare two versions of a product"),
        ("hypothesis testing", "Math & Stats", 8, 5, "Statistical method to evaluate assumptions about data"),
        ("time series", "Math & Stats", 8, 6, "Analysis of data points collected over time to find patterns"),
        ("bayesian methods", "Math & Stats", 6, 8, "Statistical framework combining prior knowledge with new data"),
        ("risk management", "Math & Stats", 7, 6, "Process of identifying and mitigating financial and operational risks"),

        # Tools & Soft Skills
        ("git", "Tools", 9, 2, "Version control system for tracking code changes and collaboration"),
        ("jupyter", "Tools", 9, 1, "Interactive notebook environment for data science and research"),
        ("agile", "Tools", 8, 2, "Iterative software development methodology for delivering value"),
        ("scrum", "Tools", 7, 3, "Agile framework for managing complex product development"),
        ("jira", "Tools", 7, 2, "Project tracking tool widely used in software development"),
        ("communication", "Soft Skills", 9, 2, "Effectively conveying ideas to technical and non-technical audiences"),
        ("leadership", "Soft Skills", 7, 4, "Guiding and inspiring teams toward a shared goal"),
        ("presentation", "Soft Skills", 8, 3, "Structuring and delivering compelling data stories"),
        ("problem solving", "Soft Skills", 10, 3, "Breaking down complex challenges into structured, solvable steps"),
        ("stakeholder management", "Soft Skills", 7, 4, "Engaging and aligning diverse stakeholders toward shared goals"),
        ("research", "Soft Skills", 7, 4, "Systematic investigation to establish new knowledge and insights"),
        ("strategy", "Soft Skills", 8, 5, "Long-term planning to achieve organizational or product goals"),
    ]
    conn.executemany(
        "INSERT INTO skills (name, category, demand_score, difficulty, description) VALUES (?,?,?,?,?)",
        skills
    )
    conn.commit()

def seed_career_paths(conn):
    paths = [
        ("Data Analyst", "Data Scientist",
         json.dumps(["machine learning", "deep learning", "scikit-learn", "feature engineering", "statistics"]),
         6, 12, "Medium"),
        ("Data Scientist", "Machine Learning Engineer",
         json.dumps(["docker", "kubernetes", "mlflow", "ci/cd", "aws", "model deployment"]),
         6, 12, "Medium"),
        ("Software Engineer", "Data Engineer",
         json.dumps(["sql", "apache spark", "airflow", "kafka", "etl", "data pipeline"]),
         9, 18, "Medium"),
        ("Data Engineer", "Data Scientist",
         json.dumps(["machine learning", "statistics", "scikit-learn", "feature engineering", "deep learning"]),
         12, 18, "Hard"),
        ("Machine Learning Engineer", "AI Researcher",
         json.dumps(["research", "mathematics", "linear algebra", "calculus", "bayesian methods"]),
         12, 24, "Hard"),
        ("Business Analyst", "Data Analyst",
         json.dumps(["python", "sql", "pandas", "power bi", "statistics", "data visualization"]),
         3, 9, "Easy"),
        ("Frontend Developer", "Full Stack Developer",
         json.dumps(["python", "node.js", "sql", "rest api", "docker", "postgresql"]),
         6, 9, "Easy"),
        ("Backend Developer", "DevOps Engineer",
         json.dumps(["docker", "kubernetes", "terraform", "ci/cd", "aws", "monitoring", "linux"]),
         9, 15, "Medium"),
        ("Data Scientist", "AI Product Manager",
         json.dumps(["product management", "stakeholder management", "agile", "strategy", "roadmap"]),
         12, 24, "Hard"),
        ("MLOps Engineer", "Cloud Architect",
         json.dumps(["cloud architecture", "networking", "security", "aws", "azure", "gcp", "terraform"]),
         12, 18, "Hard"),
        ("Data Analyst", "BI Developer",
         json.dumps(["sql", "power bi", "tableau", "dax", "data warehouse", "data modeling"]),
         3, 6, "Easy"),
        ("Software Engineer", "Machine Learning Engineer",
         json.dumps(["python", "machine learning", "deep learning", "scikit-learn", "tensorflow", "pytorch"]),
         9, 18, "Medium"),
        ("Data Scientist", "Data Engineer",
         json.dumps(["apache spark", "airflow", "kafka", "etl", "data pipeline", "scala"]),
         6, 12, "Medium"),
        ("MLOps Engineer", "Data Scientist",
         json.dumps(["machine learning", "statistics", "feature engineering", "deep learning", "research"]),
         9, 18, "Hard"),
        ("Data Analyst", "Product Manager",
         json.dumps(["product management", "agile", "user research", "roadmap", "stakeholder management"]),
         12, 24, "Hard"),
    ]
    conn.executemany(
        "INSERT INTO career_paths (from_role, to_role, skills_to_add, months_min, months_max, difficulty) VALUES (?,?,?,?,?,?)",
        paths
    )
    conn.commit()

def seed_courses(conn):
    courses = [
        ("python", "Python for Everybody Specialization", "Coursera", "3 months", "Beginner", "https://www.coursera.org/specializations/python"),
        ("python", "Complete Python Bootcamp — From Zero to Hero", "Udemy", "22 hours", "Beginner", "https://www.udemy.com/course/complete-python-bootcamp/"),
        ("python", "Python Data Science Handbook", "O'Reilly/GitHub", "Self-paced", "Intermediate", "https://jakevdp.github.io/PythonDataScienceHandbook/"),
        ("machine learning", "Machine Learning Specialization (Andrew Ng)", "Coursera", "3 months", "Intermediate", "https://www.coursera.org/specializations/machine-learning-introduction"),
        ("machine learning", "Hands-On ML with Scikit-Learn, Keras & TF", "O'Reilly Book", "Self-paced", "Advanced", "https://www.oreilly.com/library/view/hands-on-machine-learning/"),
        ("machine learning", "Machine Learning A-Z", "Udemy", "44 hours", "Beginner", "https://www.udemy.com/course/machinelearning/"),
        ("deep learning", "Deep Learning Specialization (Andrew Ng)", "Coursera", "3 months", "Advanced", "https://www.coursera.org/specializations/deep-learning"),
        ("deep learning", "Practical Deep Learning for Coders", "fast.ai", "7 weeks", "Intermediate", "https://course.fast.ai/"),
        ("deep learning", "Deep Learning with PyTorch: Zero to GANs", "Jovian", "6 weeks", "Intermediate", "https://jovian.com/learn/deep-learning-with-pytorch-zero-to-gans"),
        ("sql", "SQL for Data Analysis", "Udacity", "4 weeks", "Beginner", "https://www.udacity.com/course/sql-for-data-analysis--ud198"),
        ("sql", "The Complete SQL Bootcamp", "Udemy", "9 hours", "Beginner", "https://www.udemy.com/course/the-complete-sql-bootcamp/"),
        ("sql", "Advanced SQL for Data Scientists", "LinkedIn Learning", "5 hours", "Advanced", "https://www.linkedin.com/learning/advanced-sql-for-data-scientists"),
        ("tensorflow", "TensorFlow Developer Certificate Program", "Coursera", "4 months", "Intermediate", "https://www.coursera.org/professional-certificates/tensorflow-in-practice"),
        ("pytorch", "PyTorch for Deep Learning Bootcamp", "Udemy", "25 hours", "Intermediate", "https://www.udemy.com/course/pytorch-for-deep-learning/"),
        ("pandas", "Pandas for Data Analysis", "DataCamp", "4 hours", "Beginner", "https://www.datacamp.com/courses/data-manipulation-with-pandas"),
        ("statistics", "Statistics with Python Specialization", "Coursera", "3 months", "Intermediate", "https://www.coursera.org/specializations/statistics-with-python"),
        ("statistics", "Think Stats: Probability & Statistics for Programmers", "Green Tea Press", "Self-paced", "Intermediate", "https://greenteapress.com/wp/think-stats-2e/"),
        ("tableau", "Tableau 2024 A-Z: Hands-On Tableau Training", "Udemy", "12 hours", "Beginner", "https://www.udemy.com/course/tableau10/"),
        ("power bi", "Microsoft Power BI Desktop for Business Intelligence", "Udemy", "17 hours", "Beginner", "https://www.udemy.com/course/microsoft-power-bi-up-running-with-power-bi-desktop/"),
        ("aws", "AWS Certified Solutions Architect – Associate", "AWS Training", "3 months", "Intermediate", "https://aws.amazon.com/certification/certified-solutions-architect-associate/"),
        ("aws", "Ultimate AWS Certified Developer Associate", "Udemy", "32 hours", "Intermediate", "https://www.udemy.com/course/aws-certified-developer-associate-dva-c01/"),
        ("docker", "Docker Mastery: with Kubernetes + Swarm", "Udemy", "20 hours", "Intermediate", "https://www.udemy.com/course/docker-mastery/"),
        ("kubernetes", "Kubernetes for the Absolute Beginners", "Udemy", "6 hours", "Beginner", "https://www.udemy.com/course/learn-kubernetes/"),
        ("nlp", "Natural Language Processing Specialization", "Coursera (deeplearning.ai)", "4 months", "Advanced", "https://www.coursera.org/specializations/natural-language-processing"),
        ("nlp", "Hugging Face NLP Course", "Hugging Face", "Self-paced", "Intermediate", "https://huggingface.co/learn/nlp-course"),
        ("llm", "LLM Bootcamp (LangChain, OpenAI)", "Full Stack Deep Learning", "8 weeks", "Intermediate", "https://fullstackdeeplearning.com/llm-bootcamp/"),
        ("langchain", "LangChain & Vector Databases in Production", "Activeloop", "Self-paced", "Intermediate", "https://learn.activeloop.ai/courses/langchain"),
        ("git", "Git & GitHub Crash Course", "freeCodeCamp", "5 hours", "Beginner", "https://www.freecodecamp.org/news/git-and-github-crash-course/"),
        ("apache spark", "Apache Spark and Python (PySpark) for BigData", "Udemy", "15 hours", "Intermediate", "https://www.udemy.com/course/spark-and-python-for-big-data-with-pyspark/"),
        ("airflow", "The Complete Hands-On Course to Master Apache Airflow", "Udemy", "8 hours", "Intermediate", "https://www.udemy.com/course/the-complete-hands-on-course-to-master-apache-airflow/"),
        ("feature engineering", "Feature Engineering for Machine Learning", "Udemy", "8 hours", "Intermediate", "https://www.udemy.com/course/feature-engineering-for-machine-learning/"),
        ("data visualization", "Data Visualization with Python (IBM)", "Coursera", "3 weeks", "Beginner", "https://www.coursera.org/learn/python-for-data-visualization"),
        ("scikit-learn", "Scikit-Learn Machine Learning in Python", "DataCamp", "4 hours", "Intermediate", "https://www.datacamp.com/courses/supervised-learning-with-scikit-learn"),
        ("time series", "Time Series Analysis with Python", "Udemy", "12 hours", "Intermediate", "https://www.udemy.com/course/python-for-time-series-data-analysis/"),
        ("mlflow", "MLflow in Action: ML Lifecycle Management", "Udemy", "6 hours", "Intermediate", "https://www.udemy.com/course/mlflow-for-machine-learning/"),
        ("agile", "Agile Fundamentals: Scrum & Kanban", "Udemy", "6 hours", "Beginner", "https://www.udemy.com/course/agile-fundamentals-scrum-kanban/"),
        ("prompt engineering", "ChatGPT Prompt Engineering for Developers", "DeepLearning.AI", "4 hours", "Beginner", "https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/"),
        ("rag", "Building Systems with the ChatGPT API", "DeepLearning.AI", "4 hours", "Intermediate", "https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt/"),
    ]
    conn.executemany(
        "INSERT INTO courses (skill_name, course_name, platform, duration, level, url) VALUES (?,?,?,?,?,?)",
        courses
    )
    conn.commit()

def seed_interview_questions(conn):
    questions = [
        # Data Scientist
        ("Data Scientist", "Explain the bias-variance tradeoff and how it affects model performance.", "Technical", "Hard"),
        ("Data Scientist", "What is cross-validation? Why do we use it?", "Technical", "Medium"),
        ("Data Scientist", "How would you handle class imbalance in a classification problem?", "Technical", "Medium"),
        ("Data Scientist", "Explain the difference between L1 and L2 regularization.", "Technical", "Hard"),
        ("Data Scientist", "What is the difference between supervised and unsupervised learning?", "Technical", "Easy"),
        ("Data Scientist", "Explain PCA. When and why would you use it?", "Technical", "Medium"),
        ("Data Scientist", "Walk me through a data science project you're proud of.", "Behavioral", "Medium"),
        ("Data Scientist", "How do you explain complex model results to non-technical stakeholders?", "Behavioral", "Medium"),
        ("Data Scientist", "How do you decide which model to use for a given problem?", "Technical", "Medium"),
        ("Data Scientist", "What is the curse of dimensionality?", "Technical", "Hard"),

        # Machine Learning Engineer
        ("Machine Learning Engineer", "How do you deploy a machine learning model to production?", "Technical", "Hard"),
        ("Machine Learning Engineer", "What is model drift? How do you detect and handle it?", "Technical", "Hard"),
        ("Machine Learning Engineer", "Explain how you would design an ML pipeline for real-time inference.", "Technical", "Hard"),
        ("Machine Learning Engineer", "What's the difference between batch and online learning?", "Technical", "Medium"),
        ("Machine Learning Engineer", "How do you ensure reproducibility in ML experiments?", "Technical", "Medium"),
        ("Machine Learning Engineer", "Explain Docker and why it's important for ML deployment.", "Technical", "Medium"),
        ("Machine Learning Engineer", "How do you monitor model performance in production?", "Technical", "Hard"),
        ("Machine Learning Engineer", "How would you reduce model inference latency?", "Technical", "Hard"),

        # Data Analyst
        ("Data Analyst", "How would you identify outliers in a dataset?", "Technical", "Easy"),
        ("Data Analyst", "Walk me through how you would investigate a sudden drop in sales.", "Technical", "Medium"),
        ("Data Analyst", "What's the difference between a LEFT JOIN and INNER JOIN?", "Technical", "Easy"),
        ("Data Analyst", "How do you ensure data quality in your analysis?", "Technical", "Medium"),
        ("Data Analyst", "Explain the difference between a KPI and a metric.", "Conceptual", "Easy"),
        ("Data Analyst", "How would you design a dashboard for a CEO?", "Behavioral", "Medium"),
        ("Data Analyst", "What is cohort analysis and when would you use it?", "Technical", "Medium"),
        ("Data Analyst", "Write a SQL query to find the top 5 customers by revenue.", "Technical", "Easy"),

        # Data Engineer
        ("Data Engineer", "What is ETL? Explain the differences between ETL and ELT.", "Technical", "Medium"),
        ("Data Engineer", "How would you handle late-arriving data in a streaming pipeline?", "Technical", "Hard"),
        ("Data Engineer", "Explain the difference between Apache Spark and Hadoop MapReduce.", "Technical", "Hard"),
        ("Data Engineer", "How do you ensure data quality in a data pipeline?", "Technical", "Medium"),
        ("Data Engineer", "What is data partitioning and why does it matter for performance?", "Technical", "Hard"),
        ("Data Engineer", "Explain the star schema vs snowflake schema in data warehousing.", "Technical", "Medium"),
        ("Data Engineer", "How would you design a data pipeline for 1 billion records per day?", "Technical", "Hard"),

        # NLP Engineer
        ("NLP Engineer", "Explain the transformer architecture — how does self-attention work?", "Technical", "Hard"),
        ("NLP Engineer", "What is the difference between BERT and GPT architectures?", "Technical", "Hard"),
        ("NLP Engineer", "How would you approach a text classification problem end-to-end?", "Technical", "Medium"),
        ("NLP Engineer", "What techniques can you use to handle out-of-vocabulary words?", "Technical", "Medium"),
        ("NLP Engineer", "What is RAG and what problem does it solve?", "Technical", "Medium"),
        ("NLP Engineer", "Explain word embeddings vs contextual embeddings.", "Technical", "Medium"),

        # Software Engineer / Backend Developer
        ("Software Engineer", "What is the difference between REST and GraphQL?", "Technical", "Medium"),
        ("Software Engineer", "Explain SOLID principles with examples.", "Technical", "Medium"),
        ("Software Engineer", "How would you design a URL shortener like bit.ly?", "System Design", "Hard"),
        ("Software Engineer", "What is the difference between SQL and NoSQL databases?", "Technical", "Easy"),
        ("Software Engineer", "Explain what happens when you type a URL in the browser.", "Technical", "Medium"),
        ("Software Engineer", "What is the CAP theorem?", "Technical", "Hard"),

        # DevOps / Cloud Engineer
        ("DevOps Engineer", "What is the difference between Docker and a virtual machine?", "Technical", "Easy"),
        ("DevOps Engineer", "Explain Kubernetes pods, services, and deployments.", "Technical", "Hard"),
        ("DevOps Engineer", "What is CI/CD and how do you implement it?", "Technical", "Medium"),
        ("DevOps Engineer", "How do you handle secrets management in Kubernetes?", "Technical", "Hard"),
        ("DevOps Engineer", "What is infrastructure as code and why does it matter?", "Technical", "Medium"),

        # General / Behavioral
        ("All Roles", "Tell me about yourself and why you're interested in this role.", "Behavioral", "Easy"),
        ("All Roles", "Describe a time you failed. What did you learn from it?", "Behavioral", "Medium"),
        ("All Roles", "How do you stay updated with the latest developments in your field?", "Behavioral", "Easy"),
        ("All Roles", "Describe a situation where you had to work with a difficult teammate.", "Behavioral", "Medium"),
        ("All Roles", "Where do you see yourself in 5 years?", "Behavioral", "Easy"),
        ("All Roles", "What's your biggest technical achievement so far?", "Behavioral", "Medium"),
    ]
    conn.executemany(
        "INSERT INTO interview_questions (role, question, category, difficulty) VALUES (?,?,?,?)",
        questions
    )
    conn.commit()

def main():
    os.makedirs(DB_PATH.parent, exist_ok=True)
    print(f"📦 Creating database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    print("✅ Connected to database")
    create_tables(conn)
    print("✅ Tables created")
    seed_jobs(conn)
    print(f"✅ Seeded jobs")
    seed_skills(conn)
    print(f"✅ Seeded skills")
    seed_career_paths(conn)
    print(f"✅ Seeded career paths")
    seed_courses(conn)
    print(f"✅ Seeded courses")
    seed_interview_questions(conn)
    print(f"✅ Seeded interview questions")
    conn.close()

    # Verify
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["jobs", "skills", "career_paths", "courses", "interview_questions"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]
        print(f"   📊 {table}: {count} records")
    conn.close()
    print("\n🚀 Database ready! Run: streamlit run app.py")

if __name__ == "__main__":
    main()
