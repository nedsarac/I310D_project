import pandas as pd

def calculate_team_scores(input_file, output_file="team_score.csv"):
    """Calculate Team Scores based on provided weights and penalties, including SOR."""
    # Load team data
    df = pd.read_csv(input_file)

    # Load conference multipliers
    conf_ranking = pd.read_csv("conference_ranking.csv")
    conf_ranking['Multiplier'] = 2.0 - (conf_ranking['Conference Rank'] / conf_ranking['Conference Rank'].max())
    conference_multiplier = conf_ranking.set_index('Conference')['Multiplier'].to_dict()

    # Map multipliers to team data
    df['Conference Multiplier'] = df['Conference'].map(conference_multiplier)

    # Assign default multiplier for FBSind teams
    df['Conference Multiplier'].fillna(1.0, inplace=True)

    # Handle missing values for independent teams
    df['Conf Wins'] = df['Conf Wins'].fillna(0)
    df['Conf Losses'] = df['Conf Losses'].fillna(0)

    # Calculate Point Differential
    df['Point Differential'] = df['PF'] - df['PA']

    # Incorporate SOR (lower SOR is better, so invert and scale it for scoring)
    df['SOR Score'] = (1 / df['SOR']) * 10

    # Calculate Team Score
    df['Team Score'] = (
        df['AP Wins'] * 8 +
        (df['Conf Wins'] * df['Conference Multiplier'] * 5) +
        ((df['Overall Wins'] - df['Conf Wins']) * 5) +
        df['Point Differential'] * 0.1 +
        df['SOR Score'] * 6  # Incorporate SOR with a significant weight
    )

    # Apply penalties
    df['Unranked Losses'] = df['Overall Losses'] - df['AP Losses']
    df['Team Score'] -= df['AP Losses'] * 3
    df['Team Score'] -= df['Unranked Losses'] * 7
    df['Team Score'] -= df['Conf Losses'] * (3 / df['Conference Multiplier'])
    df['Team Score'] -= (df['Overall Losses'] - df['Conf Losses']) * 5

    # Special case for FBSind teams
    df.loc[df['Conference'] == 'FBSind', 'Team Score'] = (
        df['AP Wins'] * 8 +
        df['Overall Wins'] * 5 -
        df['Overall Losses'] * 5 +
        df['Point Differential'] * 0.1 +
        df['SOR Score'] * 6
    )

    # Sort by Team Score in descending order
    df = df.sort_values(by='Team Score', ascending=False)

    # Save to CSV
    df[['Team Name', 'Conference', 'Team Score']].to_csv(output_file, index=False)
    print(f"Team scores saved to {output_file}!")

def get_top_12_teams(conference_ranking_file, team_score_file, output_file="cfp_prediction.csv"):
    """Determine the top 12 teams based on conference rankings and team scores."""
    conf_ranking = pd.read_csv(conference_ranking_file)
    team_scores = pd.read_csv(team_score_file)

    # Step 1: Get the top 4 conferences
    top_4_conferences = conf_ranking.nsmallest(4, 'Conference Rank')['Conference'].tolist()
    top_2_conferences = top_4_conferences[:2]
    next_2_conferences = top_4_conferences[2:]

    # Step 2: Get the best team from the top 4 conferences
    top_4_teams = []
    for conference in top_4_conferences:
        best_team = team_scores[team_scores['Conference'] == conference].sort_values(by='Team Score', ascending=False).iloc[0]
        top_4_teams.append(best_team)

    # Step 3: Assign seeds to the top 4 teams
    top_4_df = pd.DataFrame(top_4_teams)
    top_4_df = top_4_df.sort_values(by='Team Score', ascending=False).reset_index(drop=True)
    top_4_df.loc[:1, 'Seed'] = [1, 2]  # Spots 1 and 2
    top_4_df.loc[2:, 'Seed'] = [3, 4]  # Spots 3 and 4

    # Step 4: Get the highest-ranked team from conferences ranked 5-10
    remaining_conferences = conf_ranking[(conf_ranking['Conference Rank'] > 4) & (conf_ranking['Conference Rank'] <= 10)]['Conference'].tolist()
    remaining_teams = team_scores[team_scores['Conference'].isin(remaining_conferences)]
    seed_5_team = remaining_teams.sort_values(by='Team Score', ascending=False).iloc[0]

    # Step 5: Get the remaining best teams
    crossed_off_teams = top_4_df['Team Name'].tolist() + [seed_5_team['Team Name']]
    remaining_teams = team_scores[~team_scores['Team Name'].isin(crossed_off_teams)]
    remaining_teams = remaining_teams.sort_values(by='Team Score', ascending=False).head(7)

    # Step 6: Assign seeds
    seed_5_df = pd.DataFrame([seed_5_team]).reset_index(drop=True)
    seed_5_df['Seed'] = [5]

    remaining_teams = remaining_teams.reset_index(drop=True)
    remaining_teams['Seed'] = range(6, 13)

    # Combine all seeds into the final DataFrame
    final_df = pd.concat([top_4_df, seed_5_df, remaining_teams]).reset_index(drop=True)
    final_df = final_df[['Seed', 'Team Name', 'Conference', 'Team Score']]

    # Save to CSV
    final_df.to_csv(output_file, index=False)
    print(f"Top 12 seeds saved to {output_file}!")

def main():
    # File paths
    stats_file = "/Users/bosnianboi/Documents/GitHub/I310D_project/stats.csv"
    team_score_file = "/Users/bosnianboi/Documents/GitHub/I310D_project/team_score.csv"
    conference_ranking_file = "/Users/bosnianboi/Documents/GitHub/I310D_project/conference_ranking.csv"
    top_12_seeds_file = "/Users/bosnianboi/Documents/GitHub/I310D_project/cfp_prediction.csv"

    # Calculate team scores and save to team_score.csv
    calculate_team_scores(stats_file, team_score_file)

    # Determine top 12 teams and save to cfp_prediction.csv
    get_top_12_teams(conference_ranking_file, team_score_file, top_12_seeds_file)

if __name__ == "__main__":
    main()


















































