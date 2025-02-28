import streamlit as st
import requests
import pyttsx3
import speech_recognition as sr
import random

# Currency API for real-time exchange rates
CURRENCY_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

# Unit conversion dictionary
CONVERSIONS = {
    "Length": {"Meter": 1, "Kilometer": 0.001, "Mile": 0.000621371, "Foot": 3.28084, "Inch": 39.3701},
    "Weight": {"Kilogram": 1, "Gram": 1000, "Pound": 2.20462, "Ounce": 35.274},
    "Temperature": {"Celsius": lambda x: x, "Fahrenheit": lambda x: x * 9/5 + 32, "Kelvin": lambda x: x + 273.15},
    "Volume": {"Liter": 1, "Milliliter": 1000, "Gallon": 0.264172, "Cup": 4.16667},
}

# Text-to-Speech function
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to fetch live currency exchange rates
def get_exchange_rates():
    try:
        response = requests.get(CURRENCY_API_URL)
        return response.json().get("rates", {})
    except:
        return {}

# UI Styling
st.set_page_config(page_title="ConvertEase", layout="wide")
st.markdown("""
    <style>
        .main { background-color: #f4f4f8; }
        h1 { color: #ff4b4b; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🔄 ConvertEase - Effortless Conversions")
st.sidebar.title("Options")

# Conversion Type Selection
conversion_type = st.sidebar.selectbox("Select Conversion Type", list(CONVERSIONS.keys()) + ["Currency"])

if conversion_type != "Currency":
    units = list(CONVERSIONS[conversion_type].keys())
    from_unit = st.selectbox("From Unit", units)
    to_unit = st.selectbox("To Unit", units)
    value = st.number_input("Enter Value", min_value=0.0, step=0.1)

    # Convert the value
    if conversion_type == "Temperature":
        converted_value = CONVERSIONS[conversion_type][to_unit](value)
    else:
        converted_value = value * (CONVERSIONS[conversion_type][to_unit] / CONVERSIONS[conversion_type][from_unit])

    st.success(f"{value} {from_unit} = {converted_value:.2f} {to_unit}")

    # Voice Output
    if st.button("🔊 Speak Result"):
        speak(f"{value} {from_unit} is equal to {converted_value:.2f} {to_unit}")

else:
    rates = get_exchange_rates()
    if rates:
        from_currency = st.selectbox("From Currency", rates.keys())
        to_currency = st.selectbox("To Currency", rates.keys())
        amount = st.number_input("Enter Amount", min_value=0.0, step=0.1)
        converted_currency = amount * rates[to_currency] / rates[from_currency]
        st.success(f"{amount} {from_currency} = {converted_currency:.2f} {to_currency}")
    else:
        st.error("Failed to fetch live exchange rates.")

# Sidebar Styling
st.sidebar.markdown("## 🌟 Welcome to ConvertEase!")
st.sidebar.markdown("---")

# 📜 Project Details & How It Works
st.sidebar.subheader("📜 About ConvertEase")
with st.sidebar.expander("ℹ️ About This App"):
    st.markdown("""
    **ConvertEase** is an interactive tool that allows users to convert units, learn fun facts, and test their knowledge with quizzes.  
    This app is designed to be engaging, educational, and easy to use!
    """)

with st.sidebar.expander("🛠️ Features"):
    st.markdown("""
    - 🎉 **Fun Facts**: Learn interesting facts every time you visit.
    - 🎮 **Quiz Mode**: Test your knowledge with interactive quizzes.
    - 📏 **Unit Converter**: Convert between different units easily.
    - 🔢 **Conversion Formulas**: Understand how conversions work.
    """)

with st.sidebar.expander("🚀 How It Works"):
    st.markdown("""
    1️⃣ **Select a Unit to Convert** – Choose the unit and enter a value.  
    2️⃣ **Get the Converted Value** – The app instantly converts the value.  
    3️⃣ **Explore Fun Facts** – A new fact is displayed every time you visit.  
    4️⃣ **Take a Quiz** – Answer fun trivia questions and check your score!  
    """)

st.sidebar.markdown("---")

# 🎉 Fun Facts Section
st.sidebar.subheader("🎉 Fun Fact of the Day")

FUN_FACTS = [
    "A nautical mile is based on the Earth's circumference!",
    "One liter of water weighs exactly one kilogram!",
    "The Fahrenheit scale was based on freezing brine!",
    "Bananas are berries, but strawberries aren’t!",
    "Octopuses have three hearts!",
    "There’s no solid land at the North Pole—just ice!",
    "Water can boil and freeze at the same time!",
]

# Display a random fun fact
st.sidebar.info(random.choice(FUN_FACTS))

st.sidebar.markdown("---")

# 🎮 Gamification: Quiz Mode
st.sidebar.subheader("🎮 Quiz Mode")

quiz_questions = {
    "How many feet are in a mile?": {"correct": "5280", "options": ["5000", "5280", "5500"]},
    "What is the freezing point of water in Fahrenheit?": {"correct": "32", "options": ["0", "32", "100"]},
    "Which planet is known as the Red Planet?": {"correct": "Mars", "options": ["Venus", "Mars", "Jupiter"]},
    "How many continents are there on Earth?": {"correct": "7", "options": ["5", "6", "7"]},
}

# Select a question
question = st.sidebar.selectbox("❓ Select a Question", list(quiz_questions.keys()))
options = quiz_questions[question]["options"]
answer = st.sidebar.radio("🔎 Choose an Answer", options)

# Submit button with feedback
if st.sidebar.button("✅ Submit Answer"):
    if answer == quiz_questions[question]["correct"]:
        st.sidebar.success("🎉 Correct! Well done!")
    else:
        st.sidebar.error("❌ Try again! Keep going!")

st.sidebar.markdown("---")

st.sidebar.markdown("💡 *Learn something new every day!*")