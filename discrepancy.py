import pandas as pd

# File paths
raw_cfb_data_path = '/Users/bosnianboi/Documents/GitHub/I310D_project/raw_cfb_data.csv'
post_week13_wl_only_path = '/Users/bosnianboi/Documents/GitHub/I310D_project/post_week13_wl_only.csv'
output_path = '/Users/bosnianboi/Documents/GitHub/I310D_project/discrepancies.csv'

# Read in data
raw_data = pd.read_csv(raw_cfb_data_path)
post_week13_data = pd.read_csv(post_week13_wl_only_path)

# Abbreviation to full team name mapping
name_mapping = {
    "ARMY": "Army Black Knights",
    "TULN": "Tulane Green Wave",
    "NAVY": "Navy Midshipmen",
    "MEM": "Memphis Tigers",
    "ECU": "East Carolina Pirates",
    "USF": "South Florida Bulls",
    "UTSA": "UTSA Roadrunners",
    "CLT": "Charlotte 49ers",
    "UNT": "North Texas Mean Green",
    "UAB": "UAB Blazers",
    "RICE": "Rice Owls",
    "TEM": "Temple Owls",
    "TLSA": "Tulsa Golden Hurricane",
    "FAU": "Florida Atlantic Owls",
    "SMU": "SMU Mustangs",
    "CLEM": "Clemson Tigers",
    "MIA": "Miami Hurricanes",
    "LOU": "Louisville Cardinals",
    "GT": "Georgia Tech Yellow Jackets",
    "DUKE": "Duke Blue Devils",
    "SYR": "Syracuse Orange",
    "UVA": "Virginia Cavaliers",
    "VT": "Virginia Tech Hokies",
    "PITT": "Pittsburgh Panthers",
    "BC": "Boston College Eagles",
    "UNC": "North Carolina Tar Heels",
    "NCSU": "NC State Wolfpack",
    "CAL": "California Golden Bears",
    "WAKE": "Wake Forest Demon Deacons",
    "STAN": "Stanford Cardinal",
    "FSU": "Florida State Seminoles",
    "COLO": "Colorado Buffaloes",
    "ASU": "Arizona State Sun Devils",
    "BYU": "BYU Cougars",
    "ISU": "Iowa State Cyclones",
    "BAY": "Baylor Bears",
    "TTU": "Texas Tech Red Raiders",
    "KSU": "Kansas State Wildcats",
    "TCU": "TCU Horned Frogs",
    "WVU": "West Virginia Mountaineers",
    "KU": "Kansas Jayhawks",
    "CIN": "Cincinnati Bearcats",
    "HOU": "Houston Cougars",
    "ARIZ": "Arizona Wildcats",
    "UTAH": "Utah Utes",
    "UCF": "UCF Knights",
    "OKST": "Oklahoma State Cowboys",
    "ORE": "Oregon Ducks",
    "IU": "Indiana Hoosiers",
    "PSU": "Penn State Nittany Lions",
    "OSU": "Ohio State Buckeyes",
    "ILL": "Illinois Fighting Illini",
    "IOWA": "Iowa Hawkeyes",
    "MICH": "Michigan Wolverines",
    "MINN": "Minnesota Golden Gophers",
    "WASH": "Washington Huskies",
    "USC": "USC Trojans",
    "RUTG": "Rutgers Scarlet Knights",
    "MSU": "Michigan State Spartans",
    "UCLA": "UCLA Bruins",
    "NEB": "Nebraska Cornhuskers",
    "WIS": "Wisconsin Badgers",
    "NU": "Northwestern Wildcats",
    "MD": "Maryland Terrapins",
    "PUR": "Purdue Boilermakers",
    "JVST": "Jacksonville State Gamecocks",
    "SHSU": "Sam Houston Bearkats",
    "WKU": "Western Kentucky Hilltoppers",
    "LIB": "Liberty Flames",
    "LT": "Louisiana Tech Bulldogs",
    "MTSU": "Middle Tennessee Blue Raiders",
    "UTEP": "UTEP Miners",
    "KENN": "Kennesaw State Owls",
    "FIU": "Florida International Panthers",
    "NMSU": "New Mexico State Aggies",
    "ND": "Notre Dame Fighting Irish",
    "CONN": "UConn Huskies",
    "MASS": "Massachusetts Minutemen",
    "M-OH": "Miami (OH) RedHawks",
    "OHIO": "Ohio Bobcats",
    "BUFF": "Buffalo Bulls",
    "BGSU": "Bowling Green Falcons",
    "WMU": "Western Michigan Broncos",
    "TOL": "Toledo Rockets",
    "NIU": "Northern Illinois Huskies",
    "AKR": "Akron Zips",
    "EMU": "Eastern Michigan Eagles",
    "CMU": "Central Michigan Chippewas",
    "BALL": "Ball State Cardinals",
    "KENT": "Kent State Golden Flashes",
    "BOIS": "Boise State Broncos",
    "CSU": "Colorado State Rams",
    "UNLV": "UNLV Rebels",
    "FRES": "Fresno State Bulldogs",
    "UNM": "New Mexico Lobos",
    "SJSU": "San José State Spartans",
    "USU": "Utah State Aggies",
    "SDSU": "San Diego State Aztecs",
    "AFA": "Air Force Falcons",
    "HAW": "Hawai'i Rainbow Warriors",
    "WYO": "Wyoming Cowboys",
    "NEV": "Nevada Wolf Pack",
    "ORST": "Oregon State Beavers",
    "WSU": "Washington State Cougars",
    "TEX": "Texas Longhorns",
    "UGA": "Georgia Bulldogs",
    "TENN": "Tennessee Volunteers",
    "TA&M": "Texas A&M Aggies",
    "MISS": "Ole Miss Rebels",
    "SC": "South Carolina Gamecocks",
    "ALA": "Alabama Crimson Tide",
    "MIZ": "Missouri Tigers",
    "LSU": "LSU Tigers",
    "FLA": "Florida Gators",
    "ARK": "Arkansas Razorbacks",
    "VAN": "Vanderbilt Commodores",
    "OU": "Oklahoma Sooners",
    "AUB": "Auburn Tigers",
    "UK": "Kentucky Wildcats",
    "MSST": "Mississippi State Bulldogs",
    "MRSH": "Marshall Thundering Herd",
    "GASO": "Georgia Southern Eagles",
    "JMU": "James Madison Dukes",
    "APP": "App State Mountaineers",
    "ODU": "Old Dominion Monarchs",
    "CCU": "Coastal Carolina Chanticleers",
    "GAST": "Georgia State Panthers",
    "UL": "Louisiana Ragin' Cajuns",
    "ARST": "Arkansas State Red Wolves",
    "TXST": "Texas State Bobcats",
    "USA": "South Alabama Jaguars",
    "ULM": "UL Monroe Warhawks",
    "TROY": "Troy Trojans",
    "USM": "Southern Miss Golden Eagles"
}

# Standardize team names in raw_data
raw_data["Team Name"] = raw_data["Team Name"].replace(name_mapping)

# Merge datasets on school name
merged_data = pd.merge(
    post_week13_data.rename(columns={"School": "Team Name", "Overall W-L": "Overall W-L_post_week13"}),
    raw_data.rename(columns={"Overall W-L": "Overall W-L_raw"}),
    on="Team Name",
    how="outer"
)

# Identify discrepancies
merged_data["Discrepancy"] = merged_data["Overall W-L_post_week13"] != merged_data["Overall W-L_raw"]

# Filter discrepancies
discrepancies = merged_data[merged_data["Discrepancy"]]

# Save discrepancies to a CSV file
discrepancies.to_csv(output_path, index=False)

print(f"Discrepancies saved to {output_path}!")

