# 🃏 Poker Hand Strength Generator

## 🎯 Overview
The **Poker Hand Strength Generator** is a Python-based tool that evaluates poker hands, calculates their strength, and provides AI-driven strategic advice. It integrates **probability calculations, AI recommendations, and card deck simulation** to help users analyze their chances of winning in a given poker hand scenario.

## 🚀 Features
- **Hand Evaluation:** Determines hand rankings (e.g., Royal Flush, Straight, Two Pair) using `deuces`.
- **Probability Calculation:** Estimates the likelihood of winning based on known cards and community cards.
- **AI-Powered Advice:** Uses **Google Gemini AI** to suggest the best strategy (Raise, Call, or Fold).
- **Card Drawing Simulation:** Fetches randomized card draws via **Deck of Cards API**.
- **Streamlit UI:** Interactive web interface for user input and result visualization.

## 🔧 Setup Instructions
### 1️⃣ Install Required Dependencies
Ensure you have Python installed, then install the required libraries:
```sh
pip install streamlit deuces2 requests google-generativeai
```

### 2️⃣ Set Up Google Gemini API Key
To enable AI-powered recommendations, **enter a valid Google Gemini API key** in the script:
```python
genai.configure(api_key="YOUR_GOOGLE_GEMINI_API_KEY")
```

### 3️⃣ Run the Poker Hand Generator
Launch the Streamlit app using:
```sh
streamlit run Poker.py
```

## 🏆 How It Works
1. **Input Hole Cards** – Enter your two personal poker cards.
2. **Simulate Community Cards** – Draw random community cards from the API.
3. **Hand Strength Evaluation** – The script ranks your hand from best to worst (1 = strongest, 7462 = weakest).
4. **AI-Driven Strategy Advice** – AI suggests whether to **Raise, Call, or Fold** based on hand strength.

## 📜 Key Scripts
- **Poker.py** – Main script handling UI, game logic, and AI integration.
- **Hand Evaluation Module (`deuces`)** – Computes hand rankings and comparisons.
- **AI Integration (`google-generativeai`)** – Provides strategic poker recommendations.
- **Card API (`requests`)** – Fetches random card draws for realistic simulations.

## 🤖 Future Enhancements
- **Monte Carlo simulations** for deeper probability analysis.
- **Opponent AI modeling** for advanced strategic decisions.
- **Multi-player mode** for simulated online poker hands.

🎯 *Ready to dominate your poker hands? Run the script and start analyzing your odds!* 🚀♠️♦️♣️♥️


