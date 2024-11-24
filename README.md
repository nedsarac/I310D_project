# I310D_project
2025 CFP Prediction

<!-- Directions -->

1. Immediate Steps: Data Collection Strategy
Start with a Sample Dataset:
Aim to collect a small sample (e.g., data for the top 5 teams over a few games) to get a feel for the structure and ensure your scraping code works.
Identify a reliable source (e.g., ESPN or Sports Reference) and use BeautifulSoup4 to scrape essential metrics like team W-L record, point differential, average points scored, and average points allowed.
Store this sample data in a CSV file to streamline testing.
Set Up GitHub Repository:
Organize your GitHub repository to keep it clean and collaborative. Suggested folders:
/data: Store your sample data and, later, the full dataset.
/scripts: For Python scripts (e.g., scraping, cleaning, analysis).
/notebooks: Any Jupyter notebooks for exploration.
/results: Output files, predictions, and summary reports.
2. Iterative Data Collection
Expand Your Scraping Scope:
After validating your sample dataset, proceed to scrape data for all relevant teams up to week 9. Focus on these fields based on your proposal:
Team W-L Record
Point Differential
Average Points Scored and Allowed
Ranked Wins
Continue storing each step’s output in CSV files, as this keeps the data manageable and helps troubleshoot any scraping issues early.
3. Data Processing and Transformation
Data Cleaning:
Use Pandas to clean and preprocess the data. Ensure fields like win-loss records are consistent and numerical values (e.g., point differential) are standardized.
Data Exploration:
Perform a quick exploratory analysis in a Jupyter notebook to verify that all metrics align with your expectations.
4. Model Development
Baseline Model:
Start with simpler models like LogisticRegression and MLPClassifier from scikit-learn to predict wins and losses. These models can use metrics like point differential, average points, and win-loss records.
Split your dataset into training and test sets (using k-fold cross-validation for reliability).
Refine Model Based on Performance:
Evaluate your model’s predictions and adjust as needed.
Save your model parameters and notes on performance in GitHub to keep a record of iterations.
5. Team Ranking Algorithm
Build Ranking Logic:
Use your model’s predictions for each team’s remaining games to simulate final W-L records.
Develop ranking logic that factors in key metrics (W-L, conference championships, strength of schedule) to sort the top 12 teams.
Test Ranking Against AP Polls:
Compare your model’s rankings with AP poll rankings as a form of validation, as suggested by your professor. You can use correlation or other similarity metrics to evaluate alignment.
6. Deliverables and Documentation
Documentation:
Write clear, concise documentation for each part of the process. This includes how data was scraped, model setup, ranking methodology, and any analysis performed.
Code Comments and GitHub README:
Comment your code extensively, explaining both what each part does and why it’s necessary.
Update your repository’s README to include an overview of the project, instructions for running scripts, and notes on each milestone.
7. Presentation and Final Report
Presentation:
Summarize the project’s motivation, methodology, key results, and any challenges encountered.
Final Report:
Include details on the dataset creation process, model selection, ranking results, and any insights on model performance relative to AP polls.