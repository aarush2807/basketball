NBA Analysis & Trade Simulator
A command-line tool for basketball fans and aspiring GMs. Dive deep into player stats with the "GOAT Lab" to create your own rankings, or fire up the Trade Simulator to build and evaluate blockbuster trades. This script is built with Python and uses the Pandas library for data crunching and Matplotlib for visualization.

Features
GOAT Lab Player Rater:

Rank players using one of three preset formulas focused on efficiency, offense, or defense.

Get creative and build your own custom formula using any stat in the dataset.

Instantly visualize the top 10 players for any formula with a clean bar chart.

NBA Trade Simulator:

Simulate a trade between any two teams in your dataset.

Interactively build trade packages player by player.

The tool automatically evaluates if the trade is fair based on a custom "Player Impact & Potential (PIP)" score.

If a trade is accepted, you can see the newly formed rosters for both teams.

How To Run
Getting this tool running is simple. You just need Python, a few common libraries, and a CSV file with NBA stats.

1. Prerequisites
Make sure you have Python 3 installed. You'll also need the following libraries:

pip install pandas matplotlib numpy

2. Get The Data
This script is designed to work with advanced player stats from any season.

Download the advanced stats for a season from a site like Basketball-Reference.com.

Export the data as a CSV file.

Save the file in the same directory as the script and name it nba2021_advanced.csv.

Required Columns: Your CSV must contain the following columns for the script to work correctly: Player, Tm, Age, G, MP, PTS, PER, TS%, WS, AST%, TOV%, STL%, BLK%, OWS, DWS, and Pos.

3. Launch the App
Open your terminal or command prompt, navigate to the project directory, and run:

python your_script_name.py

(Replace your_script_name.py with the actual name of your Python file.)

From there, the on-screen menus will guide you through the rest!

How It Works
The tool is built around two key custom metrics:

Player Impact & Potential (PIP) Score: This is the engine behind the Trade Simulator. It calculates a single "value" for each player by combining their on-court production (Win Shares, Points) and efficiency (PER, TS%) with an age-based modifier. Younger players in their prime get a slight boost, while veterans see a slight decrease, simulating how a real front office might value players.

GOAT LAB Rating: This is a normalized score used in the player rater. After calculating a player's score from a given formula, the script scales all results to a 0-90 range. This makes it easy to compare players, even if you are using wildly different custom formulas.

Contributing
Have an idea for a new feature or found a bug? Feel free to open an issue or submit a pull request. All contributions are welcome!
