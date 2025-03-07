#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logger module for Yolo Terminal game.
Handles logging game events to a file and tracking player stats over time.
"""

import os
import logging
import datetime
import json
from typing import Dict, Any, Optional, List

class GameLogger:
    """
    GameLogger class to handle logging game events and tracking player stats over time.
    """
    
    def __init__(self, player_name: str = "Unknown"):
        """
        Initialize the logger.
        
        Args:
            player_name: Name of the player for the log file name
        """
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Generate timestamp for log file name
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"logs/{timestamp}_{player_name}.log"
        
        # Configure logger
        self.logger = logging.getLogger("yolo_terminal")
        self.logger.setLevel(logging.INFO)
        
        # Create file handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(file_handler)
        
        # Store the log file path
        self.log_file = log_file
        
        # Initialize daily stats tracking
        self.daily_stats = []
        self.actions_log = []
        
        # Log game start
        self.log_event("GAME_START", {"player_name": player_name})
    
    def log_event(self, event_type: str, data: Dict[str, Any] = None) -> None:
        """
        Log a game event.
        
        Args:
            event_type: Type of event (e.g., "NEXT_DAY", "BUY", "SELL")
            data: Dictionary of event data
        """
        if data is None:
            data = {}
        
        # Format the log message
        message = f"{event_type}: {data}"
        
        # Log the event
        self.logger.info(message)
        
        # Track action in actions log
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        action_entry = {
            "timestamp": current_time,
            "event_type": event_type,
            "data": data
        }
        self.actions_log.append(action_entry)
    
    def log_player_status(self, player, stock_manager=None) -> None:
        """
        Log the player's current status.
        
        Args:
            player: Player object
            stock_manager: StockManager object (optional)
        """
        # Calculate net worth and portfolio value if stock_manager is provided
        net_worth = player.cash + player.bank_savings - player.debt
        portfolio_value = 0
        
        if stock_manager and player.portfolio:
            for stock_id, stock_info in player.portfolio.items():
                # Find current market price
                for market_stock_id, _, _, price in stock_manager.get_available_stocks():
                    if market_stock_id == stock_id:
                        portfolio_value += price * stock_info['quantity']
                        break
        
        total_assets = net_worth + portfolio_value
        
        # Extract player data
        player_data = {
            "name": player.name,
            "cash": player.cash,
            "bank_savings": player.bank_savings,
            "debt": player.debt,
            "health": player.health,
            "fame": player.fame,
            "days_left": player.days_left,
            "portfolio_used": player.portfolio_used,
            "portfolio_capacity": player.portfolio_capacity,
            "portfolio": player.portfolio,
            "net_worth": net_worth,
            "portfolio_value": portfolio_value,
            "total_assets": total_assets,
            "day": 41 - player.days_left
        }
        
        # Log the player status
        self.log_event("PLAYER_STATUS", player_data)
        
        # Track daily stats
        if stock_manager:
            daily_stat = {
                "day": 41 - player.days_left,
                "cash": player.cash,
                "bank_savings": player.bank_savings,
                "debt": player.debt,
                "health": player.health,
                "fame": player.fame,
                "net_worth": net_worth,
                "portfolio_value": portfolio_value,
                "total_assets": total_assets
            }
            
            # Check if we already have a stat for this day
            day_exists = False
            for i, stat in enumerate(self.daily_stats):
                if stat["day"] == daily_stat["day"]:
                    self.daily_stats[i] = daily_stat
                    day_exists = True
                    break
            
            if not day_exists:
                self.daily_stats.append(daily_stat)
    
    def log_next_day(self, player, stock_manager=None) -> None:
        """
        Log a next day event.
        
        Args:
            player: Player object
            stock_manager: StockManager object (optional)
        """
        next_day_data = {
            "player_name": player.name,
            "day": 41 - player.days_left,
            "days_left": player.days_left
        }
        
        self.log_event("NEXT_DAY", next_day_data)
        
        # Update player status with the new day
        if stock_manager:
            self.log_player_status(player, stock_manager)
    
    def log_buy(self, player, stock_id: int, ticker: str, name: str, quantity: int, price: int) -> None:
        """
        Log a buy event.
        
        Args:
            player: Player object
            stock_id: ID of the stock
            ticker: Ticker symbol of the stock
            name: Name of the stock
            quantity: Quantity of stocks bought
            price: Price per share
        """
        buy_data = {
            "player_name": player.name,
            "stock_id": stock_id,
            "ticker": ticker,
            "name": name,
            "quantity": quantity,
            "price": price,
            "total_cost": price * quantity,
            "cash_after": player.cash
        }
        
        self.log_event("BUY", buy_data)
    
    def log_sell(self, player, stock_id: int, ticker: str, name: str, quantity: int, price: int, buy_price: int) -> None:
        """
        Log a sell event.
        
        Args:
            player: Player object
            stock_id: ID of the stock
            ticker: Ticker symbol of the stock
            name: Name of the stock
            quantity: Quantity of stocks sold
            price: Price per share
            buy_price: Original buy price per share
        """
        profit = (price - buy_price) * quantity
        sell_data = {
            "player_name": player.name,
            "stock_id": stock_id,
            "ticker": ticker,
            "name": name,
            "quantity": quantity,
            "price": price,
            "buy_price": buy_price,
            "profit": profit,
            "total_revenue": price * quantity,
            "cash_after": player.cash
        }
        
        self.log_event("SELL", sell_data)
    
    def log_bank_transaction(self, player, transaction_type: str, amount: int) -> None:
        """
        Log a bank transaction.
        
        Args:
            player: Player object
            transaction_type: Type of transaction (e.g., "DEPOSIT", "WITHDRAW", "REPAY")
            amount: Amount of money involved
        """
        transaction_data = {
            "player_name": player.name,
            "transaction_type": transaction_type,
            "amount": amount,
            "cash_after": player.cash,
            "bank_savings_after": player.bank_savings,
            "debt_after": player.debt
        }
        
        self.log_event("BANK_TRANSACTION", transaction_data)
    
    def log_random_event(self, event_name: str, event_description: str, effects: Dict[str, Any]) -> None:
        """
        Log a random event.
        
        Args:
            event_name: Name of the event
            event_description: Description of the event
            effects: Dictionary of effects (e.g., {"health": -10, "cash": -100})
        """
        event_data = {
            "event_name": event_name,
            "event_description": event_description,
            "effects": effects
        }
        
        self.log_event("RANDOM_EVENT", event_data)
    
    def log_game_end(self, player, reason: str, final_score: int, stock_manager=None) -> None:
        """
        Log the end of the game.
        
        Args:
            player: Player object
            reason: Reason for game end (e.g., "DAYS_OVER", "HEALTH_ZERO")
            final_score: Final score
            stock_manager: StockManager object (optional)
        """
        # Calculate final portfolio value
        portfolio_value = 0
        if stock_manager and player.portfolio:
            for stock_id, stock_info in player.portfolio.items():
                # Find current market price
                for market_stock_id, _, _, price in stock_manager.get_available_stocks():
                    if market_stock_id == stock_id:
                        portfolio_value += price * stock_info['quantity']
                        break
        
        total_assets = final_score + portfolio_value
        
        end_data = {
            "player_name": player.name,
            "reason": reason,
            "days_played": 40 - player.days_left,
            "final_cash": player.cash,
            "final_bank_savings": player.bank_savings,
            "final_debt": player.debt,
            "final_health": player.health,
            "final_fame": player.fame,
            "final_score": final_score,
            "portfolio_value": portfolio_value,
            "total_assets": total_assets
        }
        
        self.log_event("GAME_END", end_data)
        
        # Save daily stats to a JSON file
        stats_file = self.log_file.replace('.log', '_stats.json')
        with open(stats_file, 'w') as f:
            json.dump({
                "daily_stats": self.daily_stats,
                "actions_log": self.actions_log,
                "end_data": end_data
            }, f, indent=2)
        
        # Log the log file paths
        print(f"\nGame log saved to: {self.log_file}")
        print(f"Game stats saved to: {stats_file}")
    
    def get_net_worth_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of player's net worth over time.
        
        Returns:
            List of daily stats dictionaries sorted by day
        """
        # Sort by day
        sorted_stats = sorted(self.daily_stats, key=lambda x: x["day"])
        return sorted_stats
