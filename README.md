# Afloat: Your AI Concierge for Mental Wellness & Productivity

> **Capstone Project for the Google x Kaggle 5-Day AI Agents Course**

**Afloat** is an AI-powered personal concierge designed to help manage day-to-day life when things feel overwhelming. It acts as a bridge between your natural language conversations and a structured life management system.

## Core Features 

### 1. Unified Task & Habit Manager
Afloat merges standard to-do lists with recurring self-care habits.
* **Smart Capture:** Simply tell the agent "Remind me to submit my project" or "I need to walk every morning."
* **One-Off Tasks:** Handles single-occurrence events (e.g., "Email the professor").
* **Recurring Habits:** Tracks daily/weekly essentials (e.g., "Sunlight exposure," "Wash sheets").

### 2. Intelligent Mood Tracker
Afloat listens to your conversations to track your well-being over time.
* **Conversational Logging:** No need to fill out forms. The agent extracts mood and context directly from your chat.
* **Pattern Recognition:** Stores emotional context to help you reflect on your mental health patterns.

---

##  Technical Architecture
* **Model:** Google Gemini
* **Agent Pattern:** Concierge / Tool-Use
* **Database:** SQLite (local persistent storage for tasks and logs)
* **Tools:**
    * `add_task(description, frequency)`
    * `log_mood(emotion, notes)`
    * `query_status()`

---

##  Future Roadmap (Planned Features)
* **Resource Tracker:** Management for budget, groceries, and medications.
* **Advanced Analytics:** Visual graphs of mood vs. task completion rates.
* **External Integrations:** Calendar and Email APIs.