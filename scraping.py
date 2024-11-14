from bs4 import BeautifulSoup

html_file_path = '/Users/bosnianboi/Documents/GitHub/I310D_project/College Football Standings, 2024 season - ESPN.html'

with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

team_names = [element.get_text(strip=True) for element in soup.find_all("span", class_="show-mobile")]

teams_data = []

for table in soup.find_all("table"):  
    for row in table.find_all("tr")[1:]:  
        columns = row.find_all("td")
        if columns and len(columns) >= 9:  
            wl_conf = columns[0].get_text(strip=True)  
            wl_overall = columns[3].get_text(strip=True)  
            pf = columns[4].get_text(strip=True)  
            pa = columns[5].get_text(strip=True)  
            ap = columns[9].get_text(strip=True) 
            
            team_data = {
                "Conf. W-L": wl_conf,
                "Overall W-L": wl_overall,
                "PF": pf,
                "PA": pa,
                "AP": ap
            }
            teams_data.append(team_data)

for i, team_name in enumerate(team_names):
    if i < len(teams_data):  
        team_data = teams_data[i]
        print(f"Team Name: {team_name}")
        print(f"Conf. W-L: {team_data['Conf. W-L']}")
        print(f"Overall W-L: {team_data['Overall W-L']}")
        print(f"PF: {team_data['PF']}")
        print(f"PA: {team_data['PA']}")
        print(f"AP: {team_data['AP']}\n")