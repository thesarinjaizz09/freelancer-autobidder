# 🤖 Freelancer AutoBidder  
### _AI-Powered Bidding Automation Bot for Freelancer.com_

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-Automation-green?logo=selenium&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🚀 Overview

**Freelancer AutoBidder** is an intelligent automation system that scans, filters, and auto-submits project bids on [Freelancer.com](https://www.freelancer.com/) — all while maintaining human-like precision and control.

This bot handles everything from **login**, **project scraping**, and **filtering irrelevant jobs** to **auto-filling and submitting proposals**.  
It’s designed for professionals, freelancers, and agencies looking to save time while maintaining bidding efficiency and consistency.

---

## ✨ Features

| Category | Description |
|-----------|--------------|
| 🧠 **AI-Generated Proposals** | Automatically generates smart, context-aware bid proposals based on project title and description. |
| 🔍 **Smart Project Filtering** | Filters out irrelevant or low-value projects using custom keyword filters (e.g., `wordpress`, `shopify`, etc.). |
| 💾 **Persistent Storage** | Saves submitted and skipped bids locally to avoid duplicates and repeated submissions. |
| 📊 **Bid Analytics** | Tracks total and session-based bids placed, skipped, or filtered in real-time. |
| 🧾 **Budget Parsing** | Automatically extracts minimum and maximum bid ranges to place smart offers. |
| 🤖 **Auto Submission** | Fills in project details, selects duration (days/hours), and submits bids automatically. |
| 🔒 **Credential Secure** | Handles login automatically — credentials are kept locally and never exposed. |

---

## 🧩 Tech Stack

- **Python 3.10+**
- **Selenium WebDriver**
- **ChromeDriver Manager**
- **WebDriverWait / EC Conditions**
- **JSON Storage for Caching**
- **Custom AI Proposal Generator**

---

## ⚙️ Installation & Setup

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/freelancer-autobidder.git
   cd freelancer-autobidder
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure credentials**
   Edit your credentials in `.env`:
   ```python
   EMAIL = "your-email@example.com"
   PSSWD = "your-password"
   OPENAI_API_KEY = "your-key"
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

---

## 📁 File Structure

```
freelancer-autobidder/
│
├── main.py                # Core automation & bidding logic
├── bid_generator.py       # Proposal generator logic (AI/Template-based)
├── submitted_bids.json    # Stores successful bids
├── skipped_bids.json      # Stores skipped project data
├── requirements.txt       # Dependencies
└── README.md              # This documentation
```

---

## 🧠 How It Works

1. Logs into Freelancer.com automatically using Selenium.  
2. Scrapes projects and identifies new postings in your preferred skill set.  
3. Filters out low-value or irrelevant projects.  
4. Generates personalized, context-aware proposals using your templates or AI prompts.  
5. Submits the bid and records the project locally to prevent duplicate submissions.

---

## 🧰 Customization

- Modify **`exclude_keywords`** in `main.py` to ignore specific project types.  
- Adjust **budget thresholds**, **proposal templates**, or **delay timings** for your use case.  
- Extend `bid_generator.py` to integrate with OpenAI or your own proposal logic.

---

## ⚠️ Disclaimer

This tool is built **for educational and personal use only**.  
Automating platform interactions may violate Freelancer.com’s terms of service — use responsibly and at your own risk.  
The author is not liable for any misuse, account bans, or damages resulting from automation.

---

## 💡 Author

**👨‍💻 Developed by [Sarin Jaiswal](https://github.com/thesarinjaizz09)**  
Founder — **Alphafusion Corporation** 🛡️  
> _"There is nothing we cannot build. Anything you think, we build it."_

---

## ⭐ Support & Contributions

If you like this project, consider starring ⭐ the repository!  
Pull requests and feature suggestions are always welcome. 🙌

---

**🦾 Freelancer AutoBidder — Automate your bidding. Maximize your time.**
