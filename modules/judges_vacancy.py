import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import tabula

def get_vacancy():
    url = 'https://doj.gov.in/vacancy-position/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    pdf_link = soup.find('div', rel='col-xs-12')

    vacancy_link = pdf_link.find('a', href=True, string=lambda text: text and 'VACANCY POSITIONS AS ON 01.09.2024 (PDF 66KB)' in text)

    # if vacancy_link:
    #     pdf_url = vacancy_link['href']
    #     return pdf_url
    # else:
    #     return "not found"
    return "https://cdnbbsr.s3waas.gov.in/s35d6646aad9bcc0be55b2c82f69750387/uploads/2024/09/202409021484465022.pdf"


#user_input = "delhi"
#user_input = input("Enter court name: ")
def judge():
    pdf_link = get_vacancy()

    dfs = tabula.read_pdf(pdf_link, pages='1')
    df=dfs[0]

    df = pd.DataFrame(df)
    data = df.to_dict(orient='records')
    json_data = json.dumps(data)
    return json_data