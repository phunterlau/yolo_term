# YOLO Terminal

A Bloomberg Terminal-inspired stock trading game where you try to make as much money as possible in 40 days.

![YOLO Terminal](https://github.com/yourusername/yolo_term/raw/main/screenshots/yolo_terminal.png)

## Overview

YOLO Terminal is a text-based stock trading simulation game with a retro Bloomberg Terminal aesthetic. You start as a college student with $2000 in cash and $5000 in student loan debt. Your goal is to trade stocks, manage your finances, and make as much money as possible within 40 days.

## Features

- **Bloomberg Terminal-inspired UI**: Experience the nostalgic feel of a financial terminal with a blue-on-black interface
- **Dynamic Stock Market**: Stock prices fluctuate daily based on market conditions and random events
- **Portfolio Management**: Buy and sell stocks to build your portfolio
- **Multiple Locations**: Visit the Bank, Hospital, Trading App, Darkweb, and more
- **Random Events**: Experience unexpected market shifts, health issues, and financial opportunities
- **Health & Reputation System**: Manage your health and reputation alongside your finances
- **Hilarious News Headlines**: Stay entertained with over 150 humorous headlines that appear throughout gameplay
- **High Score System**: Compete to achieve the highest net worth

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Steps

1. Clone the repository:
   ```
   git clone https://github.com/phunterlau/yolo_term.git
   cd yolo_term
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   
   If no requirements.txt file exists, install the following packages:
   ```
   pip install colorama questionary
   ```

3. Run the game:
   ```
   python yolo_terminal.py
   ```

## How to Play

### Game Objective

Make as much money as possible in 40 days while maintaining your health and reputation.

### Game Mechanics

1. **Next Day**: Advances time by one day and updates stock prices
2. **Buy Stocks**: Purchase stocks to add to your portfolio
3. **Sell Stocks**: Sell stocks from your portfolio for profit (or loss)
4. **Visit Bank**: Deposit/withdraw money and manage loans
5. **Visit Hospital**: Restore health (costs money)
6. **Visit Student Loan Broker**: Repay your student loan debt
7. **Robinwood Trading App**: Increase your portfolio capacity
8. **Darkweb Hacking Facility**: Get information and small cash rewards
9. **View Leaderboard**: See the highest scores

### Tips for Success

- **Diversify Your Portfolio**: Don't put all your money in one stock
- **Watch for Patterns**: Some stocks follow predictable patterns
- **Monitor Your Health**: If your health drops to 0, the game ends
- **Manage Your Reputation**: Higher reputation can lead to better opportunities
- **Pay Attention to News**: Headlines can provide clues about market movements
- **Visit the Hospital**: Don't let your health get too low
- **Expand Your Portfolio Capacity**: Use the Trading App to increase how many stocks you can hold

### Game End Conditions

The game ends when:
1. You complete 40 days
2. Your health drops to 0

## Development

YOLO Terminal is built with Python and uses:
- **colorama**: For terminal colors and styling
- **questionary**: For interactive menu selection

The game architecture is modular with separate modules for:
- Player management
- Stock market simulation
- UI rendering
- Location-specific interactions
- Random events
- News headlines

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by Bloomberg Terminal and financial trading systems
- Created for entertainment and educational purposes only
- Special thanks to all contributors and testers
