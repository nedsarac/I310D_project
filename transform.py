import pandas as pd
import re

def load_data(file_name):
    """Load raw data from a CSV file."""
    return pd.read_csv(file_name)

def clean_wl_column(column):
    """Clean the W-L column to ensure it has the correct format."""
    # Replace non-standard values with '0-0'
    column = column.fillna('0-0')  # Fill NaN with '0-0'
    column = column.replace(r'^\s*$', '0-0', regex=True)  # Replace empty strings with '0-0'
    column = column.apply(lambda x: x if re.match(r'^\d+-\d+$', x) else '0-0')  # Ensure format is 'number-number'
    return column

def transform_data(df):
    """Clean and transform the raw data."""
    # Convert PF and PA columns to numeric types
    df['PF'] = pd.to_numeric(df['PF'], errors='coerce').fillna(0).astype(int)
    df['PA'] = pd.to_numeric(df['PA'], errors='coerce').fillna(0).astype(int)
    
    # Clean Wins-Losses columns to ensure proper format
    df['Conf. W-L'] = clean_wl_column(df['Conf. W-L'])
    df['Overall W-L'] = clean_wl_column(df['Overall W-L'])
    df['AP'] = clean_wl_column(df['AP'])
    
    # Split Wins-Losses columns with explicit handling of empty or non-numeric values
    conf_split = df['Conf. W-L'].str.split('-', expand=True).astype(int)
    overall_split = df['Overall W-L'].str.split('-', expand=True).astype(int)
    ap_split = df['AP'].str.split('-', expand=True).astype(int)
    
    # Assign split columns back to the DataFrame with appropriate names
    df['Conf Wins'] = conf_split[0]
    df['Conf Losses'] = conf_split[1]
    df['Overall Wins'] = overall_split[0]
    df['Overall Losses'] = overall_split[1]
    df['AP Wins'] = ap_split[0]
    df['AP Losses'] = ap_split[1]
    
    # Drop original columns
    df.drop(columns=['Conf. W-L', 'Overall W-L', 'AP'], inplace=True)
    
    # Create derived metrics
    df['Point Differential'] = df['PF'] - df['PA']
    df['Win Percentage'] = df['Overall Wins'] / (df['Overall Wins'] + df['Overall Losses'])
    
    return df

def save_data(df, file_name):
    """Save cleaned data to a CSV file."""
    df.to_csv(file_name, index=False)
    print(f"Cleaned data saved to {file_name}")

def main():
    # File names
    raw_file = '/Users/bosnianboi/Documents/GitHub/I310D_project/raw_cfb_data.csv'
    cleaned_file = '/Users/bosnianboi/Documents/GitHub/I310D_project/cleaned_cfb_data.csv'
    
    # Load, transform, and save data
    df = load_data(raw_file)
    df = transform_data(df)
    save_data(df, cleaned_file)

if __name__ == "__main__":
    main()






