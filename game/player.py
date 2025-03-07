#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Player module for Yolo Terminal game.
Handles player stats, portfolio, and other attributes.
"""

from typing import Dict, List, Optional

class Player:
    """
    Player class representing the game player.
    Manages player stats, portfolio, and other attributes.
    """
    
    def __init__(self, name: str = "Trader"):
        """
        Initialize a new player.
        
        Args:
            name: Player's name, defaults to "Trader"
        """
        # Basic player info
        self.name = name
        self.days_left = 40
        
        # Player stats
        self.cash = 2000  # Initial cash
        self.debt = 5000  # Initial student loan debt
        self.bank_savings = 0  # Initial bank savings
        self.health = 100  # Initial health
        self.fame = 100  # Initial reputation
        
        # Portfolio
        self.portfolio: Dict[int, Dict[str, any]] = {}  # Stocks in portfolio
        self.portfolio_capacity = 100  # Max trade book size
        self.portfolio_used = 0  # Current used capacity
        
        # Special flags
        self.darkweb_visits = 0  # Number of darkweb visits
        self.sound_enabled = True  # Sound enabled flag
        self.hacker_actions_enabled = False  # Hacker actions enabled flag
    
    def get_net_worth(self) -> int:
        """
        Calculate player's net worth.
        
        Returns:
            int: Player's net worth (cash + bank_savings - debt)
        """
        return self.cash + self.bank_savings - self.debt
    
    def has_portfolio_space(self, amount: int = 1) -> bool:
        """
        Check if player has enough portfolio space.
        
        Args:
            amount: Amount of space needed
            
        Returns:
            bool: True if player has enough space, False otherwise
        """
        return self.portfolio_used + amount <= self.portfolio_capacity
    
    def add_to_portfolio(self, stock_id: int, ticker: str, name: str, quantity: int, price: int) -> bool:
        """
        Add stocks to player's portfolio.
        
        Args:
            stock_id: ID of the stock
            ticker: Ticker symbol of the stock
            name: Name of the stock
            quantity: Quantity to add
            price: Price per share
            
        Returns:
            bool: True if stocks were added successfully, False otherwise
        """
        if not self.has_portfolio_space(quantity):
            return False
        
        # If stock already in portfolio, update quantity and average price
        if stock_id in self.portfolio:
            old_quantity = self.portfolio[stock_id]["quantity"]
            old_price = self.portfolio[stock_id]["price"]
            
            # Calculate new average price
            new_price = int((old_price * old_quantity + price * quantity) / (old_quantity + quantity))
            
            # Update portfolio
            self.portfolio[stock_id]["quantity"] += quantity
            self.portfolio[stock_id]["price"] = new_price
        else:
            # Add new stock to portfolio
            self.portfolio[stock_id] = {
                "ticker": ticker,
                "name": name,
                "quantity": quantity,
                "price": price
            }
        
        # Update portfolio used
        self.portfolio_used += quantity
        return True
    
    def remove_from_portfolio(self, stock_id: int, quantity: int) -> bool:
        """
        Remove stocks from player's portfolio.
        
        Args:
            stock_id: ID of the stock
            quantity: Quantity to remove
            
        Returns:
            bool: True if stocks were removed successfully, False otherwise
        """
        if stock_id not in self.portfolio or self.portfolio[stock_id]["quantity"] < quantity:
            return False
        
        # Update portfolio
        self.portfolio[stock_id]["quantity"] -= quantity
        
        # If quantity is 0, remove stock from portfolio
        if self.portfolio[stock_id]["quantity"] == 0:
            del self.portfolio[stock_id]
        
        # Update portfolio used
        self.portfolio_used -= quantity
        return True
