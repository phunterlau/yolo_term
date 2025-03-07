#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI module for Yolo Terminal game.
Handles the command-line interface for the game with a Bloomberg Terminal style.
"""

import os
import sys
import time
from typing import Dict, List, Optional, Tuple, Any, Union, Callable
import questionary
from colorama import Fore, Style, Back, init

# Initialize colorama
init(autoreset=True)

class UI:
    """
    UI class to handle the command-line interface for the game.
    """
    
    def __init__(self):
        """Initialize the UI."""
        # Define styles for questionary (can be customized)
        self.style = questionary.Style([
            ('question', 'bold'),
            ('answer', ''), # Hide the answer text
            ('pointer', 'fg:cyan bold'),
            ('highlighted', 'fg:cyan bold'),
            ('selected', 'fg:cyan bold'),
        ])
        
        # Store the current menu level for navigation
        self.menu_level = 0
        # Store the parent menu result for back navigation
        self.parent_menu_result = None
        
        # Bloomberg Terminal style colors - custom darker blue background
        # Define a custom darker blue background using ANSI escape codes
        # Standard Back.BLUE is too light, so we're using a custom darker blue
        self.header_bg = "\033[44;1m"  # Darker blue background
        self.header_fg = Fore.WHITE
        self.positive = Fore.GREEN
        self.negative = Fore.RED
        self.highlight = Fore.YELLOW
        self.title = Fore.CYAN + Style.BRIGHT
    
    def display_width(self, s):
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
    
    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_welcome(self, clear_after=True) -> None:
        """
        Show the welcome message.
        
        Args:
            clear_after: Whether to clear the screen after showing the welcome message
        """
        self.clear_screen()
        
        # Display "YOLO TERMINAL" on top of the board edge
        title = "YOLO TERMINAL"
        title_padding = (80 - len(title)) // 2
        print(" " * title_padding + f"{self.title}{title}{Style.RESET_ALL}")
        
        # Bloomberg Terminal style UI - fixed width 80 chars (78 inside borders)
        print(f"{self.header_bg}{self.header_fg}╔" + "═" * 78 + f"╗{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}╠" + "═" * 78 + f"╣{Style.RESET_ALL}")
        print(f"{self.header_bg}{self.header_fg}║" + " " * 78 + f"║{Style.RESET_ALL}")
        
        # Format welcome message with fixed width
        welcome_text = "Welcome to Yolo Terminal! This is a game about stock trading and making money."
        welcome_padding = 78 - len(welcome_text) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {welcome_text}" + " " * welcome_padding + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}║" + " " * 78 + f"║{Style.RESET_ALL}")
        
        # Format days message with fixed width
        days_text = "You have 40 days to trade stocks and make as much money as possible."
        days_padding = 78 - len(days_text) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {days_text}" + " " * days_padding + f"║{Style.RESET_ALL}")
        
        # Format health message with fixed width
        health_text = "Watch your health and reputation, as they will affect your gameplay."
        health_padding = 78 - len(health_text) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {health_text}" + " " * health_padding + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}║" + " " * 78 + f"║{Style.RESET_ALL}")
        
        # Format good luck message with fixed width
        luck_text = "Good luck!"
        luck_padding = 78 - len(luck_text) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {luck_text}" + " " * luck_padding + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}║" + " " * 78 + f"║{Style.RESET_ALL}")
        print(f"{self.header_bg}{self.header_fg}╚" + "═" * 78 + f"╝{Style.RESET_ALL}")
        input("\nPress Enter to continue...")
        
        if clear_after:
            self.clear_screen()
    
    def show_story(self, player=None, stock_manager=None, day_manager=None) -> None:
        """Show the game story."""
        self.clear_screen()
        
        # Show status board if player is provided
        if player:
            self.show_status(player, stock_manager, day_manager)
        
        # Bloomberg Terminal style UI - fixed width 80 chars (78 inside borders)
        print(f"{self.header_bg}{self.header_fg}╔" + "═" * 78 + f"╗{Style.RESET_ALL}")
        
        title = "BACKSTORY"
        title_padding = (78 - len(title)) // 2
        print(f"{self.header_bg}{self.header_fg}║" + " " * title_padding + title + " " * (78 - title_padding - len(title)) + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}╠" + "═" * 78 + f"╣{Style.RESET_ALL}")
        print(f"{self.header_bg}{self.header_fg}║" + " " * 78 + f"║{Style.RESET_ALL}")
        
        # Format backstory messages with fixed width
        debt_text = "You're a college student with $2000 in cash and $5000 in student loan debt."
        debt_padding = 78 - len(debt_text) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {debt_text}" + " " * debt_padding + f"║{Style.RESET_ALL}")
        
        trading_text = "You've decided to try your hand at stock trading to pay off your debt and"
        trading_padding = 78 - len(trading_text) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {trading_text}" + " " * trading_padding + f"║{Style.RESET_ALL}")
        
        money_text = "make as much money as possible in 40 days."
        money_padding = 78 - len(money_text) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {money_text}" + " " * money_padding + f"║{Style.RESET_ALL}")
        
        stocks_text = "Each day, you'll have the opportunity to buy and sell various stocks,"
        stocks_padding = 78 - len(stocks_text) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {stocks_text}" + " " * stocks_padding + f"║{Style.RESET_ALL}")
        
        market_text = "but be careful - the market is volatile and full of unexpected events."
        market_padding = 78 - len(market_text) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {market_text}" + " " * market_padding + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}║" + " " * 78 + f"║{Style.RESET_ALL}")
        
        survive_text = "Can you survive in this high-stakes world and come out ahead?"
        survive_padding = 78 - len(survive_text) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {survive_text}" + " " * survive_padding + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}║" + " " * 78 + f"║{Style.RESET_ALL}")
        print(f"{self.header_bg}{self.header_fg}╚" + "═" * 78 + f"╝{Style.RESET_ALL}")
        input("\nPress Enter to continue...")
        self.clear_screen()
        if player:
            self.show_status(player, stock_manager, day_manager)
    
    def show_help(self, player=None, stock_manager=None, day_manager=None) -> None:
        """Show the help information."""
        self.clear_screen()
        
        # Show status board if player is provided
        if player:
            self.show_status(player, stock_manager, day_manager)
        
        # Bloomberg Terminal style UI - fixed width 80 chars (78 inside borders)
        print(f"{self.header_bg}{self.header_fg}╔" + "═" * 78 + f"╗{Style.RESET_ALL}")
        
        title = "HELP"
        title_padding = (78 - len(title)) // 2
        print(f"{self.header_bg}{self.header_fg}║" + " " * title_padding + title + " " * (78 - title_padding - len(title)) + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}╠" + "═" * 78 + f"╣{Style.RESET_ALL}")
        print(f"{self.header_bg}{self.header_fg}║" + " " * 78 + f"║{Style.RESET_ALL}")
        
        # Format help messages with fixed width
        objective_title = "Game Objective:"
        objective_padding = 78 - len(objective_title) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {objective_title}" + " " * objective_padding + f"║{Style.RESET_ALL}")
        
        objective_text = "  Make as much money as possible in 40 days while maintaining health and rep."
        objective_text_padding = 78 - len(objective_text) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {objective_text}" + " " * objective_text_padding + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}║" + " " * 78 + f"║{Style.RESET_ALL}")
        
        mechanics_title = "Game Mechanics:"
        mechanics_padding = 78 - len(mechanics_title) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {mechanics_title}" + " " * mechanics_padding + f"║{Style.RESET_ALL}")
        
        # Format each mechanic with fixed width
        mechanics = [
            "  1. Each 'Next Day' action advances time by one day",
            "  2. You can buy and sell stocks to make money",
            "  3. Stock prices fluctuate randomly each day",
            "  4. Random events may affect your health, reputation, and finances",
            "  5. You can deposit/withdraw money and repay loans at the Bank",
            "  6. Visit the Hospital to restore health (costs money)",
            "  7. Use Robinwood Trading App to increase your trade book capacity",
            "  8. Visit the Darkweb for information and small cash rewards",
            "  9. Visit your Student Loan Broker to repay debt"
        ]
        
        for mechanic in mechanics:
            mechanic_padding = 78 - len(mechanic) - 2  # -2 for "║ "
            print(f"{self.header_bg}{self.header_fg}║ {mechanic}" + " " * mechanic_padding + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}║" + " " * 78 + f"║{Style.RESET_ALL}")
        
        end_title = "Game End Conditions:"
        end_padding = 78 - len(end_title) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {end_title}" + " " * end_padding + f"║{Style.RESET_ALL}")
        
        end1 = "  1. 40 days are over"
        end1_padding = 78 - len(end1) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {end1}" + " " * end1_padding + f"║{Style.RESET_ALL}")
        
        end2 = "  2. Health drops to 0"
        end2_padding = 78 - len(end2) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {end2}" + " " * end2_padding + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}║" + " " * 78 + f"║{Style.RESET_ALL}")
        
        luck_text = "Good luck!"
        luck_padding = 78 - len(luck_text) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {luck_text}" + " " * luck_padding + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}║" + " " * 78 + f"║{Style.RESET_ALL}")
        print(f"{self.header_bg}{self.header_fg}╚" + "═" * 78 + f"╝{Style.RESET_ALL}")
        input("\nPress Enter to continue...")
        self.clear_screen()
        if player:
            self.show_status(player, stock_manager, day_manager)
    
    def show_status(self, player, stock_manager, day_manager=None) -> None:
        """
        Show the player's status.
        
        Args:
            player: Player object
            stock_manager: StockManager object
            day_manager: DayManager object (optional)
        """
        # Import headlines module here to avoid circular imports
        from game.headlines import get_random_headline
        # Get current day description if day_manager is provided
        current_day = ""
        if day_manager:
            current_day = day_manager.get_day_description(player)
        
        # Display "YOLO TERMINAL" on top of the board edge
        title = "YOLO TERMINAL"
        title_padding = (80 - len(title)) // 2
        print(" " * title_padding + f"{self.title}{title}{Style.RESET_ALL}")
        
        # Bloomberg Terminal style UI
        print(f"{self.header_bg}{self.header_fg}╔" + "═" * 78 + f"╗{Style.RESET_ALL}")
        
        # Status line 1 - ensure fixed width
        # Use stronger color for days left if less than 10
        days_color = self.negative if player.days_left < 10 else self.header_fg
        
        status1_text = f"Trader: {player.name}   Days Left: {days_color}{player.days_left}/40{self.header_fg}   {current_day}"
        padding1 = 76 - self.display_width(status1_text)  # 76 = 78 - 2 (for "║ ")
        if padding1 < 0:  # Handle overflow by truncating
            status1_text = status1_text[:76 - 3] + "..."
            padding1 = 0
        print(f"{self.header_bg}{self.header_fg}║ {status1_text}" + " " * padding1 + f"║{Style.RESET_ALL}")
        
        # Status line 2 - ensure fixed width
        # Color debt in red if greater than cash, otherwise green
        debt_color = self.negative if player.debt > player.cash else self.positive
        
        status2_text = f"Cash: ${player.cash}   Bank: ${player.bank_savings}   Debt: {debt_color}${player.debt}{self.header_fg}"
        padding2 = 76 - self.display_width(status2_text)  # 76 = 78 - 2 (for "║ ")
        if padding2 < 0:  # Handle overflow by truncating
            status2_text = status2_text[:76 - 3] + "..."
            padding2 = 0
        print(f"{self.header_bg}{self.header_fg}║ {status2_text}" + " " * padding2 + f"║{Style.RESET_ALL}")
        
        # Status line 3 - ensure fixed width
        health_color = self.positive if player.health > 50 else (self.highlight if player.health > 25 else self.negative)
        fame_color = self.positive if player.fame > 50 else (self.highlight if player.fame > 25 else self.negative)
        portfolio_color = self.positive if player.portfolio_used < player.portfolio_capacity * 0.8 else (self.highlight if player.portfolio_used < player.portfolio_capacity * 0.95 else self.negative)
        
        status3_text = f"Health: {health_color}{player.health}/100{self.header_fg}   Rep: {fame_color}{player.fame}/100{self.header_fg}   Portfolio: {portfolio_color}{player.portfolio_used}/{player.portfolio_capacity}{self.header_fg}"
        padding3 = 76 - self.display_width(status3_text)  # 76 = 78 - 2 (for "║ ")
        if padding3 < 0:  # Handle overflow by truncating
            # This is more complex due to color codes, so we'll just ensure the line fits
            plain_text = f"Health: {player.health}/100   Rep: {player.fame}/100   Portfolio: {player.portfolio_used}/{player.portfolio_capacity}"
            if len(plain_text) > 76:
                plain_text = plain_text[:76 - 3] + "..."
            # Recreate the colored version but ensure it fits
            status3_text = f"Health: {health_color}{player.health}/100{self.header_fg}   Rep: {fame_color}{player.fame}/100{self.header_fg}   Portfolio: {portfolio_color}{player.portfolio_used}/{player.portfolio_capacity}{self.header_fg}"
            padding3 = 76 - self.display_width(status3_text)
            if padding3 < 0:
                padding3 = 0
        print(f"{self.header_bg}{self.header_fg}║ {status3_text}" + " " * padding3 + f"║{Style.RESET_ALL}")
        
        if player.portfolio:
            print(f"{self.header_bg}{self.header_fg}║" + " " * 78 + f"║{Style.RESET_ALL}")
            # Portfolio header
            portfolio_title = "Portfolio:"
            portfolio_padding = 78 - len(portfolio_title) - 2  # -2 for "║ "
            print(f"{self.header_bg}{self.header_fg}║ {portfolio_title}" + " " * portfolio_padding + f"║{Style.RESET_ALL}")
            
            for stock_id, stock_info in player.portfolio.items():
                # Check if stock is available in market
                market_price = 0
                for market_stock_id, ticker, name, price in stock_manager.get_available_stocks():
                    if market_stock_id == stock_id:
                        market_price = price
                        break
                
                # Color stock ticker based on availability and type
                if stock_info['ticker'] in ["CATO", "PITCOIN"]:
                    # Cryptocurrency with bold yellow
                    if market_price > 0:
                        ticker_display = f"{self.highlight + Style.BRIGHT}${stock_info['ticker']}{Style.RESET_ALL + self.header_fg + self.header_bg}"
                    else:
                        ticker_display = f"{self.highlight}${stock_info['ticker']}{self.header_fg}"
                else:
                    # Regular stock with bold green
                    if market_price > 0:
                        ticker_display = f"{self.positive + Style.BRIGHT}${stock_info['ticker']}{Style.RESET_ALL + self.header_fg + self.header_bg}"
                    else:
                        ticker_display = f"{self.positive}${stock_info['ticker']}{self.header_fg}"
                
                # Color price based on profitability
                if market_price > stock_info['price']:
                    price_str = f"{self.positive}Cost basis: ${stock_info['price']}{self.header_fg}"
                elif market_price > 0:
                    # Use orange (yellow in this case) instead of red for lower price
                    price_str = f"{self.highlight}Cost basis: ${stock_info['price']}{self.header_fg}"
                else:
                    price_str = f"Cost basis: ${stock_info['price']}"
                
                # Format portfolio item with fixed width
                item_text = f"{ticker_display} ({stock_info['name']}) - Qty: {stock_info['quantity']} - {price_str}"
                
                # Handle overflow by truncating if necessary
                if self.display_width(item_text) > 75:  # 75 = 78 - 3 (for "║ ")
                    # This is complex due to color codes, so we'll just ensure it fits
                    plain_text = f"${stock_info['ticker']} ({stock_info['name']}) - Qty: {stock_info['quantity']} - Bought: ${stock_info['price']}"
                    if len(plain_text) > 75:
                        plain_text = plain_text[:75 - 3] + "..."
                    # Recreate the colored version but ensure it fits
                    item_text = f"{ticker_display} ({stock_info['name']}) - Qty: {stock_info['quantity']} - {price_str}"
                
                # Add the portfolio item with proper padding
                full_item_text = f"  {item_text}"
                padding = 76 - self.display_width(full_item_text)  # 76 = 78 - 2 (for "║ ")
                if padding < 0:
                    padding = 0
                
                print(f"{self.header_bg}{self.header_fg}║ {full_item_text}" + " " * padding + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}╚" + "═" * 78 + f"╝{Style.RESET_ALL}")
        
        # Display a random headline with news agency acronym right after the status board
        headline, agency, agency_color = get_random_headline()
        headline_text = f"[{agency_color}{agency}{Style.RESET_ALL}] {headline}"
        print(headline_text)
    
    def show_available_stocks(self, stock_manager, player=None, day_manager=None) -> None:
        """
        Show available stocks at the current day.
        
        Args:
            stock_manager: StockManager object
            player: Player object (optional)
            day_manager: DayManager object (optional)
        """
        self.clear_screen()
        
        # Show status board if player is provided
        if player:
            self.show_status(player, stock_manager, day_manager)
            
        available_stocks = stock_manager.get_available_stocks()
        
        # Bloomberg Terminal style UI - fixed width 80 chars (78 inside borders)
        print(f"{self.header_bg}{self.header_fg}╔" + "═" * 78 + f"╗{Style.RESET_ALL}")
        
        title = "Available Stocks:"
        title_padding = 78 - len(title) - 2  # -2 for "║ "
        print(f"{self.header_bg}{self.header_fg}║ {title}" + " " * title_padding + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}╠" + "═" * 78 + f"╣{Style.RESET_ALL}")
        
        if not available_stocks:
            no_stocks_text = "No stocks available for trading today."
            no_stocks_padding = 78 - len(no_stocks_text) - 2  # -2 for "║ "
            print(f"{self.header_bg}{self.header_fg}║ {no_stocks_text}" + " " * no_stocks_padding + f"║{Style.RESET_ALL}")
        else:
            for i, (stock_id, ticker, name, price) in enumerate(available_stocks, 1):
                # Format stock item with fixed width
                # Use different bold color for cryptocurrencies
                if ticker in ["CATO", "PITCOIN"]:
                    ticker_display = f"{self.highlight + Style.BRIGHT}${ticker}{Style.RESET_ALL + self.header_fg + self.header_bg}"
                else:
                    ticker_display = f"{self.positive + Style.BRIGHT}${ticker}{Style.RESET_ALL + self.header_fg + self.header_bg}"
                
                item_text = f"{i}. {ticker_display} ({name}) - Price: ${price}"
                
                # Handle overflow by truncating if necessary
                if self.display_width(item_text) > 76:  # 76 = 78 - 2 (for "║ ")
                    # This is complex due to color codes, so we'll just ensure it fits
                    plain_text = f"{i}. ${ticker} ({name}) - Price: ${price}"
                    if len(plain_text) > 76:
                        plain_text = plain_text[:76 - 3] + "..."
                    # Recreate the colored version but ensure it fits
                    if ticker in ["CATO", "PITCOIN"]:
                        ticker_display = f"{self.highlight + Style.BRIGHT}${ticker}{Style.RESET_ALL + self.header_fg + self.header_bg}"
                    else:
                        ticker_display = f"{self.positive + Style.BRIGHT}${ticker}{Style.RESET_ALL + self.header_fg + self.header_bg}"
                    item_text = f"{i}. {ticker_display} ({name}) - Price: ${price}"
                
                # Add the stock item with proper padding
                padding = 76 - self.display_width(item_text)  # 76 = 78 - 2 (for "║ ")
                if padding < 0:
                    padding = 0
                print(f"{self.header_bg}{self.header_fg}║ {item_text}" + " " * padding + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}╚" + "═" * 78 + f"╝{Style.RESET_ALL}")
        input("\nPress Enter to continue...")
        self.clear_screen()
        if player:
            self.show_status(player, stock_manager, day_manager)
    
    def show_news_reports(self, news_reports: List[str], player=None, stock_manager=None, day_manager=None) -> None:
        """
        Show news reports to the player.
        
        Args:
            news_reports: List of news report messages
            player: Player object (optional)
            stock_manager: StockManager object (optional)
            day_manager: DayManager object (optional)
        """
        if not news_reports:
            return
        
        self.clear_screen()
        
        # Show status board if player is provided
        if player:
            self.show_status(player, stock_manager, day_manager)
        
        # Bloomberg Terminal style UI with darker background for NEWS FEED - fixed width 80 chars (78 inside borders)
        print(f"{self.header_bg}{self.header_fg}╔" + "═" * 78 + f"╗{Style.RESET_ALL}")
        
        title = "NEWS FEED"
        title_padding_left = (78 - len(title)) // 2
        title_padding_right = 78 - len(title) - title_padding_left
        print(f"{Back.BLACK}{self.header_fg}║" + " " * title_padding_left + title + " " * title_padding_right + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}╠" + "═" * 78 + f"╣{Style.RESET_ALL}")
        
        for report in news_reports:
            # Split long reports into multiple lines with fixed width
            words = report.split()
            lines = []
            current_line = ""
            
            for word in words:
                # Check if adding this word would exceed the line width
                if len(current_line) + len(word) + 1 <= 76:  # +1 for space, 76 = 78 - 2 (for "║ ")
                    if current_line:
                        current_line += " " + word
                    else:
                        current_line = word
                else:
                    lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            # Print each line with proper padding
            for line in lines:
                # Ensure line fits within the fixed width
                if len(line) > 76:  # 76 = 78 - 2 (for "║ ")
                    line = line[:76 - 3] + "..."
                
                padding = 78 - len(line) - 2  # -2 for the "║ " prefix
                print(f"{self.header_bg}{self.header_fg}║ {line}" + " " * padding + f"║{Style.RESET_ALL}")
            
            # Add a blank line between reports
            if report != news_reports[-1]:
                print(f"{self.header_bg}{self.header_fg}║" + " " * 78 + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}╚" + "═" * 78 + f"╝{Style.RESET_ALL}")
        input("\nPress Enter to continue...")
    
    def custom_select(self, message, choices, style=None, is_main_menu=False, parent_menu_result=None):
        """
        Custom select function with keyboard navigation.
        
        Args:
            message: The message to display
            choices: List of questionary.Choice objects
            style: The questionary style to use
            is_main_menu: Whether this is the main menu
            parent_menu_result: The result to return when left arrow is pressed
            
        Returns:
            The selected value or parent_menu_result if left arrow is pressed
        """
        import questionary
        from prompt_toolkit.formatted_text import ANSI
        
        # Set menu level
        if is_main_menu:
            self.menu_level = 0
            self.parent_menu_result = None
        
        # Create a select prompt with default settings
        # We can't easily add custom key bindings in questionary 2.1.0
        # So we'll just use the default behavior
        
        # Create a custom style that hides the answer line
        from prompt_toolkit.styles import Style as PTKStyle
        custom_style = PTKStyle.from_dict({
            'answer': 'hidden',  # Hide the answer text completely
        })
        
        select = questionary.select(
            message=message,
            choices=choices,
            style=style or self.style,
            use_indicator=False,  # Don't use the circle indicator
            use_arrow_keys=True,
            use_shortcuts=True,
            show_selected=True,
            qmark="",  # Remove the question mark
            instruction="",  # Remove the instruction text
        )
        
        # Monkey patch the select prompt to hide the answer line
        if hasattr(select, '_question') and hasattr(select._question, 'application'):
            select._question.application.style = custom_style
        
        # Run the select prompt
        result = select.ask()
        
        return result
    
    def show_main_menu(self, player) -> str:
        """
        Show the main menu and get player's choice.
        
        Args:
            player: Player object
            
        Returns:
            str: Player's choice
        """
        choices = [
            questionary.Choice(title='Next Day', value='next_day'),
            questionary.Choice(title='Buy Stocks', value='buy'),
            questionary.Choice(title='Sell Stocks', value='sell'),
            questionary.Choice(title='Visit Bank', value='bank'),
            questionary.Choice(title='Visit Hospital', value='hospital'),
            questionary.Choice(title='Visit Student Loan Broker', value='broker'),
            questionary.Choice(title='Robinwood Trading App', value='trading_app'),
            questionary.Choice(title='Darkweb Hacking Facility', value='darkweb'),
            questionary.Choice(title='View Leaderboard', value='high_scores'),
            questionary.Choice(title='Help', value='help'),
            questionary.Separator(),
            questionary.Choice(title='Quit Game', value='quit')
        ]
        
        result = self.custom_select(
            "Main Menu:",
            choices=choices,
            is_main_menu=True
        )
        
        return result if result else 'quit'
    
    def show_message(self, message: str, player=None, stock_manager=None, day_manager=None) -> None:
        """
        Show a message to the player.
        
        Args:
            message: Message to show
            player: Player object (optional)
            stock_manager: StockManager object (optional)
            day_manager: DayManager object (optional)
        """
        self.clear_screen()
        
        # Show status board if player is provided
        if player:
            self.show_status(player, stock_manager, day_manager)
        
        # Bloomberg Terminal style UI - fixed width 80 chars (78 inside borders)
        print(f"{self.header_bg}{self.header_fg}╔" + "═" * 78 + f"╗{Style.RESET_ALL}")
        
        # Split long messages into multiple lines with fixed width
        words = message.split()
        lines = []
        current_line = ""
        
        for word in words:
            # Check if adding this word would exceed the line width
            if len(current_line) + len(word) + 1 <= 76:  # +1 for space, 76 = 78 - 2 (for "║ ")
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Print each line with proper padding
        for line in lines:
            # Ensure line fits within the fixed width
            if len(line) > 76:  # 76 = 78 - 2 (for "║ ")
                line = line[:76 - 3] + "..."
            
            padding = 78 - len(line) - 2  # -2 for the "║ " prefix
            print(f"{self.header_bg}{self.header_fg}║ {line}" + " " * padding + f"║{Style.RESET_ALL}")
        
        print(f"{self.header_bg}{self.header_fg}╚" + "═" * 78 + f"╝{Style.RESET_ALL}")
        input("\nPress Enter to continue...")
        self.clear_screen()
        if player:
            self.show_status(player, stock_manager, day_manager)
    
    def get_input(self, prompt: str, input_type: Callable = str, default: Any = None, 
                 min_value: Optional[Union[int, float]] = None, 
                 max_value: Optional[Union[int, float]] = None) -> Any:
        """
        Get input from the player with validation.
        
        Args:
            prompt: Prompt to show
            input_type: Type to convert input to
            default: Default value if input is empty
            min_value: Minimum value for numeric input
            max_value: Maximum value for numeric input
            
        Returns:
            Validated input value
        """
        # For numeric input with min/max values
        if input_type in (int, float):
            # Create validation message
            validate_message = ""
            if min_value is not None and max_value is not None:
                validate_message = f" ({min_value}-{max_value})"
            elif min_value is not None:
                validate_message = f" (min {min_value})"
            elif max_value is not None:
                validate_message = f" (max {max_value})"
            
            # Define validation function
            def validate_number(text):
                if not text and default is not None:
                    return True
                
                try:
                    value = input_type(text)
                    
                    if min_value is not None and value < min_value:
                        return f"Input must be greater than or equal to {min_value}"
                    
                    if max_value is not None and value > max_value:
                        return f"Input must be less than or equal to {max_value}"
                    
                    return True
                
                except ValueError:
                    return f"Please enter a valid {input_type.__name__}"
            
            result = questionary.text(
                f"{prompt}{validate_message}",
                default=str(default) if default is not None else "",
                validate=validate_number,
                style=self.style
            ).ask()
            
            # Convert to the correct type
            if result is not None:
                try:
                    return input_type(result)
                except ValueError:
                    return default
            return default
        
        # For string or other input types
        result = questionary.text(
            prompt,
            default=default if default is not None else "",
            style=self.style
        ).ask()
        
        # Convert to the correct type if needed
        if result is not None and input_type is not str:
            try:
                return input_type(result)
            except ValueError:
                return default
        
        return result
    
    def ask_yes_no(self, prompt: str) -> bool:
        """
        Ask a yes/no question.
        
        Args:
            prompt: Question to ask
            
        Returns:
            bool: True if yes, False if no
        """
        result = questionary.confirm(
            prompt,
            default=False,
            style=self.style
        ).ask()
        
        return result if result is not None else False
    
    def show_net_worth_chart(self, net_worth_history: List[Dict[str, Any]]) -> None:
        """
        Display an ASCII art line chart of the player's net worth over time.
        
        Args:
            net_worth_history: List of daily stats dictionaries
        """
        from game.chart import Chart
        
        chart = Chart()
        chart.show_net_worth_chart(net_worth_history, self.clear_screen)
