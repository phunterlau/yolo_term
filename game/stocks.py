#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stocks module for Yolo Terminal game.
Handles stocks and trading system.
"""

import random
from typing import Dict, List, Optional, Tuple
import questionary
from colorama import Fore, Style

class Stock:
    """
    Stock class representing a type of stock in the game.
    """
    
    def __init__(self, stock_id: int, ticker: str, name: str, base_price: int, price_range: int):
        """
        Initialize a new stock type.
        
        Args:
            stock_id: Unique ID for the stock
            ticker: Ticker symbol for the stock
            name: Name of the stock
            base_price: Base price of the stock
            price_range: Range of price fluctuation
        """
        self.id = stock_id
        self.ticker = ticker
        self.name = name
        self.base_price = base_price
        self.price_range = price_range
        self.current_price = 0
        self.update_price()
    
    def update_price(self) -> int:
        """
        Update the price of the stock randomly within the price range.
        
        Returns:
            int: New price of the stock
        """
        self.current_price = self.base_price + random.randint(0, self.price_range)
        return self.current_price
    
    def multiply_price(self, factor: int) -> int:
        """
        Multiply the price of the stock by a factor.
        Used for events that affect stock prices.
        
        Args:
            factor: Multiplication factor
            
        Returns:
            int: New price of the stock
        """
        self.current_price *= factor
        return self.current_price
    
    def divide_price(self, factor: int) -> int:
        """
        Divide the price of the stock by a factor.
        Used for events that affect stock prices.
        
        Args:
            factor: Division factor
            
        Returns:
            int: New price of the stock
        """
        self.current_price //= factor
        return self.current_price


class StockManager:
    """
    StockManager class to manage all stocks and trading operations.
    """
    
    def __init__(self):
        """Initialize the stock manager with all available stock types."""
        # Initialize all stock types
        self.stock_types: Dict[int, Stock] = {
            0: Stock(0, "SNCI", "Super Nicron", 100, 350),
            1: Stock(1, "PITCOIN", "Pitcoin", 15000, 15000),
            2: Stock(2, "CATO", "Cato Coin", 5, 50),
            3: Stock(3, "NWDA", "nWidia", 1000, 2500),
            4: Stock(4, "SBY", "SBY500", 5000, 9000),
            5: Stock(5, "TZLA", "Tezla", 250, 600),
            6: Stock(6, "PTT", "PinTuoTuo", 750, 750),
            7: Stock(7, "PLTI", "Plantir", 65, 180)
        }
        
        # Available stocks in the market (some stocks may not be available)
        self.available_stocks: Dict[int, bool] = {stock_id: True for stock_id in self.stock_types}
    
    def update_prices(self, leave_out: int = 3) -> None:
        """
        Update prices of all stocks and randomly make some unavailable.
        
        Args:
            leave_out: Number of stock types to leave out of the market
        """
        # Make all stocks available first
        self.available_stocks = {stock_id: True for stock_id in self.stock_types}
        
        # Update prices
        for stock in self.stock_types.values():
            stock.update_price()
        
        # Randomly make some stocks unavailable
        for _ in range(leave_out):
            stock_id = random.choice(list(self.stock_types.keys()))
            self.available_stocks[stock_id] = False
    
    def get_available_stocks(self) -> List[Tuple[int, str, str, int]]:
        """
        Get list of available stocks in the market.
        
        Returns:
            List of tuples (stock_id, ticker, name, price) for available stocks
        """
        available = []
        for stock_id, available_flag in self.available_stocks.items():
            if available_flag:
                stock = self.stock_types[stock_id]
                available.append((stock_id, stock.ticker, stock.name, stock.current_price))
        return available
    
    def buy_stocks(self, player, ui, logger=None, day_manager=None) -> str:
        """
        Handle buying stocks from the market.
        
        Args:
            player: Player object
            ui: UI object for user interaction
            logger: GameLogger object for logging (optional)
            day_manager: DayManager object (optional)
        """
        # Get available stocks
        available_stocks = self.get_available_stocks()
        
        if not available_stocks:
            ui.show_message("There are no stocks available for trading right now.", player, self, day_manager)
            return "exit"
        
        # Create choices for the stocks menu
        choices = []
        for i, (stock_id, ticker, name, price) in enumerate(available_stocks, 1):
            choices.append(questionary.Choice(
                title=f"${ticker} ({name}) - Price: ${price}",
                value=(stock_id, ticker, name, price)
            ))
        
        # Add cancel option
        choices.append(questionary.Separator())
        choices.append(questionary.Choice(title='Cancel', value=None))
        
        # Ask player which stock to buy
        stock_choice = ui.custom_select(
            'Available stocks:',
            choices=choices,
            parent_menu_result=None
        )
        
        if not stock_choice:
            return "exit"
        
        try:
            stock_id, ticker, name, price = stock_choice
        except (ValueError, TypeError):
            # Handle case where stock_choice is not a tuple of 4 values
            return "exit"
        
        # Check if player has enough money
        if player.cash < price:
            ui.show_message("You don't have enough cash to buy even one share of this stock.")
            return "continue"
        
        # Calculate max amount player can buy
        max_buy = min(player.cash // price, player.portfolio_capacity - player.portfolio_used)
        if max_buy <= 0:
            ui.show_message("You don't have enough space in your trade book or cash to buy this stock.")
            return "continue"
        
        # Ask how many to buy
        amount = ui.get_input(f"How many shares of ${ticker} do you want to buy? (max {max_buy}): ", 
                             input_type=int, default=1, min_value=1, max_value=max_buy)
        
        # Confirm purchase
        if not ui.ask_yes_no(f"Confirm purchase of {amount} shares of ${ticker} for ${price * amount}?"):
            return "continue"
        
        # Process purchase
        player.cash -= price * amount
        player.add_to_portfolio(stock_id, ticker, name, amount, price)
        
        # Log the purchase if logger is provided
        if logger:
            logger.log_buy(player, stock_id, ticker, name, amount, price)
        
        ui.show_message(f"You bought {amount} shares of ${ticker} for ${price * amount}.", player, self, day_manager)
        return "continue"
    
    def sell_stocks(self, player, ui, logger=None, day_manager=None) -> str:
        """
        Handle selling stocks to the market.
        
        Args:
            player: Player object
            ui: UI object for user interaction
            logger: GameLogger object for logging (optional)
            day_manager: DayManager object (optional)
        """
        if not player.portfolio:
            ui.show_message("You don't have any stocks to sell.", player, self, day_manager)
            return "exit"
        
        # Create choices for the portfolio menu
        choices = []
        portfolio_list = []
        
        for i, (stock_id, stock_info) in enumerate(player.portfolio.items(), 1):
            portfolio_list.append((stock_id, stock_info["ticker"], stock_info["name"], stock_info["quantity"], stock_info["price"]))
            
            # Check if stock is available in market
            market_price = 0
            is_available = False
            for market_stock_id, ticker, name, price in self.get_available_stocks():
                if market_stock_id == stock_id:
                    market_price = price
                    is_available = True
                    break
            
            # Prepare information for display
            is_profitable = market_price > stock_info['price']
            
            # Create title without color codes for questionary
            title = f"${stock_info['ticker']} ({stock_info['name']}) - Qty: {stock_info['quantity']} - Bought: ${stock_info['price']}"
            if is_available:
                title += f" - Current: ${market_price}"
                profit = market_price - stock_info['price']
                if profit > 0:
                    title += f" (+${profit})"
                else:
                    title += f" (-${-profit})"
                
            # Print colored version to console for reference
            status_line = ""
            if is_available:
                status_line += f"{Fore.GREEN}${stock_info['ticker']} ({stock_info['name']}){Style.RESET_ALL} - Qty: {stock_info['quantity']} - "
                if is_profitable:
                    status_line += f"{Fore.YELLOW}Bought: ${stock_info['price']}{Style.RESET_ALL}"
                else:
                    status_line += f"{Fore.RED}Bought: ${stock_info['price']}{Style.RESET_ALL}"
                
                status_line += f" - Current: ${market_price}"
                if is_profitable:
                    status_line += f" ({Fore.GREEN}+${market_price - stock_info['price']}{Style.RESET_ALL})"
                else:
                    status_line += f" ({Fore.RED}-${stock_info['price'] - market_price}{Style.RESET_ALL})"
            else:
                status_line += f"${stock_info['ticker']} ({stock_info['name']}) - Qty: {stock_info['quantity']} - Bought: ${stock_info['price']}"
                status_line += " (Not tradable now)"
            
            print(f"{i}. {status_line}")
            
            choices.append(questionary.Choice(
                title=title,
                value=(stock_id, stock_info["ticker"], stock_info["name"], stock_info["quantity"], stock_info["price"])
            ))
        
        # Add cancel option
        choices.append(questionary.Separator())
        choices.append(questionary.Choice(title='Cancel', value=None))
        
        # Ask player which stock to sell
        stock_choice = ui.custom_select(
            'Your portfolio:',
            choices=choices,
            parent_menu_result=None
        )
        
        if not stock_choice:
            return "exit"
        
        try:
            stock_id, ticker, name, quantity, buy_price = stock_choice
        except (ValueError, TypeError):
            # Handle case where stock_choice is not a tuple of 5 values
            return "exit"
        
        # Check if the stock is available in the market
        market_price = 0
        is_available = False
        for market_stock_id, market_ticker, market_name, price in self.get_available_stocks():
            if market_stock_id == stock_id:
                market_price = price
                is_available = True
                break
        
        if not is_available:
            ui.show_message(f"${ticker} is not currently tradable in the market.", player, self, day_manager)
            return "continue"
        
        # Ask how many to sell
        amount = ui.get_input(f"How many shares of ${ticker} do you want to sell? (max {quantity}): ", 
                             input_type=int, default=1, min_value=1, max_value=quantity)
        
        # Confirm sale
        profit = (market_price - buy_price) * amount
        profit_str = f"Profit: ${profit}" if profit >= 0 else f"Loss: ${-profit}"
        
        if not ui.ask_yes_no(f"Confirm sale of {amount} shares of ${ticker} at ${market_price} each? {profit_str}"):
            return "continue"
        
        # Process sale
        player.cash += market_price * amount
        player.remove_from_portfolio(stock_id, amount)
        
        # Log the sale if logger is provided
        if logger:
            logger.log_sell(player, stock_id, ticker, name, amount, market_price, buy_price)
        
        ui.show_message(f"You sold {amount} shares of ${ticker} for ${market_price * amount}.", player, self, day_manager)
        
        return "continue"
    
    def sell_all_stocks(self, player, ui, logger=None, day_manager=None) -> None:
        """
        Sell all stocks in player's portfolio at the end of the game.
        
        Args:
            player: Player object
            ui: UI object for user interaction
            logger: GameLogger object for logging (optional)
            day_manager: DayManager object (optional)
        """
        if not player.portfolio:
            return
        
        ui.show_message("Game over. The system will automatically sell all your remaining stocks:", player, self, day_manager)
        
        total_earned = 0
        for stock_id, stock_info in list(player.portfolio.items()):
            ticker = stock_info["ticker"]
            name = stock_info["name"]
            quantity = stock_info["quantity"]
            
            # Find market price
            market_price = 0
            is_available = False
            for market_stock_id, market_ticker, market_name, price in self.get_available_stocks():
                if market_stock_id == stock_id:
                    market_price = price
                    is_available = True
                    break
            
            # If not available in market, use buy price
            if not is_available:
                market_price = stock_info["price"]
                ui.show_message(f"${ticker} is not currently tradable, selling at purchase price.", player, self, day_manager)
            
            # Sell stocks
            earned = market_price * quantity
            total_earned += earned
            
            # Log the sale if logger is provided
            if logger:
                logger.log_sell(player, stock_id, ticker, name, quantity, market_price, stock_info["price"])
            
            ui.show_message(f"Sold {quantity} shares of ${ticker} for ${earned}", player, self, day_manager)
            player.remove_from_portfolio(stock_id, quantity)
        
        player.cash += total_earned
        ui.show_message(f"Total earned: ${total_earned}", player, self, day_manager)
