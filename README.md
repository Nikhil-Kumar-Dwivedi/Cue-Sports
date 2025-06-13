# 🏟️ Sports Fixture Notifier 

A dynamic Flask-based web application that scrapes and displays the latest **Football**, **NBA**, and **Cricket** match fixtures from top sources. It allows users to browse upcoming matches, schedule desktop notifications for updates, and view trending sports news.

---

## 📌 Features

- **Live Match Fixture Scraping**
  - Football Fixtures from [ESPN - Premier League](https://www.espn.in/football/fixtures?league=eng.1)
  - NBA Fixtures from [ESPN - NBA](https://www.espn.com/nba/schedule)
  - Cricket Fixtures from [NDTV Sports](https://sports.ndtv.com/cricket/schedules-fixtures)

- **Desktop Notifications**
  - Sends notifications using `plyer` if any new fixtures are detected for Football, NBA, or Cricket.

- **Daily Scheduling**
  - Users can select a time from the `/settings` page to auto-scrape and notify them daily.

- **Live Sports News**
  - Displays top headlines scraped from:
    - [LiveMint Sports](https://www.livemint.com/sports)
    - [Indian Express Sports](https://indianexpress.com/section/sports/)

- **AJAX-Powered Match Loader**
  - Dynamically loads matches for selected sports without reloading the entire page.

- **Additional Pages**
  - `/community`, `/about`, `/dipti` for extra content or future features.

---

## 🏗️ Project Structure
/project-root
│
├── app.py                  # Main Flask backend
├── templates/
│   ├── index.html
│   ├── welcome.html
│   ├── news.html
│   ├── settings.html
│   ├── community.html
│   ├── about.html
│   ├── ticket.html
│
├── static/                 
├── requirements.txt
└── tempCodeRunnerFile.py



## ⚙️ Tech Stack

Backend: Python 3.x, Flask

Scraping: BeautifulSoup4, Requests

Notifications: Plyer

Scheduling: Schedule

Frontend: HTML, Bootstrap (optional), AJAX (for dynamic loading)


## 📅 Scheduling Notifications

Go to http://localhost:5000/settings

Choose your preferred time (e.g., 14:30)

The app will check for updates daily at the selected time and notify you if there are changes in any sport's schedule.

Note: Keep the app running in the background for notifications to work.



## 🧪 Example Output (Notification)
🏆 Match Updates

New Football Matches Available!

New NBA Matches Available!


## 🗃 Requirements File (requirements.txt)
Flask
requests
beautifulsoup4
plyer
schedule


## 📢 Credits
Football & NBA Fixtures: ESPN

Cricket Schedules: NDTV Sports

News Headlines: LiveMint & IndianExpress

Notifications: Plyer Python Library


## SCREENSHOTS

![Screenshot 2024-12-02 234141](https://github.com/user-attachments/assets/e470828f-c474-4fc0-9f8d-bf179e958e5c)

![Screenshot 2024-12-02 234237](https://github.com/user-attachments/assets/d2f14280-1b2a-4760-b28c-2f48d3f7c488)

![Screenshot 2024-12-02 234248](https://github.com/user-attachments/assets/02ed6a64-9b73-4ec6-8370-6a06f35f453a)

![Screenshot 2024-12-02 234303](https://github.com/user-attachments/assets/5cb7562e-ffbe-4461-8833-c6edd7fe4d1c)

![Screenshot 2024-12-02 234315](https://github.com/user-attachments/assets/7e213eb3-64f0-4e11-82f4-7830f3cc79d9)



