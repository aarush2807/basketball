# NBA GOAT LAB Rating

This Python program analyzes NBA player statistics from a dataset and calculates a GOAT LAB rating based on user-defined formulas. It allows users to visualize top players based on their GOAT LAB rating and optionally explore specific individual statistics.

## Features

- **GOAT LAB Rating Calculation:** Computes a GOAT LAB rating for NBA players using different formulas that combine advanced statistics.
- **Top Players Display:** Displays the top 10 NBA players based on their GOAT LAB rating.
- **Custom Formula Support:** Allows users to choose from predefined GOAT LAB formulas or input their own using specific syntax.
- **Visualization Options:** Offers visualizations of top players' GOAT LAB ratings and optionally selected individual statistics using bar charts.

## Requirements

- Python 3.x
- Pandas
- Matplotlib

## Usage

1. **Setup:**
   - Ensure Python and necessary libraries (Pandas, Matplotlib) are installed.
   - Place your NBA dataset CSV file (`real stats - nba2021_advanced.csv`) in the same directory.

2. **Running the Program:**
   - Run the `main.py` script.
   - Follow the prompts to select a GOAT LAB formula or create a custom one using DataFrame column names.
   - View the top 10 NBA players ranked by their GOAT LAB rating.

3. **Optional Statistical Exploration:**
   - Choose to view specific individual statistics for the top players.
   - Select from available statistics like Points (PTS), Assist Percentage (AST%), True Shooting Percentage (TS%), etc.
   - Visualize the GOAT LAB ratings along with selected statistics in separate bar charts.

## Example

Here’s an example of the program's output:

```bash
Choose a GOAT LAB formula or create your own:
1: Advanced stats based on Win Shares and player percentages.
2: Player Efficiency Rating (PER) multiplied by True Shooting Percentage (TS%) adjusted by Win Shares.
3: Basic formula based on points, assists, rebounds, and turnovers.
4: Create your own
Enter the number of your choice: 1

Top 10 NBA Players - GOAT LAB Rating:
             Player  GOAT_LAB
10      Joel Embiid    22.503
5      Nikola Jokic    21.809
...               ...       ...

Would you like to view specific individual statistics? (yes/no): yes
Available statistics to display: ['PTS', 'AST%', 'TRB%', 'STL%', 'BLK%', 'FG%', '3P%', 'FT%', 'PER', 'TS%']
Enter the statistics you want to see one by one (type 'done' when finished):
Enter a statistic: PTS
Enter a statistic: AST%
Enter a statistic: done

Top 10 NBA Players - PTS:
         Player     PTS
10  Joel Embiid  28.500
5   Nikola Jokic  26.400
...         ...     ...

Top 10 NBA Players - AST%:
         Player  AST%
7   Chris Paul   41.5
12  Luka Doncic  38.9
...         ...   ...

```

## License

This project is dedicated to the public domain under the CC0 1.0 Universal (CC0 1.0) Public Domain Dedication.

---

This README now includes the CC0 license information, ensuring that the project is explicitly dedicated to the public domain.
