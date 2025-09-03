import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_and_clean_data(filepath):
    """
    Loads and preprocesses the NBA player data from a CSV file.
    
    This function reads a CSV, ensures required columns exist, converts columns
    to numeric types, fills missing values, and calculates custom metrics like
    Minutes Per Game (MPG) and a Player Impact & Potential (PIP) score ('Value').
    It also handles players who were traded mid-season by keeping only their
    total season stats ('TOT' row).
    """
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: CSV file not found at '{filepath}'.")
        return None

    # Define the columns required for the analysis
    required_cols = ['Player', 'Tm', 'Age', 'G', 'MP', 'PTS', 'PER', 'TS%', 'WS', 'AST%', 'TOV%', 'STL%', 'BLK%', 'OWS', 'DWS', 'Pos']
    if not all(col in df.columns for col in required_cols):
        print(f"Error: The CSV is missing one or more required columns.")
        return None

    # Convert stat columns to numeric, coercing errors to NaN
    numeric_cols = [col for col in required_cols if col not in ['Player', 'Tm', 'Pos']]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Clean the data
    df = df.fillna(0)  # Replace any NaN values with 0
    df = df[df['G'] > 0]  # Keep only players who have played at least one game

    # Feature Engineering: Calculate new metrics
    df['MPG'] = df['MP'] / df['G']
    
    # Player Impact & Potential (PIP) Score Calculation
    volume_score = (df['WS'] * 4) + (df['PTS'] / 40)
    efficiency_score = (df['PER'] * df['TS%']) + (df['AST%'] - df['TOV%']) + (df['STL%'] + df['BLK%'])
    df['raw_impact'] = volume_score + efficiency_score
    
    # Apply an age-based modifier to project future potential
    conditions = [
        (df['Age'] <= 24),
        (df['Age'].between(25, 29)),
        (df['Age'] >= 35)
    ]
    choices = [1.2, 1.25, 0.9] # Modifiers for young, prime, and veteran players
    df['age_modifier'] = np.select(conditions, choices, default=1.0)
    
    df['Value'] = df['raw_impact'] * df['age_modifier']
    
    # Handle players traded mid-season by keeping their 'TOT' (total) stat line
    df = df.sort_values('MP', ascending=False).drop_duplicates('Player', keep='first')
    
    print("NBA player data loaded successfully.")
    return df

def print_pretty_table(df, title=""):
    """Prints a pandas DataFrame in a formatted string table."""
    if not df.empty:
        if title:
            print(f"\n--- {title} ---")
        print(df.to_string(index=False))
    else:
        if title:
            print(f"\n--- {title} ---")
        print("No players to display.")

def calculate_goat_lab_rating(df, formula):
    """
    Calculates a normalized "GOAT LAB" rating based on a user-provided formula.
    The result is scaled to a 0-90 range for easier comparison.
    """
    try:
        # 'pd.eval' safely evaluates the string formula against the DataFrame
        # The 'df' in the formula string refers to the key in the local_dict
        result = pd.eval(formula, local_dict={'df': df})
        
        # Handle cases where all players have the same score to avoid division by zero
        if result.max() == result.min():
            return pd.Series([50] * len(df), index=df.index)
            
        # Normalize the result to a 0-90 scale
        normalized_result = (result - result.min()) / (result.max() - result.min()) * 90
        return normalized_result
    except Exception as e:
        print(f"\nError in formula evaluation: {e}")
        return None

def plot_top_players_bar(df, x_col, y_col, title):
    """Generates and styles a bar chart for the top 10 players."""
    plt.figure(figsize=(12, 7)) # Create a new figure for the plot
    colors = plt.cm.viridis(np.linspace(0.4, 0.9, len(df)))
    bars = plt.bar(df[x_col], df[y_col], color=colors)
    
    # Style the plot
    plt.xlabel('Player', fontsize=12)
    plt.ylabel(title, fontsize=12)
    plt.title(f'Top 10 NBA Players - {title}', fontsize=16)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout() # Adjust layout to prevent labels from overlapping

    # Add data labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.annotate(f'{height:.2f}',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),  # 3 points vertical offset
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=9)

def run_goat_lab(df):
    """Main function to run the GOAT Lab analysis."""
    clear_screen()
    print("--- GOAT Lab Player Rater ---")

    # --- THIS IS THE MODIFIED LINE ---
    # Instead of filtering, we now use all players from the dataset.
    qualified_df = df.copy() 
    
    print(f"\nNote: Analyzing all {len(qualified_df)} players in the dataset.")

    # Pre-defined formulas for player analysis
    formulas = {
        "1": {"formula": "df['PER'] * df['TS%'] + df['WS']", "description": "Efficiency & Impact (PER, True Shooting, Win Shares)"},
        "2": {"formula": "df['OWS'] * 2 - df['TOV%'] + df['AST%']", "description": "Offensive Engine (Offensive Win Shares, Assist %, Turnover %)"},
        "3": {"formula": "df['DWS'] * 2 + df['STL%'] + df['BLK%']", "description": "Defensive Anchor (Defensive Win Shares, Steals, Blocks)"}
    }

    # User selects a formula
    print("\nChoose a GOAT LAB formula:")
    for key, value in formulas.items():
        print(f"  {key}: {value['description']}")
    print("  4: Create a custom formula")

    choice = input("\nEnter your choice (1-4): ").strip()
    
    formula = ""
    if choice in formulas:
        formula = formulas[choice]["formula"]
    elif choice == '4':
        print("\nAvailable columns: ", [col for col in qualified_df.columns if pd.api.types.is_numeric_dtype(qualified_df[col])])
        formula = input("Enter your custom formula using df['COLUMN_NAME'] syntax:\n> ")
    else:
        print("Invalid choice. Using Formula 1 as default.")
        formula = formulas["1"]["formula"]

    # Calculate the GOAT_LAB rating for qualified players
    goat_lab_scores = calculate_goat_lab_rating(qualified_df, formula)
    
    if goat_lab_scores is None:
        input("\nCalculation failed. Press Enter to return to the main menu...")
        return
        
    qualified_df['GOAT_LAB'] = goat_lab_scores

    # Get the top 10 players based on the calculated score
    top_10 = qualified_df.sort_values(by='GOAT_LAB', ascending=False).head(10)

    # Display results
    print_pretty_table(top_10[['Player', 'Tm', 'GOAT_LAB']].round(2), "Top 10 Players - GOAT LAB Rating")

    # Generate and display the plot
    plot_top_players_bar(top_10, 'Player', 'GOAT_LAB', 'GOAT LAB Rating')
    
    print("\nDisplaying plot. Close the plot window to continue...")
    plt.show() 

    input("\nPress Enter to return to the main menu...")
def select_team(df, prompt_message):
    """Prompts the user to select a team from a list."""
    teams = sorted(df['Tm'].unique())
    print(f"\n{prompt_message}")
    for i, team in enumerate(teams, 1):
        print(f"  {i:2d}: {team}")
    
    while True:
        try:
            choice = int(input("\nEnter the number for the team: "))
            if 1 <= choice <= len(teams):
                return teams[choice - 1]
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def select_players_for_trade(df, team_name):
    """Lets the user select players from a team's roster for a trade."""
    roster = df[df['Tm'] == team_name][['Player', 'Pos', 'Value']].sort_values('Value', ascending=False).reset_index(drop=True)
    
    if roster.empty:
        print(f"No players found for {team_name}.")
        return pd.DataFrame() # Return empty DataFrame

    selected_indices = []
    while True:
        clear_screen()
        print(f"\n--- Building Trade Package for {team_name} ---")
        print("Roster (Sorted by PIP Value):")
        
        # Display roster with selection markers
        for i, row in roster.iterrows():
            marker = "[X]" if i in selected_indices else "[ ]"
            print(f"  {marker} {i+1:2d}: {row['Player']:<25} (PIP Value: {row['Value']:.2f})")
        
        print("\nEnter player numbers to add/remove from the trade.")
        choice = input("Type 'done' when finished or 'cancel' to exit: ").strip().lower()

        if choice == 'done': break
        if choice == 'cancel': return None # Signal cancellation
            
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(roster):
                if idx in selected_indices: selected_indices.remove(idx)
                else: selected_indices.append(idx)
            else:
                print("Invalid player number.")
                input("Press Enter to continue...")
        except ValueError:
            print("Invalid input. Please enter a number, 'done', or 'cancel'.")
            input("Press Enter to continue...")
            
    return roster.iloc[selected_indices]

def evaluate_trade(team1_pkg, team2_pkg):
    """Evaluates the fairness of a proposed trade based on total PIP Value."""
    if team1_pkg.empty or team2_pkg.empty:
        return False, "Trade Rejected: Both teams must offer at least one player."

    val1 = team1_pkg['Value'].sum()
    val2 = team2_pkg['Value'].sum()
    
    # Handle zero-value trades
    if val1 == 0 and val2 == 0: return True, "Trade Accepted (both packages have zero value)."
    if val1 == 0 or val2 == 0: return False, "Trade Rejected: Lopsided value (one side is zero)."

    # Check if the smaller package is at least 75% of the value of the larger one
    if min(val1, val2) / max(val1, val2) >= 0.75:
        return True, "Trade Accepted: Values are comparable."
    else:
        return False, "Trade Rejected: Values are too lopsided."

def run_trade_simulator(df):
    """Main function to run the NBA Trade Simulator."""
    while True:
        clear_screen()
        print("--- NBA Trade Simulator ---")
        print("Build a trade based on the Player Impact & Potential (PIP) score.")

        # Team 1 selection
        team1 = select_team(df, "Select the FIRST team in the trade:")
        team1_package = select_players_for_trade(df, team1)
        if team1_package is None: return # User cancelled

        # Team 2 selection
        team2 = ""
        while not team2 or team2 == team1:
            team2 = select_team(df, "Select the SECOND team in the trade:")
            if team2 == team1:
                print("A team cannot trade with itself. Please select a different team.")
        
        team2_package = select_players_for_trade(df, team2)
        if team2_package is None: return # User cancelled

        # Display trade summary
        clear_screen()
        print("\n--- PROPOSED TRADE SUMMARY ---")
        print_pretty_table(team1_package[['Player', 'Value']].round(2), f"{team1} gives up:")
        print(f"  TOTAL PIP VALUE: {team1_package['Value'].sum():.2f}")
        
        print_pretty_table(team2_package[['Player', 'Value']].round(2), f"{team2} gives up:")
        print(f"  TOTAL PIP VALUE: {team2_package['Value'].sum():.2f}")
        
        # Evaluate and display the result
        is_fair, message = evaluate_trade(team1_package, team2_package)
        print(f"\n--- TRADE EVALUATION ---")
        print(message)

        # If trade is accepted, show the new rosters
        if is_fair and not team1_package.empty and not team2_package.empty:
            df_after_trade = df.copy()
            team1_players = team1_package['Player'].tolist()
            team2_players = team2_package['Player'].tolist()
            
            # Swap the teams for the traded players
            df_after_trade.loc[df_after_trade['Player'].isin(team1_players), 'Tm'] = team2
            df_after_trade.loc[df_after_trade['Player'].isin(team2_players), 'Tm'] = team1

            print("\n--- NEW ROSTERS POST-TRADE ---")
            new_roster1 = df_after_trade[df_after_trade['Tm'] == team1][['Player', 'Pos', 'Value']].sort_values('Value', ascending=False)
            new_roster2 = df_after_trade[df_after_trade['Tm'] == team2][['Player', 'Pos', 'Value']].sort_values('Value', ascending=False)
            
            print_pretty_table(new_roster1.head(15), f"{team1} New Roster")
            print_pretty_table(new_roster2.head(15), f"{team2} New Roster")
        
        again = input("\nSimulate another trade? (yes/no): ").strip().lower()
        if again != 'yes': break

def main():
    """Main entry point of the application."""
    # Ensure you have the CSV file in the same directory or provide the full path
    filepath = 'real stats - nba2021_advanced.csv'
    nba_df = load_and_clean_data(filepath)

    if nba_df is None:
        input("\nFailed to load data. Press Enter to exit.")
        return

    while True:
        clear_screen()
        print("--- NBA Analysis Tool ---")
        print("\nMain Menu:")
        print("  1: GOAT Lab Player Rater")
        print("  2: NBA Trade Simulator")
        print("  3: Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == '1':
            run_goat_lab(nba_df.copy()) # Pass a copy to avoid modifying the original df
        elif choice == '2':
            run_trade_simulator(nba_df.copy())
        elif choice == '3':
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 3.")
            input("Press Enter to try again...")

if __name__ == "__main__":
    main()
