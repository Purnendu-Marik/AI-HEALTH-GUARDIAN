# 🩺 AI Health Guardian

AI-powered health assessment and preventive health insights web application.

AI Health Guardian is a web-based application that analyzes user-provided health information and generates general, educational and preventive health insights using rule-based analysis and AI.

> ⚠️ This application is designed for educational and preventive purposes only. It does not provide medical diagnosis or replace professional medical advice.

---

## 📌 Project Overview

AI Health Guardian allows users to:

- Create an account and securely log in
- Provide basic health information
- Select reported symptoms
- Provide sleep and physical activity information
- Receive a rule-based health assessment
- Generate personalized AI-powered health insights
- View key observations and lifestyle suggestions
- Receive guidance about when professional medical help may be appropriate

The project combines a **FastAPI backend**, **SQLite database**, **SQLAlchemy ORM**, and **Groq API with Llama 3.3 70B** to provide an interactive health assessment experience.

---

## ✨ Key Features

### 🔐 User Authentication
- User registration
- User login
- Session-based authentication
- Password hashing
- SQLite-based user storage

### 🩺 Health Assessment
Users can provide:

- Age
- Gender
- Symptoms
- Sleep duration
- Physical activity level
- Additional information

### 📊 Rule-Based Health Analysis

The application evaluates the submitted information using a basic rule-based analysis engine and generates:

- Overall health status
- Key observations
- General recommendations
- Reported symptoms

### 🤖 AI-Powered Health Insights

The application uses the Groq API with the **Llama 3.3 70B** model to generate:

- Overall health insight
- Key insights
- Lifestyle suggestions
- Guidance on when to seek professional help

### 🎨 User Interface

The application includes:

- Modern dark-themed interface
- Responsive web pages
- Health assessment form
- Login and signup pages
- AI-powered result page
- Interactive navigation

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      User / Client   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   HTML / CSS UI      │
                    │   Jinja2 Templates   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    FastAPI Backend   │
                    │       main.py        │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
      │ Authentication│ │    Health    │ │ AI Service   │
      │    Service    │ │   Analyzer   │ │    Groq      │
      └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                    ┌──────────────────────┐
                    │   SQLite Database    │
                    │     SQLAlchemy       │
                    └──────────────────────┘
