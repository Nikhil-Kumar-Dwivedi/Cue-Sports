from flask import Flask, render_template, request, redirect, url_for, jsonify
import schedule
import time
import requests
from bs4 import BeautifulSoup
from plyer import notification
from threading import Thread

app = Flask(__name__)


def get_current_matches():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    response = requests.get("https://www.espn.in/football/fixtures?league=eng.1", headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    matches = []
    for section in soup.find_all('div', class_='ScheduleTables'):
        date_title = section.find('div', class_='Table__Title').text if section.find('div', class_='Table__Title') else 'N/A'
        games = section.find_all('tr', class_='Table__TR--sm')
        
        for game in games:
            teams = game.find_all('a', class_='AnchorLink')
            match_info = {
                'date': date_title,
                'home_team': teams[1].text.strip() if len(teams) > 1 else 'N/A',
                'away_team': teams[4].text.strip() if len(teams) > 4 else 'N/A',
                'time': game.find('td', class_='date__col').text.strip() if game.find('td', class_='date__col') else 'N/A',
                'location': game.find('td', class_='venue__col').text.strip() if game.find('td', class_='venue__col') else 'N/A',
            }
            matches.append(match_info)
        
    return matches

def scrape_nba_fixtures():
    url = "https://www.espn.com/nba/schedule"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all date headers
    date_headers = soup.find_all('div', class_='Table__Title')
    
    fixtures = []
    current_date = None

    # Loop through each date section and its respective matches
    for header in date_headers:
        # Set the current date from the header
        current_date = header.text.strip() if header else 'N/A'

        # Find the match rows under each date header section
        match_rows = header.find_next('tbody').find_all('tr', class_='Table__TR Table__TR--sm Table__even')
        
        for row in match_rows:
            # Get the away team
            away_team = row.find('span', class_='Table__Team away')
            away_team = away_team.text.strip() if away_team else 'N/A'

            # Get the home team (second <span> without "away" class)
            home_team = row.find_all('span', class_='Table__Team')
            home_team = home_team[1].text.strip() if len(home_team) > 1 else 'N/A'

            # Get the match time
            match_time = row.find('td', class_='date__col Table__TD').text.strip() if row.find('td', class_='date__col Table__TD') else 'N/A'

            fixture = {
                'away_team': away_team,
                'home_team': home_team,
                'match_time': match_time,
                'match_date': current_date
            }
            fixtures.append(fixture)

    return fixtures

print(scrape_nba_fixtures())

def get_cricket_matches():
    url = "https://sports.ndtv.com/cricket/schedules-fixtures"
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')
    matches = []

    match_divs = soup.find_all('div', class_="sp-scr_wrp vevent")
    for match in match_divs:
        teams = match['data-teama'], match['data-teamb'] if 'data-teama' in match.attrs and 'data-teamb' in match.attrs else ('N/A', 'N/A')
        series = match['data-series'] if 'data-series' in match.attrs else 'N/A'
        venue = match['data-venue'] if 'data-venue' in match.attrs else 'N/A'
        time_info = match.find('div', class_="scr_dt-red").text if match.find('div', class_="scr_dt-red") else 'N/A'
        
        match_info = {
            'teams': teams,
            'series': series,
            'venue': venue,
            'time': time_info,
            'link': match.find('a', class_='sp-scr_lnk url')['href'] if match.find('a', class_='sp-scr_lnk url') else 'N/A',
        }
        matches.append(match_info)

    return matches


scheduled_time = None
previous_matches = {
    'football': [],
    'cricket': [],
    'nba': []
}

def check_for_updates():
    global previous_matches
    current_football_matches = get_current_matches()
    current_cricket_matches = get_cricket_matches()
    current_nba_fixtures = scrape_nba_fixtures()

    updates = []

    
    if current_football_matches != previous_matches.get('football', []):
        updates.append("New Football Matches Available!")
        previous_matches['football'] = current_football_matches

    
    if current_cricket_matches != previous_matches.get('cricket', []):
        updates.append("New Cricket Matches Available!")
        previous_matches['cricket'] = current_cricket_matches

    # NBA
    if current_nba_fixtures != previous_matches.get('nba', []):
        updates.append("New NBA Matches Available!")
        previous_matches['nba'] = current_nba_fixtures

    # Notify 
    if updates:
        notify_user("\n".join(updates))
    else:
        notify_user("No New Matches")

# 
def notify_user(message):
    notification.notify(
        title="Match Updates",
        message=message,
        timeout=10
    )

# 
def schedule_scraping(time_str):
    schedule.every().day.at(time_str).do(check_for_updates)

    while True:
        schedule.run_pending()
        time.sleep(1)

#
@app.route('/')
def index():
    return render_template('index.html')

# 
@app.route('/welcome')
def welcome():
    football_matches = get_current_matches()  # Function to get football matches
    cricket_matches = get_cricket_matches()     # Function to get cricket matches
    nba_fixtures = scrape_nba_fixtures()
    return render_template('welcome.html', football_matches=football_matches, cricket_matches=cricket_matches, nba_fixtures=nba_fixtures)

# Route for loading matches via AJAX
@app.route('/load_matches', methods=['GET'])
def load_matches():
    sport = request.args.get('sport')
    if sport == 'football':
        matches = get_current_matches()
        return jsonify(matches)
    elif sport == 'cricket':
        matches = get_cricket_matches()
        return jsonify(matches)
    elif sport == 'nba':
        fixtures = scrape_nba_fixtures()
        return jsonify(fixtures)
    return jsonify([])

# Route for the settings page
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    global scheduled_time
    if request.method == 'POST':
        # Get the scheduled time from the form
        scheduled_time = request.form['time']
        
        # Schedule the scraping at the specified time
        thread = Thread(target=schedule_scraping, args=(scheduled_time,))
        thread.start()
        
        return redirect(url_for('settings'))
    
    return render_template('settings.html')

# Other routes...
# Route for the community page
@app.route('/community')
def community():
    return render_template('community.html')


previous_headings_livemint = []
previous_headings_indianexpress = []

def fetch_livemint_headlines():
    url = 'https://www.livemint.com/sports'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return [heading.get_text(strip=True) for heading in soup.find_all('h2', class_='headline')]

def fetch_indianexpress_headlines():
    url = 'https://indianexpress.com/section/sports/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return [heading.get_text(strip=True) for heading in soup.find_all('h2')]



# Route for the news page
@app.route('/news')
def news():
    global previous_headings_livemint, previous_headings_indianexpress

    # Fetch the current headlines
    current_headings_livemint = fetch_livemint_headlines()
    current_headings_indianexpress = fetch_indianexpress_headlines()

    # Check for updates in Livemint headlines
    if current_headings_livemint != previous_headings_livemint:
        livemint_updates = current_headings_livemint
        previous_headings_livemint = current_headings_livemint
    else:
        livemint_updates = []


    # Check for updates in Indian Express headlines
    if current_headings_indianexpress != previous_headings_indianexpress:
        indianexpress_updates = current_headings_indianexpress
        previous_headings_indianexpress = current_headings_indianexpress
    else:
        indianexpress_updates = []

    # Render the news.html template with the headlines
    return render_template('news.html', livemint_updates=livemint_updates, indianexpress_updates=indianexpress_updates)

# Route for Dipti Ma'am Suggestion page
@app.route('/dipti')
def dipti():
    return render_template('ticket.html')

# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for the logout page
@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
