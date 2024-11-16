import pandas as pd

def calculate_team_scores(input_file, output_file="team_score.csv"):
    """Calculate Team Scores based on provided weights and penalties."""
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

    # Calculate Team Score
    df['Point Differential'] = df['PF'] - df['PA']
    df['Team Score'] = (
        df['AP Wins'] * 10 +
        (df['Conf Wins'] * df['Conference Multiplier'] * 5) +
        ((df['Overall Wins'] - df['Conf Wins']) * 5) +
        df['Point Differential'] * 0.1
    )

    # Apply penalties
    df['Unranked Losses'] = df['Overall Losses'] - df['AP Losses']
    df['Team Score'] -= df['AP Losses'] * 3
    df['Team Score'] -= df['Unranked Losses'] * 7
    df['Team Score'] -= df['Conf Losses'] * (3 / df['Conference Multiplier'])
    df['Team Score'] -= (df['Overall Losses'] - df['Conf Losses']) * 5

    # Special case for FBSind teams
    df.loc[df['Conference'] == 'FBSind', 'Team Score'] = (
        df['AP Wins'] * 10 +
        df['Overall Wins'] * 5 -
        df['Overall Losses'] * 5 +
        df['Point Differential'] * 0.1
    )

    # Sort by Team Score in descending order
    df = df.sort_values(by='Team Score', ascending=False)

    # Save to CSV
    df[['Team Name', 'Conference', 'Team Score']].to_csv(output_file, index=False)
    print(f"Team scores saved to {output_file}!")

def get_top_12_teams(conference_ranking_file, team_score_file, output_file="top_12_seeds.csv"):
    """Determine the top 12 teams based on conference rankings and team scores."""
    conf_ranking = pd.read_csv(conference_ranking_file)
    team_scores = pd.read_csv(team_score_file)

    # Step 1: Get the top 2 conferences
    top_2_conferences = conf_ranking.nsmallest(2, 'Conference Rank')['Conference'].tolist()

    # Step 2: Get the best team from each of the top 2 conferences
    best_teams = []
    for conference in top_2_conferences:
        best_team = team_scores[team_scores['Conference'] == conference].sort_values(by='Team Score', ascending=False).iloc[0]
        best_teams.append(best_team)

    # Sort the best two teams by Team Score
    best_teams_df = pd.DataFrame(best_teams).sort_values(by='Team Score', ascending=False).reset_index(drop=True)
    best_teams_df['Seed'] = [1, 2]

    # Step 3: Get the next 10 best teams
    remaining_teams = team_scores[~team_scores['Team Name'].isin(best_teams_df['Team Name'])]
    top_10_remaining = remaining_teams.sort_values(by='Team Score', ascending=False).head(10)
    top_10_remaining['Seed'] = range(3, 13)

    # Step 4: Combine the top 2 and next 10 teams
    top_12_teams = pd.concat([best_teams_df, top_10_remaining]).reset_index(drop=True)
    top_12_teams = top_12_teams[['Seed', 'Team Name', 'Conference', 'Team Score']]

    # Save to CSV
    top_12_teams.to_csv(output_file, index=False)
    print(f"Top 12 seeds saved to {output_file}!")

def main():
    # File paths
    stats_file = "/Users/bosnianboi/Documents/GitHub/I310D_project/stats.csv"
    team_score_file = "/Users/bosnianboi/Documents/GitHub/I310D_project/team_score.csv"
    conference_ranking_file = "/Users/bosnianboi/Documents/GitHub/I310D_project/conference_ranking.csv"
    top_12_seeds_file = "/Users/bosnianboi/Documents/GitHub/I310D_project/cfp_prediction.csv"

    # Calculate team scores and save to team_score.csv
    calculate_team_scores(stats_file, team_score_file)

    # Determine top 12 teams and save to top_12_seeds.csv
    get_top_12_teams(conference_ranking_file, team_score_file, top_12_seeds_file)

if __name__ == "__main__":
    main()


















































