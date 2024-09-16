import requests
from bs4 import BeautifulSoup
from modules.court_code import state_court, high_court
from modules.trainedModel import threshold, model, v

def case_pendency_data_dist(court_type):
    for key in state_court:
        if key in court_type:
            state_code = state_court[key]
            url = f"https://njdg.ecourts.gov.in/njdg_v3/?p=home/index&state_code={state_code}&app_token=7ae1c7670840a36dbe9c2207ce99a7f4b125ff67ea8e553b01013d6d5435c43e"
            break
    else:
        url = "https://njdg.ecourts.gov.in/njdg_v3/"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="text-center table table-bordered table-hover")  # Update with actual class/id
        if table:
            rows = table.find_all("tr")
            data = []
            for row in rows:
                cols = row.find_all("td")
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
            return data
        else:
            return {"error": "Unable to find the data table on NJDG"}
    else:
        return {"error": "Failed to retrieve data from NJDG"}

def case_pendency_data_high(court_type):
    for key in high_court:
        if key in court_type:
            high_code = high_court[key]
            url = f"https://njdg.ecourts.gov.in/hcnjdg_v2/?p=home/index&state_code={high_code}&app_token=fe30e95603136f9e6d1601f445c07c4043b80a4d393a3cdd629c65111bd74324"
            break
    else:
        url = "https://njdg.ecourts.gov.in/hcnjdg_v2/"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="text-center table-bordered table-hover")  # Update with actual class/id
        if table:
            rows = table.find_all("tr")
            data = []
            for row in rows:
                cols = row.find_all("td")
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
            return data
        else:
            return {"error": "Unable to find the data table on NJDG"}
    else:
        return {"error": "Failed to retrieve data from NJDG"}

def case_pendency_data_supreme():

    url = "https://njdg.ecourts.gov.in/scnjdg/"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="table table-hover text-start m-0")  # Update with actual class/id
        if table:
            rows = table.find_all("tr")
            data = []
            for row in rows:
                row_data = []
                cols = row.find_all(["td", "th"])                
                for col in cols:
                    cell_value = col.get_text(strip=True)
                    row_data.append(cell_value)                
                if row_data:
                    data.append(row_data)            
            return data
        else:
            return {"error": "Unable to find the data table on NJDG"}
    else:
        return {"error": "Failed to retrieve data from NJDG"}


def case(court_type):
    if 'district' or 'state' in court_type:
        case_pendency_data = case_pendency_data_dist(court_type)
    elif 'high' in court_type:
        case_pendency_data = case_pendency_data_high(court_type)
    elif 'supreme' in court_type:
        case_pendency_data = case_pendency_data_supreme()
    else:
        case_pendency_data = {"error": "Invalid court type"}
    
    return case_pendency_data