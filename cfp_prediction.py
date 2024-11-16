import pandas as pd

def calculate_team_scores(df):
    """Calculate a score for each team based on performance metrics."""
    
    # Normalize point differential
    max_point_diff = df['Point Differential'].max()
    df['Normalized Point Diff'] = df['Point Differential'] / max_point_diff

    # Calculate Team Score using weighted metrics
    df['Team Score'] = (
        (df['Conf Wins'] / (df['Conf Wins'] + df['Conf Losses'])) * 0.15 +
        (df['Overall Wins'] / (df['Overall Wins'] + df['Overall Losses'])) * 0.25 +
        (df['AP Wins'] / (df['AP Wins'] + df['AP Losses'] + 1)) * 0.20 +  # Add 1 to avoid division by zero
        df['Normalized Point Diff'] * 0.20 +
        df['Win Percentage'] * 0.20
    )

    # Sort teams by Team Score
    df = df.sort_values(by='Team Score', ascending=False).reset_index(drop=True)
    return df

def cfp_predictor(df):
    """Predict the 12-team playoff based on conference rankings and team scores."""

    # Track selected teams to avoid duplicates
    selected_teams = set()

    # Final playoff bracket as a list of dictionaries
    playoff_teams = []

    # Step 1: Select top 4 teams from the top 4 conferences
    top_4_conferences = df[df['Conference Rank'] <= 4]
    for conf in sorted(top_4_conferences['Conference Rank'].unique()):
        team = (top_4_conferences[top_4_conferences['Conference Rank'] == conf]
                .sort_values(by='Team Score', ascending=False)
                .iloc[0])
        playoff_teams.append(team.to_dict())  # Ensure it's a dictionary
        selected_teams.add(team['Team Name'])

    # Step 2: Best team from conferences ranked 5-9
    mid_conferences = df[(df['Conference Rank'] >= 5) & (df['Conference Rank'] <= 9)]
    best_mid_team = (mid_conferences.sort_values(by='Team Score', ascending=False)
                     .iloc[0])
    playoff_teams.append(best_mid_team.to_dict())  # Ensure it's a dictionary
    selected_teams.add(best_mid_team['Team Name'])

    # Step 3: Second-best teams from the top 3 conferences
    for conf in sorted(top_4_conferences['Conference Rank'].unique()[:3]):
        second_team = (top_4_conferences[(top_4_conferences['Conference Rank'] == conf) &
                                         (~top_4_conferences['Team Name'].isin(selected_teams))]
                       .sort_values(by='Team Score', ascending=False)
                       .iloc[0])
        playoff_teams.append(second_team.to_dict())  # Ensure it's a dictionary
        selected_teams.add(second_team['Team Name'])

    # Step 4: Fill remaining spots with next best teams
    remaining_teams = df[~df['Team Name'].isin(selected_teams)]
    next_best_teams = remaining_teams.sort_values(by='Team Score', ascending=False).head(4)
    playoff_teams.extend(next_best_teams.to_dict(orient='records'))  # Add as list of dictionaries

    # Convert list of playoff teams to a DataFrame and assign seeds
    playoff_df = pd.DataFrame(playoff_teams).reset_index(drop=True)
    playoff_df['Seed'] = range(1, len(playoff_df) + 1)

    # Final output
    return playoff_df[['Seed', 'Team Name', 'Conference', 'Team Score', 'Conference Rank']]

def main():
    # Load the ranked data
    ranked_file = '/Users/bosnianboi/Documents/GitHub/I310D_project/ranked_conf.csv'
    df = pd.read_csv(ranked_file)

    # Calculate team scores
    df = calculate_team_scores(df)

    # Generate CFP predictor output
    playoff_teams = cfp_predictor(df)
    output_file = '/Users/bosnianboi/Documents/GitHub/I310D_project/cfp_playoff_predictions.csv'
    playoff_teams.to_csv(output_file, index=False)
    print(f"Playoff predictions saved to {output_file}")

if __name__ == "__main__":
    main()






