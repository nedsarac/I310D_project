import pandas as pd
import re

# Team name mapping for SOR matching
TEAM_NAME_MAPPING = {
    "ARMY": "Army Black Knights",
    "TULN": "Tulane Green Wave",
    "NAVY": "Navy Midshipmen",
    "MEM": "Memphis Tigers",
    "ECU": "East Carolina Pirates",
    "USF": "South Florida Bulls",
    "UTSA": "UTSA Roadrunners",
    "CLT": "Charlotte 49ers",
    "UAB": "UAB Blazers",
    "UNT": "North Texas Mean Green",
    "RICE": "Rice Owls",
    "TEM": "Temple Owls",
    "TLSA": "Tulsa Golden Hurricane",
    "FAU": "Florida Atlantic Owls",
    "SMU": "SMU Mustangs",
    "CLEM": "Clemson Tigers",
    "MIA": "Miami Hurricanes",
    "LOU": "Louisville Cardinals",
    "GT": "Georgia Tech Yellow Jackets",
    "SYR": "Syracuse Orange",
    "DUKE": "Duke Blue Devils",
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
    "USA": "South Alabama Jaguars",
    "TXST": "Texas State Bobcats",
    "ULM": "UL Monroe Warhawks",
    "TROY": "Troy Trojans",
    "USM": "Southern Miss Golden Eagles",
}

def load_data(file_name):
    """Load raw data from a CSV file."""
    return pd.read_csv(file_name)

def clean_wl_column(column):
    """Clean the W-L column to ensure it has the correct format."""
    column = column.fillna('0-0')  # Fill NaN with '0-0'
    column = column.replace(r'^\s*$', '0-0', regex=True)  # Replace empty strings with '0-0'
    column = column.apply(lambda x: x if re.match(r'^\d+-\d+$', x) else '0-0')  # Ensure format is 'number-number'
    return column

def transform_data(df, sor_file):
    """Clean and transform the raw data."""
    # Load SOR data
    sor_df = pd.read_csv(sor_file)

    # Match team names and add SOR
    df['Matched Team Name'] = df['Team Name'].map(TEAM_NAME_MAPPING)
    df = pd.merge(df, sor_df[['Team Name', 'SOR']], left_on='Matched Team Name', right_on='Team Name', how='left')
    df.drop(columns=['Team Name_y'], inplace=True)
    df.rename(columns={'Team Name_x': 'Team Name'}, inplace=True)

    # Convert PF and PA columns to numeric types
    df['PF'] = pd.to_numeric(df['PF'], errors='coerce').fillna(0).astype(int)
    df['PA'] = pd.to_numeric(df['PA'], errors='coerce').fillna(0).astype(int)

    # Clean Wins-Losses columns
    df['Conf. W-L'] = clean_wl_column(df['Conf. W-L'])
    df['Overall W-L'] = clean_wl_column(df['Overall W-L'])

    # Split Wins-Losses columns
    conf_split = df['Conf. W-L'].str.split('-', expand=True).astype(int)
    overall_split = df['Overall W-L'].str.split('-', expand=True).astype(int)

    # Assign split columns back to the DataFrame
    df['Conf Wins'], df['Conf Losses'] = conf_split[0], conf_split[1]
    df['Overall Wins'], df['Overall Losses'] = overall_split[0], overall_split[1]

    # Drop original W-L columns
    df.drop(columns=['Conf. W-L', 'Overall W-L'], inplace=True)

    # Create derived metrics
    df['Point Differential'] = df['PF'] - df['PA']
    df['Win Percentage'] = df['Overall Wins'] / (df['Overall Wins'] + df['Overall Losses'])

    return df

def save_data(df, file_name):
    """Save cleaned data to a CSV file."""
    df.to_csv(file_name, index=False)
    print(f"Cleaned data saved to {file_name}")

def main():
    raw_file = '/Users/bosnianboi/Documents/GitHub/I310D_project/raw_cfb_data.csv'
    sor_file = '/Users/bosnianboi/Documents/GitHub/I310D_project/SOR.csv'
    cleaned_file = '/Users/bosnianboi/Documents/GitHub/I310D_project/cleaned_cfb_data.csv'

    raw_df = load_data(raw_file)
    cleaned_df = transform_data(raw_df, sor_file)
    save_data(cleaned_df, cleaned_file)

if __name__ == "__main__":
    main()







