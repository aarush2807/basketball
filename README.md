# NBA Analysis & Trade Simulator

A command-line tool for basketball fans and aspiring general managers. Explore advanced player stats in the **GOAT Lab** to create your own rankings, or test your GM skills in the **Trade Simulator** to build and evaluate blockbuster trades.

This project is built with **Python**, using **Pandas** for data crunching and **Matplotlib** for visualization.

---

## Features

### GOAT Lab Player Rater

* Rank players using one of three preset formulas: Efficiency, Offense, or Defense.
* Create your own custom formula with any stat in the dataset.
* Instantly visualize the top 10 players with a clean bar chart.

### NBA Trade Simulator

* Simulate trades between any two teams in the dataset.
* Interactively build trade packages, player by player.
* Evaluate trades automatically using the custom **Player Impact & Potential (PIP)** score.
* If a trade is accepted, view the updated rosters for both teams.

---

## How To Run

Getting started is simple. You just need Python, a few common libraries, and a CSV file with NBA stats.

### 1. Install Prerequisites

Make sure you have Python 3 installed. Then install the required libraries:

```bash
pip install pandas matplotlib numpy
```

### 2. Get the Data

This tool works with advanced player stats from any NBA season.

1. Download advanced stats from [Basketball-Reference.com](https://www.basketball-reference.com/).
2. Export the stats as a CSV file.
3. Save the file in the same directory as the script and name it:

   ```
   nba2021_advanced.csv
   ```

**Required Columns**:
`Player, Tm, Age, G, MP, PTS, PER, TS%, WS, AST%, TOV%, STL%, BLK%, OWS, DWS, Pos`

### 3. Launch the Application

Open your terminal, navigate to the project directory, and run:

```bash
python your_script_name.py
```

Replace `your_script_name.py` with the actual name of your file.

The on-screen menus will guide you from there.

---

## How It Works

### Player Impact & Potential (PIP) Score

This is the engine behind the Trade Simulator. It calculates a single value for each player by combining:

* On-court production (Win Shares, Points)
* Efficiency (PER, TS%)
* Age-based modifier (boost for younger players, slight decrease for veterans)

This models how a real front office might evaluate player value.

### GOAT Lab Rating

The GOAT Lab uses a normalized score to compare players. After applying your chosen formula, all results are scaled to a **0–90 range**, making it easy to compare players even when using very different formulas.

---

## Contributing

Got an idea for a new feature or found a bug? Open an issue or submit a pull request. Contributions of all kinds are welcome!

---

Would you like me to also make this **GitHub README-ready** (with badges, table of contents, and code formatting polish) so it looks professional for a repo?

