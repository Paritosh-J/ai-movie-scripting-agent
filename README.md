# AI Movie Scripting Agent 🎬🤖✨

**Turn your movie ideas into full script outlines and casting suggestions instantly!**

This application uses a multi-agent AI team to act as your personal **Script Writer** and **Casting Director**. Powered by **Gemini 2.5 Flash** and **SerpApi**, it generates creative plotlines and finds real-world actors suitable for the roles.

---

## ⭐ Features

- **📝 Intelligent Script Generation**: Creates detailed script outlines, including 3-act structures, character arcs, and plot twists.
- **🎭 Smart Casting**: Suggests real actors for roles based on descriptions and checks their current status using Google Search.
- **⚙️ Customizable**: Tailor the output by selecting genre, target audience, and runtime.
- **🤝 Multi-Agent Collaboration**: Orchestrated by a "Movie Producer" agent that manages the workflow between the writer and casting director.

## 🛠️ Tech Stack

- **Python** 🐍
- **Streamlit** (User Interface) 👆
- **Agno** (Agentic Framework) 🧠
- **Gemini 2.5 Flash** (LLM) 🤖
- **SerpApi** (Real-time Google Search) 🔍

## 📋 Prerequisites

Before you begin, ensure you have the following:

- **Python 3.9+** installed.
- An **[Google API Key](https://aistudio.google.com/)**.
- A **[SerpApi Key](https://serpapi.com/)** (for Google Search capabilities).

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai-movie-scripting-agent
   ```

2. **Create a virtual environment** (Recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the root directory and add your keys:
   ```env
   GOOGLE_API_KEY=your-api-key
   SERP_API_KEY=your-api-key
   ```

## ▶️ Usage

Run the Streamlit application:

```bash
streamlit run ai-movie-scripting-agent.py
```

Once the app opens in your browser:
1. Enter your **Movie Idea**.
2. Select a **Genre** and **Target Audience**.
3. Set the **Runtime**.
4. Click **Generate Script 📝**.

---

*Happy Scripting!* 🍿