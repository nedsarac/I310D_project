from bs4 import BeautifulSoup
import pandas as pd

# Path to HTML file
html_file_path = '/Users/bosnianboi/Documents/GitHub/I310D_project/College Football Standings, 2024 season - ESPN.html'

# Read and parse HTML content
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Extract team names
team_names = [element.get_text(strip=True) for element in soup.find_all("span", class_="show-mobile")]

teams_data = []

for table in soup.find_all("table"):
    for row in table.find_all("tr")[1:]:  # Skip header row
        # Skip rows with "subgroup-headers Table__sub-header" class (like "East" and "West" labels)
        if "subgroup-headers" in row.get("class", []) and "Table__sub-header" in row.get("class", []):
            print("Skipping row with division label (East/West)")
            continue

        columns = row.find_all("td")
        # Process only valid team rows with enough columns
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
                "AP": ap,
            }
            teams_data.append(team_data)

# Conference ranges (indices for each conference)
conference_ranges = [
    (0, 13, "AAC"),
    (14, 30, "ACC"),
    (31, 46, "Big 12"),
    (47, 64, "Big 10"),
    (65, 74, "ConUSA"),
    (75, 77, "FBSind"),
    (78, 89, "MAC"),
    (90, 101, "MWC"),
    (102, 103, "PAC12"),
    (104, 119, "SEC"),
    (120, 133, "SBC"),
]

# Assign team names and conferences
for i, team_name in enumerate(team_names):
    if i < len(teams_data):  
        team_data = teams_data[i]
        team_data["Team Name"] = team_name
        
        # Assign conference based on index
        for start, end, conference in conference_ranges:
            if start <= i <= end:
                team_data["Conference"] = conference
                break  # Stop checking ranges once the conference is assigned

# Convert to DataFrame and save to CSV
df = pd.DataFrame(teams_data)
output_csv = '/Users/bosnianboi/Documents/GitHub/I310D_project/raw_cfb_data.csv'
df.to_csv(output_csv, index=False)

print(f"Data saved to {output_csv}")





