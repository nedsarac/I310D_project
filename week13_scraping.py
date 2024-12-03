import re
import csv

# Path to the HTML source file
html_file_path = '/Users/bosnianboi/Documents/GitHub/I310D_project/complete post week-13 W-L.html'

# Read the HTML file
with open(html_file_path, 'r', encoding='utf-8') as file:
    source_code = file.read()

# Regex to extract team name and overall W-L record
team_stats_pattern = re.compile(
    r'"team":{.*?"displayName":"(?P<school>.*?)".*?'
    r'"stats":\[.*?"name":"numwins","value":"(?P<record>.*?)".*?\]',
    re.DOTALL
)

# Extract team data
team_data = []
for match in team_stats_pattern.finditer(source_code):
    school = match.group("school")
    record = match.group("record")
    team_data.append({"School": school, "Overall W-L": record})

# Save to CSV
output_csv = '/Users/bosnianboi/Documents/GitHub/I310D_project/post_week13_wl_only.csv'
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["School", "Overall W-L"])
    writer.writeheader()
    writer.writerows(team_data)

print(f"Data saved to {output_csv}!")





