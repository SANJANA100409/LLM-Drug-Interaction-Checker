# 💊 LLM Drug Interaction Checker

A Streamlit-based application that detects **drug–drug interactions** using a locally generated database.  
Every possible drug pair in the database has a realistic medical interaction, so you’ll never get a “No interaction found” result.

---

## 🚀 Features
- Search drug interactions by brand or generic names.
- Automatically maps brand names to generics.
- Displays realistic interaction descriptions.
- Shows possible side effects for each drug.
- Fully offline — no API calls needed.
- Built using **Python**, **Streamlit**, and **JSON databases**.

---

## 📂 Project Structure
LLM-Drug-Interaction-Checker/
│
├── app.py # Streamlit frontend
├── generate_interactions.py # Script to generate interactions database
├── drug_name_mapping.json # Brand→Generic mappings
├── interactions_db.json # Auto-generated interactions data
├── side_effects_db.json # Auto-generated side effects data
└── README.md # Project documentation

## 🛠 Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/SANJANA100409/LLM-Drug-Interaction-Checker.git
   cd LLM-Drug-Interaction-Checker
Create and Activate a Virtual Environment

python -m venv venv
venv\Scripts\activate
Install Requirements

pip install -r requirements.txt
Generate the Interaction Database

python generate_interactions.py
✅ This loads the drug mapping, creates all possible drug–drug interaction pairs, and saves them to:

interactions_db.json

side_effects_db.json

Run the App

streamlit run app.py
The app will open in your default browser.

🧪 Example Test Cases
Here are some example drug pairs guaranteed to return interactions:

Paracetamol + Ibuprofen

Aspirin + Metformin

Amoxicillin + Atorvastatin

Ibuprofen + Metformin

Aspirin + Paracetamol

📜 How It Works
drug_name_mapping.json contains brand→generic mappings.

generate_interactions.py:

Reads the mapping file.

Generates every possible pair of generic drugs.

Assigns realistic-sounding interaction descriptions.

Assigns side effects from a predefined set or a default list.

app.py:

Takes two drug names from user input.

Maps them to generic names.

Looks up their interaction and side effects.

Displays them in a clean Streamlit UI.

📌 Technologies Used
Python 3

Streamlit (UI)

JSON (Data storage)

itertools & random (Pair generation)

👩‍💻 Author
Sanjana S
📧 Email: sanjana.s091004@gmail.com
🌐 GitHub: SANJANA100409
