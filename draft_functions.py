from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from selenium import webdriver
import time
import re

driver = webdriver.Chrome()

def get_details(driver = driver):
    """
    Scrapes the team names, team ids and names of team owners
    """


    driver.get('https://draft.premierleague.com/')
    input('Complete CAPTCHA and log in then hit enter when done')
    league = driver.find_element("xpath", "/html/body/main/div/div[1]/div/div/div/nav/ul/li[5]/a")
    league.click()
    table = driver.find_element("xpath", "/html/body/main/div/div[2]/div/div[1]/div/table")
    soup = BeautifulSoup(table.get_attribute('outerHTML'), "html.parser")

    team_names = [tag.text for tag in soup.find_all('strong')]

    team_and_name = ([tag.text for tag in soup.find_all('a')])
    names = []
    for i in range(len(team_and_name)):
        names.append(team_and_name[i][len(team_names[i]):].strip())

    team_ids = []
    for a in soup.find_all('a', href=True):
        s = a['href']
        team_ids.append(re.search(r'entry/(.*?)/event/', s).group(1))

    team_name_dict = {}
    for i in range(len(team_ids)):
        team_name_dict[team_ids[i]] = names[i]
    
    return team_names, names, team_ids

def get_gw_scores(team_ids, team_names, csv_name = 'gw_scores.csv', driver = driver):
    """
    Takes a list of team_ids and returns a csv file containing the gameweek scores for each team.
    """
    gw_scores = []
    print(f'Getting scores for: {team_names}')
    for id in team_ids:
        s = 'https://draft.premierleague.com/entry/' +  str(id)+ '/history'
        try:
            driver.get(s)
            time.sleep(2)
            gw_table = driver.find_element("xpath", "/html/body/main/div/div[2]/div/div[1]/div")
            
        except:
            print(f'Error getting GW data for {id}, retrying in 15s')
            time.sleep(15)
            gw_table = driver.find_element("xpath", "/html/body/main/div/div[2]/div/div[1]/div")
        
        scores = list(pd.read_html(gw_table.get_attribute('outerHTML'))[0]['Points'])
        i = 0
        while scores[0] == 'No Gameweek history.' and i <3:
            
            print(f'Error getting GW data for {id}, retrying in 15s')
            time.sleep(15)
            gw_table = driver.find_element("xpath", "/html/body/main/div/div[2]/div/div[1]/div")
            scores = list(pd.read_html(gw_table.get_attribute('outerHTML'))[0]['Points'])
            i+=1
            
        gw_scores.append(scores)
    columns = ['gw_' + str(x+1) for x in range(len(scores))]
    gw_scores = pd.DataFrame(gw_scores, columns = columns)
    gw_scores['team_name'] = team_names
    gw_scores = gw_scores.set_index('team_name')

    gw_scores['Total'] = gw_scores.sum(axis=1)
    gw_scores
    gw_scores.to_csv(csv_name, encoding='utf-8-sig')
    return gw_scores

def get_detailed_breakdown(team_ids, team_names, driver = driver):
    """
    Takes a list of team_ids and returns a csv file containing the players in each team each week and the breakdown of their stats provided by fpl
    """

    driver.get('https://draft.premierleague.com/')
    time.sleep(2)
    completed_gws = int(driver.find_element("xpath", '/html/body/main/div/div[2]/div/div[1]/div[1]/h3').text.strip('Gameweek'))
    df = pd.DataFrame(columns = ['gw', 'name', 'POS', 'MP', 'GS', 'A', 'CS', 'GC', 'OG', 'PS', 'PM',
       'YC', 'RC', 'S', 'B', 'BPS', 'I', 'C', 'T', 'II', 'benched'])
    for i in range(len(team_ids)):
        team_id = team_ids[i]
        team_name = team_names[i] 
        temp_df = pd.DataFrame(columns = ['gw', 'name', 'POS', 'MP', 'GS', 'A', 'CS', 'GC', 'OG', 'PS', 'PM',
       'YC', 'RC', 'S', 'B', 'BPS', 'I', 'C', 'T', 'II', 'benched'])
        for gw in range(1,completed_gws+1):
            s = 'https://draft.premierleague.com/entry/' +  str(team_id) + '/event/' + str(gw)
            driver.get(s)
            time.sleep(2)
            try:
                list_view = driver.find_element("xpath", '/html/body/main/div/div[2]/div/div[1]/div/div[3]/div[1]/ul/li[2]/a')
            except:
                print(f'Error clicking list view for {team_id}, GW {gw}, trying again in 15s')
                time.sleep(15)
                list_view = driver.find_element("xpath", '/html/body/main/div/div[2]/div/div[1]/div/div[3]/div[1]/ul/li[2]/a')
            list_view.click()
            time.sleep(1)
            try:
                player_table = driver.find_element("xpath", "/html/body/main/div/div[2]/div/div[1]/div/div[3]/div[2]/div/div/div[2]/div/table")
            except:
                print(f'Error getting {team_id}, GW {gw}, trying again in 15s')
                time.sleep(15)
                player_table = driver.find_element("xpath", "/html/body/main/div/div[2]/div/div[1]/div/div[3]/div[2]/div/div/div[2]/div/table")
                
            gw_11 = list(pd.read_html(player_table.get_attribute('outerHTML')))[0]
            bench_table = driver.find_element("xpath", "/html/body/main/div/div[2]/div/div[1]/div/div[3]/div[2]/div/div/div[4]/div/table")
            gw_bench = list(pd.read_html(bench_table.get_attribute('outerHTML')))[0]

            gw_squad = pd.concat([gw_11,gw_bench])
            gw_squad['Unnamed: 1'] = gw_squad['Unnamed: 1'].apply(lambda x: str(x)[:-6])
            gw_squad.rename({'Unnamed: 1' : 'name'}, axis = 1, inplace = True)
            gw_squad.drop('Unnamed: 0', axis = 1, inplace = True)
            gw_squad['gw'] = gw 
            gw_squad.insert(0, 'gw', gw_squad.pop('gw'))
            gw_squad['new_index'] = ['player_' + str(i) for i in range(1,16)]
            gw_squad = gw_squad.set_index('new_index')
            gw_squad['benched'] = [0] * 11 + [1] * 4
            temp_df = pd.concat([temp_df,gw_squad])
    
        temp_df['draft_team'] = team_name
        df = pd.concat([df,temp_df])
    df.insert(0, 'draft_team', df.pop('draft_team'))
    s = 'gw_' + str(completed_gws) + '_player_breakdown.csv'
    df.to_csv(s ,encoding='utf-8-sig')
    return df