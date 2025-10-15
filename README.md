# DemandFlow — AI-Powered Demand Planner

A full-stack web application that predicts product demand, visualizes sales trends, and generates AI-driven insights, using **free open-source models (Microsoft Phi-3 Mini)**.

# Features

- Upload CSV sales data and auto-generate forecasts (Prophet)
- AI summaries powered by Microsoft Phi-3 Mini (no API key needed)
- PostgreSQL database to store results & insights
- FastAPI backend + React frontend (modern UI)
- Interactive charts using Recharts

# Tech Stack

| Layer               | Technologies                                         |
| ------------------- | ---------------------------------------------------- |
| **Frontend**        | React, TailwindCSS, Recharts, Framer Motion          |
| **Backend**         | FastAPI, Python, SQLAlchemy, PostgreSQL              |
| **AI Model**        | Microsoft Phi-3 Mini (via Hugging Face Transformers) |
| **Version Control** | Git + GitHub                                         |

# Setup Instructions

# Clone the repository

git clone https://github.com/<your-username>/demandflow.git
cd demandflow

# Backend setup

cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend setup

cd ../frontend
npm install
npm run dev

# Environment variables

Create .env file in the backend folder like this backend/.env:
Replace username and the password with you have set for your account.
DATABASE_URL=postgresql+psycopg2://postgres:<your_password>@localhost:5432/demandflow
