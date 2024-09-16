import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import tabula
from modules.court_code import high_court
from modules.trainedModel import threshold, model, v

def get_judges(input):
    for key in high_court:
        if key in input:
             input = key
             break
    url = 'https://doj.gov.in/list-of-high-court-judges/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    list = soup.find('div', class_='gen-list')

    list_items = list.find_all('li')

    pdf_links = []
    for item in list_items:
        a_tag = item.find('a')
        if a_tag:
            list_text = a_tag.find('div', class_='list-text').get_text(strip=True)
            if input.upper() in list_text:
                href_value = a_tag.get('href')
                pdf_links.append(href_value)

    for link in pdf_links:
        return link
    
#user_input = "delhi"
#user_input = input("Enter court name: ")
def judge(query):
    pdf_link = get_judges(query)

    dfs = tabula.read_pdf(pdf_link, pages='1')
    df=dfs[0]

    df = pd.DataFrame(df)
    data = df.to_dict(orient='records')
    json_data = json.dumps(data)
    return json_data
    # df_cleaned = df.dropna(how='all')
    # specific_columns = [0, 1, 3, 4, 5] 
    # if max(specific_columns) < len(df_cleaned.columns):
    #         return (df_cleaned.iloc[:, specific_columns])
    # else:
    #         return ("Some column indices are out of range.")
