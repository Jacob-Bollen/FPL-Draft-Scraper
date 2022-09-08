from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from selenium import webdriver
import time
import re
from draft_functions import get_details,  get_detailed_breakdown

def main():
    """
    Returns a csv file containing the players in each draft team each week along with the stats provided by FPL, goals, assists, etc
    """
    team_names, names, team_ids = get_details()
    name_dict = {}
    for i in range(len(names)):
        name_dict[team_names[i]] = team_ids[i]

    print()
    get_detailed_breakdown(team_ids, team_names)
    
    print('Scraping gameweek scores completed, csv created')

if __name__ == "__main__":
    main()


