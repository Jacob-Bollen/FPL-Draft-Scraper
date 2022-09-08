<h3 align="center">FPL Draft Scraper</h3>

  <p align="center">
    Returns .csv files of gameweek scores for each squad as well as a detailed breakdown of the players stats for each gameweek.
    Useful for analysis and visualisation of each squad's performance.
    <br />
    
  </p>
</div>




<!-- ABOUT THE PROJECT -->
## About The Project

Although an API exists for the regular Fantasy Premier League game, it is harder to extract data of a draft league.
This code should allow users to get a csv file of the useful data from the league for further analysis.








### Prerequisites

The scraper requires the latest version of ChromeDriver
You can download it from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)





## Usage

It is necessary to login and complete a CAPTCHA to allow the script to scrape the data.

`gw_scores` returns a csv file with each team and their score each week as well as their respective totals.
`player_details` returns a csv file with the players in each squad each week along with the stats provided on FPL
The columns in the csv file are:

'team_name', 'gw', 'name', 'POS', 'MP', 'GS', 'A', 'CS', 'GC', 'OG', 'PS', 'PM', 'YC', 'RC', 'S', 'B', 'BPS', 'I', 'C', 'T', 'II', 'benched'

Further details of each stat can be found on the information tab for each player on the FPL website.

