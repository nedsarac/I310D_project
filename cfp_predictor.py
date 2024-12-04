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
        df['AP Wins'] * 12 +
        (df['Conf Wins'] * df['Conference Multiplier'] * 5) +
        ((df['Overall Wins'] - df['Conf Wins']) * 6) +
        df['Point Differential'] * 0.1 +
        df['SOR Score'] * 20  # Incorporate SOR with a significant weight
    )

    # Apply penalties
    df['Unranked Losses'] = df['Overall Losses'] - df['AP Losses']
    df['Team Score'] -= df['AP Losses'] * 10
    df['Team Score'] -= df['Unranked Losses'] * 15
    df['Team Score'] -= df['Conf Losses'] * (5 / df['Conference Multiplier'])
    df['Team Score'] -= (df['Overall Losses'] - df['Conf Losses']) * 5

    # Special case for FBSind teams
    df.loc[df['Conference'] == 'FBSind', 'Team Score'] = (
        df['AP Wins'] * 12 +
        df['Overall Wins'] * 5 -
        df['Overall Losses'] * 5 +
        df['Point Differential'] * 0.1 +
        df['SOR Score'] * 20
    )

    # Sort by Team Score in descending order
    df = df.sort_values(by='Team Score', ascending=False)

    # Save to CSV
    df[['Team Name', 'Conference', 'Team Score']].to_csv(output_file, index=False)
    print(f"Team scores saved to {output_file}!")


def get_top_12_teams(team_score_file, output_file="cfp_prediction.csv"):
    """Rank teams based on Team Score with constraints for unique conferences."""
    # Load team scores
    team_scores = pd.read_csv(team_score_file)

    # Sort teams by Team Score in descending order
    team_scores = team_scores.sort_values(by='Team Score', ascending=False).reset_index(drop=True)

    # Step 1: Select seeds 1–4 with unique conferences (excluding FBSind)
    seeds_1_to_4 = []
    used_conferences = set()

    for _, row in team_scores.iterrows():
        if len(seeds_1_to_4) < 4 and row['Conference'] not in used_conferences and row['Conference'] != 'FBSind':
            seeds_1_to_4.append(row)
            used_conferences.add(row['Conference'])

    # If fewer than 4 unique conferences are found, raise an error
    if len(seeds_1_to_4) < 4:
        raise ValueError("Not enough unique conferences to fill seeds 1–4.")

    # Step 2: Select remaining teams for seeds 5–12
    remaining_teams = team_scores[~team_scores['Team Name'].isin([team['Team Name'] for team in seeds_1_to_4])]
    seeds_5_to_12 = remaining_teams.head(8).to_dict('records')

    # Step 3: Ensure a 5th unique conference in seeds 5–12 (excluding FBSind)
    fifth_conference_team = None
    for _, row in remaining_teams.iterrows():
        if row['Conference'] not in used_conferences and row['Conference'] != 'FBSind':
            fifth_conference_team = row
            used_conferences.add(row['Conference'])
            break

    # If a 5th unique conference team is found, ensure they are in seeds 5–12
    if fifth_conference_team is not None:
        # Replace the lowest-ranked team in seeds 5–12 with the 5th conference team
        seeds_5_to_12[-1] = fifth_conference_team

    # Sort seeds 5–12 back by Team Score
    seeds_5_to_12 = sorted(seeds_5_to_12, key=lambda x: x['Team Score'], reverse=True)

    # Assign seeds
    seeds_1_to_4_df = pd.DataFrame(seeds_1_to_4).reset_index(drop=True)
    seeds_1_to_4_df['Seed'] = range(1, 5)

    seeds_5_to_12_df = pd.DataFrame(seeds_5_to_12).reset_index(drop=True)
    seeds_5_to_12_df['Seed'] = range(5, 13)

    # Combine all seeds
    final_df = pd.concat([seeds_1_to_4_df, seeds_5_to_12_df]).reset_index(drop=True)
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
    get_top_12_teams(team_score_file, top_12_seeds_file)


if __name__ == "__main__":
    main()




























































