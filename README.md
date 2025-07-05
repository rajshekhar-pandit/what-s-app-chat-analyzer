# what-s-app-chat-analyzer

# 📊 WhatsApp Chat Analyzer

A Python-based tool to analyze WhatsApp chat data. Gain insights into your conversations through message statistics, activity patterns, most active users, and more—visualized with graphs and word clouds.

---

## ✅ Features

- 🔍 Analyze message counts, words, emojis, media, and links
- 📅 Track daily, weekly, and monthly activity
- ⏰ Identify most active hours and days
- 👥 Analyze group chat participants individually
- 🧠 Generate word clouds of commonly used words
- 📈 Create graphical reports with Matplotlib / Seaborn / Plotly
- 🗃 Supports export of results and visuals

---

## 🛠️ Tech Stack

- **Language:** Python 🐍
- **Libraries:** 
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `emoji`
  - `wordcloud`
  - `streamlit` (for web app UI, optional)

---

## 🧑‍💻 Installation & Usage

### 🔧 Prerequisites

- Python 3.x installed
- WhatsApp chat file (`.txt`) exported from phone

### 💻 Local Setup

```bash
# Clone the repo
git clone https://github.com/your-username/whatsapp-chat-analyzer.git

# Navigate to the directory
cd whatsapp-chat-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the analyzer (Streamlit version)
streamlit run app.py




whatsapp-chat-analyzer/
├── app.py                # Main Streamlit web app
├── analyzer.py           # Core logic for parsing and analysis
├── requirements.txt      # Python dependencies
├── sample_chat.txt       # Sample WhatsApp chat
├── assets/               # Images, icons, etc.
└── README.md             # You're here!



