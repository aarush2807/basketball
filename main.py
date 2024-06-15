import pandas as pd
import matplotlib.pyplot as plt

def calculate_goat_lab_rating(df, formula):
    return eval(formula)

def plot_top_players_bar(df, x_col, y_col, title, color):
    bars = plt.bar(df[x_col], df[y_col], color=color)
    plt.xlabel('Player')
    plt.ylabel(title)
    plt.title('Top 10 NBA Players - {}'.format(title))
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Add value labels on top of the bars
    for bar in bars:
        height = bar.get_height()
        plt.annotate('{}'.format(round(height, 3)), 
                     xy=(bar.get_x() + bar.get_width() / 2, height), 
                     xytext=(0, 3),  # 3 points vertical offset
                     textcoords="offset points",
                     ha='center', va='bottom')

def print_top_players(df, columns):
    rounded_df = df.copy()
    rounded_df[columns] = rounded_df[columns].round(3)
    print(rounded_df[['Player'] + columns])

# Read the CSV file
df = pd.read_csv('real stats - nba2021_advanced.csv')

# Filter players with a minimum points requirement
df = df[df['PTS'] >= 15]

# Example GOAT LAB formulas with descriptions
formulas = {
    "1": {
        "formula": "((48 * (df['OWS'] + df['DWS']) / (df['MP'] / 5))) * (df['WS/48']) + 0.5 * ((48 * (df['OWS'] + df['DWS']) / (df['MP'] / 5))) * (df['PTS'] + df['TRB%'] + df['AST%'] + df['STL%'] + df['BLK%'] + df['TOV%'])",
        "description": "Advanced stats based on Win Shares and player percentages."
    },
    "2": {
        "formula": "df['PER'] * df['TS%'] + df['OWS'] - df['DWS']",
        "description": "Player Efficiency Rating (PER) multiplied by True Shooting Percentage (TS%) adjusted by Win Shares."
    },
    "3": {
        "formula": "df['PTS'] + df['AST'] + df['TRB'] - df['TOV']",
        "description": "Basic formula based on points, assists, rebounds, and turnovers."
    }
}

# Display available formulas with descriptions
print("Choose a GOAT LAB formula or create your own:")
for key, value in formulas.items():
    print(f"{key}: {value['description']}")
print("4: Create your own")

# User input for GOAT LAB formula
choice = input("Enter the number of your choice: ")

if choice in formulas:
    formula = formulas[choice]["formula"]
elif choice == '4':
    formula = input("Enter your custom GOAT LAB formula using df['COLUMN_NAME'] syntax: ")
else:
    print("Invalid choice. Using Formula 1 as default.")
    formula = formulas["1"]["formula"]

# Calculate GOAT LAB rating
df['GOAT_LAB'] = calculate_goat_lab_rating(df, formula)
df = df.sort_values(by='GOAT_LAB', ascending=False)
top_players_goat_lab = df.head(10)

# Print the top players and their GOAT LAB rating
print("\nTop 10 NBA Players - GOAT LAB Rating:")
print_top_players(top_players_goat_lab, ['GOAT_LAB'])

# Ask user if they want to view specific stats
view_stats = input("\nWould you like to view specific individual statistics? (yes/no): ").lower()

if view_stats == 'yes':
    # User input for which stats to display
    available_stats = ['PTS', 'AST%', 'TRB%', 'STL%', 'BLK%', 'FG%', '3P%', 'FT%', 'PER', 'TS%']
    selected_stats = []

    print("Available statistics to display: ", available_stats)
    print("Enter the statistics you want to see one by one (type 'done' when finished):")

    while True:
        stat = input("Enter a statistic: ").upper().strip()
        if stat == 'DONE':
            break
        if stat in available_stats:
            selected_stats.append(stat)
        else:
            print("Invalid statistic. Please enter a valid statistic from the list.")

    # Plotting for GOAT LAB Rating
    plt.figure(figsize=(20, 8))
    plt.subplot(1, len(selected_stats) + 1, 1)
    plot_top_players_bar(top_players_goat_lab, 'Player', 'GOAT_LAB', 'GOAT LAB Rating', 'skyblue')

    # Plotting for each selected stat
    for i, stat in enumerate(selected_stats):
        top_players_stat = df.sort_values(by=stat, ascending=False).head(10)
        print("\nTop 10 NBA Players - {}: ".format(stat))
        print_top_players(top_players_stat, [stat])

        plt.subplot(1, len(selected_stats) + 1, i + 2)
        plot_top_players_bar(top_players_stat, 'Player', stat, stat, 'lightcoral')

    plt.tight_layout()
    plt.show()
elif view_stats == 'no':
    # Plotting only GOAT LAB Rating
    plt.figure(figsize=(8, 6))
    plot_top_players_bar(top_players_goat_lab, 'Player', 'GOAT_LAB', 'GOAT LAB Rating', 'skyblue')
    plt.tight_layout()
    plt.show()
else:
    print("Invalid input. Exiting program.")
