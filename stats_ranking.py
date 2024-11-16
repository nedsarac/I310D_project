import pandas as pd

def rank_conferences(df):
    """Calculate conference rankings and assign them to teams, excluding 'FBSind'."""
    # Exclude 'FBSind' from the calculation
    conference_df = df[df['Conference'] != 'FBSind']

    # Aggregate metrics by conference
    conference_strength = conference_df.groupby('Conference').agg({
        'Win Percentage': 'mean',
        'Point Differential': 'mean',
        'Conf Wins': 'sum'
    })

    # Add the number of teams in each conference
    conference_strength['Team Count'] = conference_df.groupby('Conference').size()

    # Normalize 'Conf Wins' by 'Team Count' to get average wins per team
    conference_strength['Avg Conf Wins'] = conference_strength['Conf Wins'] / conference_strength['Team Count']

    # Calculate the Conference Score
    conference_strength['Conference Score'] = (
        conference_strength['Win Percentage'] * 0.5 + 
        conference_strength['Point Differential'] * 0.3 +
        conference_strength['Avg Conf Wins'] * 0.2
    )

    # Sort conferences by their score
    conference_strength = conference_strength.sort_values(by='Conference Score', ascending=False)

    # Print the conference rankings for verification
    print("Conference Rankings (excluding FBSind):")
    print(conference_strength[['Conference Score', 'Team Count']])

    # Map Conference Score to teams in the main DataFrame, excluding FBSind
    conference_score_dict = conference_strength['Conference Score'].to_dict()
    df['Conference Score'] = df['Conference'].map(conference_score_dict)

    # Rank conferences and map the rank to teams
    conference_rankings = conference_strength['Conference Score'].rank(ascending=False).to_dict()
    df['Conference Rank'] = df['Conference'].map(conference_rankings)

    # Manually set 'Conference Rank' for FBSind teams to the lowest rank
    max_rank = df['Conference Rank'].max()  # Find the maximum rank among real conferences
    df.loc[df['Conference'] == 'FBSind', 'Conference Rank'] = max_rank + 1

    return df, conference_strength

def save_conference_ranking(conference_strength, output_file="conference_ranking.csv"):
    """
    Saves the conference rankings to a separate file for easy reference.
    """
    # Reset index and prepare data
    conference_ranking = conference_strength.reset_index()[['Conference', 'Conference Score']]
    conference_ranking['Conference Rank'] = conference_ranking['Conference Score'].rank(ascending=False).astype(int)

    # Save to CSV
    conference_ranking.to_csv(output_file, index=False)
    print(f"Conference rankings saved to {output_file}!")

def main():
    # Load cleaned data
    cleaned_file = '/Users/bosnianboi/Documents/GitHub/I310D_project/cleaned_cfb_data.csv'
    df = pd.read_csv(cleaned_file)

    # Rank conferences and save updated data
    df, conference_strength = rank_conferences(df)
    stats_file = '/Users/bosnianboi/Documents/GitHub/I310D_project/stats.csv'
    df.to_csv(stats_file, index=False)
    print(f"Team rankings with conference strength saved to {stats_file}")

    # Save separate conference ranking
    conf_ranking_file = '/Users/bosnianboi/Documents/GitHub/I310D_project/conference_ranking.csv'
    save_conference_ranking(conference_strength, conf_ranking_file)

if __name__ == "__main__":
    main()



