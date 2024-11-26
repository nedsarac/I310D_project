from bs4 import BeautifulSoup
import pandas as pd

# Path to HTML file
html_file_path = '/Users/bosnianboi/Documents/GitHub/I310D_project/2024 Resume College Football Power Index - ESPN.html'

# Read and parse HTML content
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Find all rows in the table
table_rows = soup.find_all("tr", class_="Table__TR")

# Initialize a list to store extracted data
team_data = []

# Loop through each row
for row in table_rows:
    # Extract team name
    team_span = row.find("span", class_="TeamLink__Name")
    if team_span:  # Ensure the team name exists in this row
        team_name = team_span.a.get_text(strip=True)
    else:
        continue  # Skip rows without team names

    # Extract conference
    # Locate the second <td> element that contains the conference
    tds = row.find_all("td")  # Get all <td> elements in the row
    if len(tds) > 1:  # Ensure there are enough <td> elements
        conference_td = tds[1].find("div")  # Access the second <td> and its <div>
        if conference_td:
            conference = conference_td.get_text(strip=True)
        else:
            conference = None
    else:
        conference = None

    # Extract SOR from the `data-idx` attribute
    sor_idx = row.get("data-idx")
    sor = int(sor_idx)+1

    # Add to the list
    team_data.append({"Team Name": team_name, "Conference": conference, "SOR": sor})

# Convert team_data into a DataFrame
df = pd.DataFrame(team_data)

# Save the DataFrame to a CSV file
output_csv = 'SOR.csv'
df.to_csv(output_csv, index=False)

print(f"Data saved to {output_csv}!")










