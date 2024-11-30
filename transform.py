import pandas as pd
import re

# Team name mapping for SOR matching
TEAM_NAME_MAPPING = {
    "Army": "Army Black Knights",
    "Tulane": "Tulane Green Wave",
    "Navy": "Navy Midshipmen",
    "Memphis": "Memphis Tigers",
    "East Carolina": "East Carolina Pirates",
    "South Florida": "South Florida Bulls",
    "UTSA": "UTSA Roadrunners",
    "Charlotte": "Charlotte 49ers",
    "UAB": "UAB Blazers",
    "North Texas": "North Texas Mean Green",
    "Rice": "Rice Owls",
    "Temple": "Temple Owls",
    "Tulsa": "Tulsa Golden Hurricane",
    "Florida Atlantic": "Florida Atlantic Owls",
    "SMU": "SMU Mustangs",
    "Clemson": "Clemson Tigers",
    "Miami": "Miami Hurricanes",
    "Louisville": "Louisville Cardinals",
    "Georgia Tech": "Georgia Tech Yellow Jackets",
    "Syracuse": "Syracuse Orange",
    "Duke": "Duke Blue Devils",
    "Virginia Tech": "Virginia Tech Hokies",
    "Virginia": "Virginia Cavaliers",
    "Pittsburgh": "Pittsburgh Panthers",
    "Boston College": "Boston College Eagles",
    "North Carolina": "North Carolina Tar Heels",
    "California": "California Golden Bears",
    "NC State": "NC State Wolfpack",
    "Wake Forest": "Wake Forest Demon Deacons",
    "Stanford": "Stanford Cardinal",
    "Florida State": "Florida State Seminoles",
    "Arizona State": "Arizona State Sun Devils",
    "BYU": "BYU Cougars",
    "Iowa State": "Iowa State Cyclones",
    "Colorado": "Colorado Buffaloes",
    "Baylor": "Baylor Bears",
    "TCU": "TCU Horned Frogs",
    "Texas Tech": "Texas Tech Red Raiders",
    "West Virginia": "West Virginia Mountaineers",
    "Kansas State": "Kansas State Wildcats",
    "Kansas": "Kansas Jayhawks",
    "Cincinnati": "Cincinnati Bearcats",
    "Houston": "Houston Cougars",
    "UCF": "UCF Knights",
    "Arizona": "Arizona Wildcats",
    "Utah": "Utah Utes",
    "Oklahoma State": "Oklahoma State Cowboys",
    "Oregon": "Oregon Ducks",
    "Ohio State": "Ohio State Buckeyes",
    "Indiana": "Indiana Hoosiers",
    "Penn State": "Penn State Nittany Lions",
    "Illinois": "Illinois Fighting Illini",
    "Iowa": "Iowa Hawkeyes",
    "Washington": "Washington Huskies",
    "Michigan": "Michigan Wolverines",
    "Minnesota": "Minnesota Golden Gophers",
    "USC": "USC Trojans",
    "UCLA": "UCLA Bruins",
    "Nebraska": "Nebraska Cornhuskers",
    "Wisconsin": "Wisconsin Badgers",
    "Rutgers": "Rutgers Scarlet Knights",
    "Michigan State": "Michigan State Spartans",
    "Northwestern": "Northwestern Wildcats",
    "Maryland": "Maryland Terrapins",
    "Purdue": "Purdue Boilermakers",
    "Jacksonville State": "Jacksonville State Gamecocks",
    "Liberty": "Liberty Flames",
    "Western Kentucky": "Western Kentucky Hilltoppers",
    "Sam Houston": "Sam Houston Bearkats",
    "Louisiana Tech": "Louisiana Tech Bulldogs",
    "Middle Tennessee": "Middle Tennessee Blue Raiders",
    "UTEP": "UTEP Miners",
    "Kennesaw State": "Kennesaw State Owls",
    "Florida International": "Florida International Panthers",
    "New Mexico State": "New Mexico State Aggies",
    "Notre Dame": "Notre Dame Fighting Irish",
    "UConn": "UConn Huskies",
    "Massachusetts": "Massachusetts Minutemen",
    "Miami (OH)": "Miami (OH) RedHawks",
    "Ohio": "Ohio Bobcats",
    "Bowling Green": "Bowling Green Falcons",
    "Buffalo": "Buffalo Bulls",
    "Toledo": "Toledo Rockets",
    "Western Michigan": "Western Michigan Broncos",
    "Northern Illinois": "Northern Illinois Huskies",
    "Akron": "Akron Zips",
    "Eastern Michigan": "Eastern Michigan Eagles",
    "Central Michigan": "Central Michigan Chippewas",
    "Ball State": "Ball State Cardinals",
    "Kent State": "Kent State Golden Flashes",
    "Boise State": "Boise State Broncos",
    "Colorado State": "Colorado State Rams",
    "UNLV": "UNLV Rebels",
    "Fresno State": "Fresno State Bulldogs",
    "New Mexico": "New Mexico Lobos",
    "Utah State": "Utah State Aggies",
    "San José State": "San José State Spartans",
    "San Diego State": "San Diego State Aztecs",
    "Hawai'i": "Hawai'i Rainbow Warriors",
    "Wyoming": "Wyoming Cowboys",
    "Air Force": "Air Force Falcons",
    "Nevada": "Nevada Wolf Pack",
    "Oregon State": "Oregon State Beavers",
    "Washington State": "Washington State Cougars",
    "Texas": "Texas Longhorns",
    "Texas A&M": "Texas A&M Aggies",
    "Georgia": "Georgia Bulldogs",
    "Tennessee": "Tennessee Volunteers",
    "South Carolina": "South Carolina Gamecocks",
    "Alabama": "Alabama Crimson Tide",
    "LSU": "LSU Tigers",
    "Missouri": "Missouri Tigers",
    "Ole Miss": "Ole Miss Rebels",
    "Florida": "Florida Gators",
    "Arkansas": "Arkansas Razorbacks",
    "Vanderbilt": "Vanderbilt Commodores",
    "Oklahoma": "Oklahoma Sooners",
    "Auburn": "Auburn Tigers",
    "Kentucky": "Kentucky Wildcats",
    "Mississippi State": "Mississippi State Bulldogs",
    "Marshall": "Marshall Thundering Herd",
    "Georgia Southern": "Georgia Southern Eagles",
    "James Madison": "James Madison Dukes",
    "Old Dominion": "Old Dominion Monarchs",
    "App State": "App State Mountaineers",
    "Coastal Carolina": "Coastal Carolina Chanticleers",
    "Georgia State": "Georgia State Panthers",
    "Louisiana": "Louisiana Ragin' Cajuns",
    "Arkansas State": "Arkansas State Red Wolves",
    "South Alabama": "South Alabama Jaguars",
    "Texas State": "Texas State Bobcats",
    "UL Monroe": "UL Monroe Warhawks",
    "Troy": "Troy Trojans",
    "Southern Miss": "Southern Miss Golden Eagles",
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







