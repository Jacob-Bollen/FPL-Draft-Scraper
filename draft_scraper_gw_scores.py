from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from selenium import webdriver
import time
import re
from draft_functions import get_details, get_gw_scores

def main():
    """
    Returns a csv file containing the gameweek scores for each team.
    """
    team_names, names, team_ids = get_details()

    name_dict = {}
    for i in range(len(names)):
        name_dict[team_names[i]] = team_ids[i]

    get_gw_scores(team_ids, team_names, csv_name = 'gw_scores.csv')
    print('Scraping gameweek scores completed, csv created')
    print()

if __name__ == "__main__":
    main()


