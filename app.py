import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from io import BytesIO

# Streamlit App Title
st.title("Transfermarkt Player Data Scraper 🏆")

# User input for the Transfermarkt URL
url = st.text_input("Enter Transfermarkt URL (Detailed Stats Only):")

# Headers to mimic a real browser visit (rotating User-Agents)
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.7; rv:134.0) Gecko/20100101 Firefox/134.0"
]

# Competitions to exclude
EXCLUDED_COMPETITIONS = {'UNLB', 'FS', 'EM24'}

# Function to scrape match data
def scrape_match_data(competition_box, league_name):
    """Extracts match data from a given competition table."""
    match_data = []

    # Find the table inside the box
    responsive_table = competition_box.find('div', class_='responsive-table')
    if not responsive_table:
        return []

    table = responsive_table.find('table')
    if not table:
        return []

    # Extract all rows from the table body
    for row in table.find('tbody').find_all('tr'):
        columns = row.find_all('td')

        # Extract data based on column index
        matchday = columns[0].text.strip() if len(columns) > 0 else None
        date = columns[1].text.strip() if len(columns) > 2 else None
        home_team = columns[3].text.strip() if len(columns) > 4 else None
        away_team = columns[5].text.strip() if len(columns) > 6 else None
        substitutions_on = columns[14].text.strip() if len(columns) > 14 else None
        substitutions_off = columns[15].text.strip() if len(columns) > 15 else None
        minutes_played = columns[-1].text.strip() if len(columns) > -1 else None

        # Append row data
        match_data.append({
            'Matchday': matchday,
            "Date": date,
            'Home Team': home_team,
            'Away Team': away_team,
            'Substitutions On': substitutions_on,
            'Substitutions Off': substitutions_off,
            'Minutes Played': minutes_played,
            'League': league_name
        })

    return match_data

# Function to scrape the webpage and generate data
def scrape_transfermarkt(url):
    # Add a small delay to mimic human behavior
    time.sleep(random.uniform(2, 4))

    # Get a random user-agent
    headers = {"User-Agent": random.choice(user_agents)}

    # Send a GET request to the URL with headers
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        st.error("Failed to fetch data. Please check the URL.")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # List to store extracted data
    all_match_data = []

    # Find all divs with class 'box' (each representing a competition)
    for box in soup.find_all('div', class_='box'):
        # Extract the competition name
        comp_header = box.find('a', href=True)
        if comp_header and 'name' in comp_header.attrs:
            comp_name = comp_header['name']

            # Skip excluded competitions
            if comp_name in EXCLUDED_COMPETITIONS:
                continue
        else:
            continue  # Skip if no valid competition name found

        # Scrape match data from this competition
        match_data = scrape_match_data(box, comp_name)
        all_match_data.extend(match_data)

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(all_match_data)
    return df

# Button to start scraping
if st.button("Scrape Data"):
    if not url:
        st.error("Please enter a valid Transfermarkt URL.")
    else:
        with st.spinner("Scraping data... Please wait ⏳"):
            df = scrape_transfermarkt(url)
            if df is not None and not df.empty:
                st.success("Data successfully scraped! 🎉")

                # Display DataFrame in Streamlit
                st.dataframe(df)

                # Convert DataFrame to Excel and create a download link
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name="Match Data")
                    writer.book.close()
                output.seek(0)

                st.download_button(
                    label="📥 Download Excel File",
                    data=output,
                    file_name="player_performance_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("No data found. Make sure the URL is correct and the page is accessible.")



