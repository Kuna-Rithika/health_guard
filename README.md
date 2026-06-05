# HealthGuard

An AI-powered Multi-Agent Health Assistant that analyzes symptoms, assesses health risks, tracks medical history, and provides personalized wellness recommendations through voice or text input.

## Problem Statement

Many people ignore early symptoms until conditions become serious. Traditional symptom checkers are often static, non-personalized, and unable to learn from a user's health history.

## Solution

HealthGuard uses a team of specialized AI agents that work together to analyze symptoms, detect patterns, assess risk levels, predict potential health concerns, and provide personalized guidance. The system maintains user health history and delivers intelligent recommendations in real time.

## 8 AI Agents

* Security Agent – Validates and sanitizes user input
* Symptom Agent – Extracts symptom information
* Clarification Agent – Identifies missing details
* Pattern Detection Agent – Detects recurring health issues
* Risk Assessment Agent – Calculates health risk levels
* Predictive Agent – Predicts future health concerns
* Emergency Agent – Provides emergency guidance
* Wellness Agent – Recommends lifestyle improvements

## Tech Stack

-Frontend: HTML, CSS, JavaScript, Web Speech API
-Backend: FastAPI, Python, JWT Authentication
-Database: Neon PostgreSQL
-AI: Groq API, Lyzr Multi-Agent Framework
-Memory: Qdrant Vector Database
-Voice Interface: Omi
-Reporting: ReportLab PDF Generator

## How to Run

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Initialize Database

```bash
python backend/database.py
```

### Run Backend

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

### Serve Frontend

```bash
cd frontend
python -m http.server 8001
```

Open:

```text
http://127.0.0.1:8001
```

Backend API Docs:

```text
http://127.0.0.1:8000/docs
```

## Features

* User Signup and Login
* Voice-Based Symptom Input
* Multi-Agent AI Analysis
* Risk Classification (LOW / MEDIUM / HIGH / CRITICAL)
* Personalized Health Recommendations
* Dynamic Dashboard
* User Profile Management
* Health History Tracking
* PDF Report Generation
* Real-Time AI Response

## Workflow

User Login → Voice/Text Symptom Input → AI Analysis → Pattern Detection → Risk Assessment → Predictive Analysis → Emergency/Wellness Response → History Storage → Report Generation
