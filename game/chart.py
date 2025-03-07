#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chart module for Yolo Terminal game.
Handles ASCII art charts for displaying data trends.
"""

from typing import List, Dict, Any, Optional
from colorama import Fore, Style, Back, init

# Initialize colorama
init(autoreset=True)

class Chart:
    """
    Chart class to handle ASCII art charts for the game.
    """
    
    def __init__(self):
        """Initialize the Chart."""
        # Define colors
        self.header_bg = "\033[44;1m"  # Darker blue background
        self.header_fg = Fore.WHITE
        self.positive = Fore.GREEN
        self.negative = Fore.RED
        self.highlight = Fore.YELLOW
        self.title = Fore.CYAN + Style.BRIGHT
    
    def display_width(self, s: str) -> int:
        """
        Calculate display width of a string.
        
        Args:
            s: String to calculate width for
            
        Returns:
            int: Display width of the string
        """
        # Remove ANSI color codes for width calculation
        clean_s = s
        for color in [Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.CYAN, Fore.WHITE, Fore.MAGENTA,
                     Back.BLUE, Back.BLACK, Back.RED, Style.BRIGHT, Style.RESET_ALL]:
            clean_s = clean_s.replace(f"{color}", "")
        
        # Also remove custom ANSI escape codes
        clean_s = clean_s.replace("\033[44;1m", "")  # Custom darker blue background
        clean_s = clean_s.replace("\033[43m", "")    # Orange background for headlines
        
        return len(clean_s)
    
    def show_net_worth_chart(self, net_worth_history: List[Dict[str, Any]], clear_screen_func=None) -> None:
        """
        Display an ASCII art line chart of the player's net worth over time.
        
        Args:
            net_worth_history: List of daily stats dictionaries
            clear_screen_func: Function to clear the screen (optional)
        """
        if not net_worth_history:
            return
        
        if clear_screen_func:
            clear_screen_func()
        
        # Extract days and net worth values
        days = [stat["day"] for stat in net_worth_history]
        net_worths = [stat["net_worth"] for stat in net_worth_history]
        total_assets = [stat["total_assets"] for stat in net_worth_history]
        
        # Find min and max values for scaling
        min_net_worth = min(net_worths)
        max_net_worth = max(net_worths)
        min_total = min(total_assets)
        max_total = max(total_assets)
        
        # Use the overall min and max for consistent scaling
        min_value = min(min_net_worth, min_total)
        max_value = max(max_net_worth, max_total)
        
        # Ensure there's a range to display
        if max_value == min_value:
            max_value = min_value + 1
        
        # Chart dimensions - adjusted to fit within 80 chars
        chart_height = 15
        chart_width = 60
        
        # Make sure to reset any previous color codes
        print(f"{Style.RESET_ALL}", end="")
        
        # Bloomberg Terminal style UI - fixed width 80 chars (78 inside borders)
        print(f"{self.header_bg}{self.header_fg}╔" + "═" * 78 + f"╗{Style.RESET_ALL}")
        
        title = "NET WORTH CHART"
        title_padding = (78 - len(title)) // 2
        print(f"{self.header_bg}{self.header_fg}║" + " " * title_padding + title + " " * (78 - title_padding - len(title)) + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}╠" + "═" * 78 + f"╣{Style.RESET_ALL}")
        
        # Create the chart
        chart = []
        
        # Y-axis labels (left side)
        y_labels = []
        for i in range(chart_height + 1):
            value = max_value - (i / chart_height) * (max_value - min_value)
            y_labels.append(f"${int(value)}")
        
        # Find the maximum length of y-axis labels for padding
        max_label_len = max(len(label) for label in y_labels)
        
        # Create the chart rows
        for i in range(chart_height + 1):
            if i == 0:
                # Top row with max value
                row = f"{self.header_bg}{self.header_fg}║ {y_labels[i]:<{max_label_len}} ┌" + "─" * chart_width + "┐"
            elif i == chart_height:
                # Bottom row with min value
                row = f"{self.header_bg}{self.header_fg}║ {y_labels[i]:<{max_label_len}} └" + "─" * chart_width + "┘"
            else:
                # Middle rows with grid lines
                row = f"{self.header_bg}{self.header_fg}║ {y_labels[i]:<{max_label_len}} │" + " " * chart_width + "│"
            
            # Pad to fixed width
            padding = 78 - self.display_width(row)
            row += " " * padding + f"║{Style.RESET_ALL}"
            chart.append(row)
        
        # Plot the net worth line
        for day_idx, net_worth in enumerate(net_worths):
            if day_idx >= len(days):
                continue
                
            # Calculate x position
            x_pos = int((days[day_idx] - 1) / 40 * chart_width)
            if x_pos >= chart_width:
                x_pos = chart_width - 1
            
            # Calculate y position (inverted because rows go from top to bottom)
            y_pos = chart_height - int((net_worth - min_value) / (max_value - min_value) * chart_height)
            if y_pos < 0:
                y_pos = 0
            elif y_pos > chart_height:
                y_pos = chart_height
            
            # Place the point on the chart
            row = chart[y_pos]
            # Find the position to insert the marker
            pos = row.find("│") + 1 + x_pos if "│" in row else row.find("└") + 1 + x_pos
            # Replace the character at that position with a marker
            row_chars = list(row)
            # Use a simple character without color codes for now
            row_chars[pos] = "O"
            chart[y_pos] = "".join(row_chars)
        
        # Plot the total assets line (including portfolio value)
        for day_idx, total in enumerate(total_assets):
            if day_idx >= len(days):
                continue
                
            # Calculate x position
            x_pos = int((days[day_idx] - 1) / 40 * chart_width)
            if x_pos >= chart_width:
                x_pos = chart_width - 1
            
            # Calculate y position (inverted because rows go from top to bottom)
            y_pos = chart_height - int((total - min_value) / (max_value - min_value) * chart_height)
            if y_pos < 0:
                y_pos = 0
            elif y_pos > chart_height:
                y_pos = chart_height
            
            # Place the point on the chart
            row = chart[y_pos]
            # Find the position to insert the marker
            pos = row.find("│") + 1 + x_pos if "│" in row else row.find("└") + 1 + x_pos
            # Replace the character at that position with a marker
            row_chars = list(row)
            # Use a simple character without color codes for now
            row_chars[pos] = "#"
            chart[y_pos] = "".join(row_chars)
        
        # Print the chart
        for row in chart:
            print(row)
        
        # Print x-axis labels
        x_label = "Day: "
        for i in range(5):
            day = 1 + i * 10
            pos = int(day / 40 * chart_width)
            x_label += " " * (pos - len(x_label)) + str(day)
        
        x_label_padding = 78 - len(x_label) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {x_label}" + " " * x_label_padding + f"║{Style.RESET_ALL}")
        
        # Print legend
        legend = "Legend: O Net Worth (Cash + Savings - Debt)   # Total Assets (incl. Portfolio)"
        legend_padding = 78 - len(legend) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {legend}" + " " * legend_padding + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}╚" + "═" * 78 + f"╝{Style.RESET_ALL}")
        input("\nPress Enter to continue...")

def generate_test_data() -> List[Dict[str, Any]]:
    """
    Generate synthetic data for testing the chart.
    
    Returns:
        List of daily stats dictionaries
    """
    import random
    import math
    
    # Generate 40 days of data
    data = []
    
    # Start with initial values
    cash = 2000
    bank_savings = 0
    debt = 5000
    portfolio_value = 0
    
    for day in range(1, 41):
        # Simulate some random changes
        cash_change = random.randint(-500, 1000)
        bank_change = random.randint(-200, 500)
        debt_change = random.randint(-300, 100)
        portfolio_change = random.randint(-200, 800)
        
        # Apply changes
        cash += cash_change
        bank_savings += bank_change
        debt = max(0, debt + debt_change)  # Debt can't go below 0
        portfolio_value = max(0, portfolio_value + portfolio_change)  # Portfolio value can't go below 0
        
        # Add some trends
        # Sine wave for cash to simulate trading cycles
        cash += int(500 * math.sin(day / 5))
        
        # Gradually increase bank savings
        bank_savings += day * 10
        
        # Gradually decrease debt
        debt = max(0, debt - day * 20)
        
        # Calculate net worth and total assets
        net_worth = cash + bank_savings - debt
        total_assets = net_worth + portfolio_value
        
        # Create the daily stat
        daily_stat = {
            "day": day,
            "cash": cash,
            "bank_savings": bank_savings,
            "debt": debt,
            "health": random.randint(50, 100),
            "fame": random.randint(50, 100),
            "net_worth": net_worth,
            "portfolio_value": portfolio_value,
            "total_assets": total_assets
        }
        
        data.append(daily_stat)
    
    return data

def main():
    """Test function to demonstrate the chart with synthetic data."""
    import os
    
    # Function to clear the screen
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    # Generate test data
    test_data = generate_test_data()
    
    # Create chart and display it
    chart = Chart()
    chart.show_net_worth_chart(test_data, clear_screen)
    
    print("Chart test completed successfully!")

if __name__ == "__main__":
    main()
