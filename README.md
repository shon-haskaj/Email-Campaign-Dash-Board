# 🚀 Automated Mailchimp & Twitter/X Scraper with Google Sheets Integration  

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Selenium](https://img.shields.io/badge/Selenium-Automation-green.svg)
![Mailchimp API](https://img.shields.io/badge/Mailchimp-API-red.svg)
![Google Sheets API](https://img.shields.io/badge/Google%20Sheets-Integration-yellow.svg)
![Web Scraper](https://img.shields.io/badge/Web%20Scraper-Dynamic-blueviolet.svg)

> A **powerful** automation tool that fetches Mailchimp campaign data, scrapes **Twitter/X** dynamically using **Selenium**, and updates a **Google Sheet**—all in one go!  

🔹 **Mailchimp API**: Fetches campaign statistics (open rate, click rate, emails sent).  
🔹 **Selenium Scraper**: Extracts **live tweet data** dynamically, even with infinite scrolling!  
🔹 **Google Sheets API**: Updates a spreadsheet automatically with campaign & scraped data.  

---

## 📸 Demo & How It Works  

### 🎥 **Automated Data Collection**
<img src="https://media.giphy.com/media/l1J9EdzfOSgfyueLm/giphy.gif" width="600" />

1. ✅ Fetches **Mailchimp** campaign reports.  
2. ✅ Scrapes **Twitter/X** dynamically using Selenium.  
3. ✅ Writes everything neatly into **Google Sheets**.  

---

## 📜 Features  

✅ **Dynamic Web Scraping** – No static HTML, handles infinite scrolling & pop-ups.  
✅ **Google Sheets API** – Automates spreadsheet updates with real-time data.  
✅ **Mailchimp API** – Fetches email campaign analytics.  
✅ **Optimized with Logging** – Tracks progress and handles errors gracefully.  

---

## 🚀 Installation & Setup  

### 🔧 **Prerequisites**  
- Install **Python 3.8+**  
- Install **Google Chrome** & **ChromeDriver**  

### 📦 **Clone & Install Dependencies**  

```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
```

### ⚒️ Configure API Keys & Credentials

1. Mailchimp API:
	- Get your API key from Mailchimp API Settings.
	- Set your Mailchimp data center (the part after the hyphen in your API key) and list ID.
2. Google Sheets API:
	- Enable the Google Sheets API and download your credentials.json file from the Google API Console.
	- Place the credentials.json in the project folder and update the constants in main.py.

---

## 📌 Usage
Run the project using:
```sh
python main.py
```

---

## 🏗️ Project Structure
Email-Campaign-Dashboard/
│
├── main.py          # Contains all project logic (Mailchimp, scraping, and Sheets integration)
├── README.md        # This file: Overview, setup, and usage instructions
├── requirements.txt # List of Python dependencies
└── .gitignore       # Specifies files/folders to be ignored by Git

---

## 🤖 Tech Stack
- Python – Core language
- Selenium – Dynamic web scraping
- Mailchimp API – Fetches campaign insights
- Google Sheets API – Manages spreadsheet data

---

## 💡 Future Enhancements

- [ ] Login Handling for Twitter/X: Implement advanced authentication.
- [ ] Multiple Mailchimp Lists Support: Handle more than one audience.
- [ ] Dashboard Visualization: Create a UI for data analytics.

---

## 👨‍💻 Author & License

Created by Shon Haskaj.

This project is licensed under the MIT License.
If you found this project useful, please give it a star!
