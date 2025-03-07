#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yolo Terminal - Python Command Line Version
Based on the original Beijing Life Story game

This is a remake of the classic Chinese game where players try to make money
by trading stocks over a 40-day period.
"""

import random
import os
import sys
import time
from typing import List, Dict, Tuple, Optional, Any

# Import game modules
from game.player import Player
from game.stocks import Stock, StockManager
from game.locations import DayManager
from game.events import EventManager
from game.ui import UI
from game.bank import Bank
from game.hospital import Hospital
from game.trading_app import TradingApp
from game.darkweb import Darkweb
from game.broker import Broker
from game.high_scores import HighScores
from game.logger import GameLogger

def main():
    """Main game function that initializes and runs the game."""
    ui = UI()
    
    # Show welcome screen first (without player status)
    ui.show_welcome(clear_after=False)  # Don't clear screen after welcome
    
    # Get player name under the welcome screen (append to welcome)
    # Limit to max 10 letters, no emoji
    while True:
        player_name = ui.get_input("\nEnter your name (max 10 letters): ", default="Trader")
        # Truncate to 10 characters if longer
        if len(player_name) > 10:
            player_name = player_name[:10]
        
        # Check for emoji or non-ASCII characters
        if not all(ord(c) < 128 for c in player_name):
            print("Please use only ASCII characters (no emoji).")
            continue
        
        break
    
    # Initialize game components
    player = Player(name=player_name)
    stock_manager = StockManager()
    day_manager = DayManager()
    event_manager = EventManager()
    bank = Bank()
    hospital = Hospital()
    trading_app = TradingApp()
    darkweb = Darkweb()
    broker = Broker()
    high_scores = HighScores()
    
    # Initialize logger
    logger = GameLogger(player_name)
    logger.log_player_status(player)
    
    # Show story if player wants (with player status)
    if ui.ask_yes_no("View game backstory?"):
        ui.show_story(player, stock_manager, day_manager)
    
    # Start day 1 with top board always on
    ui.clear_screen()
    ui.show_status(player, stock_manager, day_manager)
    ui.show_message("Welcome to Yolo Terminal! Day 1 has begun.", player, stock_manager, day_manager)
    ui.show_available_stocks(stock_manager, player, day_manager)
    
    # Main game loop
    game_running = True
    while game_running:
        ui.clear_screen()
        ui.show_status(player, stock_manager, day_manager)
        
        # Show main menu
        choice = ui.show_main_menu(player)
        
        if choice == "next_day":
            # Handle next day
            player.days_left -= 1
            
            # Log travel event
            logger.log_next_day(player)
            
            # Update stock prices
            stock_manager.update_prices()
            
            # Handle random events and show news reports
            news_reports = event_manager.handle_events(player, stock_manager)
            
            # Add debt collector visit in the last 10 days if player has debt
            if player.days_left <= 10 and player.debt > 0:
                debt_collector_report = f"A debt collector visits you, demanding payment. The stress affects your mental health. (-10 health)"
                player.health = max(0, player.health - 10)
                if not news_reports:
                    news_reports = [debt_collector_report]
                else:
                    news_reports.append(debt_collector_report)
                
                # Log debt collector event
                logger.log_random_event("Debt Collector", debt_collector_report, {})
            
            if news_reports:
                ui.show_news_reports(news_reports, player, stock_manager, day_manager)
                
                # Log random events
                for report in news_reports:
                    if "debt collector" not in report.lower():  # Skip logging debt collector again
                        logger.log_random_event("Random Event", report, {})
            
            # Update bank interest and debt
            bank.update_interest(player)
            
            # Calculate net worth and profit
            current_net_worth = player.cash + player.bank_savings - player.debt
            
            # Calculate portfolio value
            portfolio_value = 0
            for stock_id, stock_info in player.portfolio.items():
                # Find current market price
                for market_stock_id, _, _, price in stock_manager.get_available_stocks():
                    if market_stock_id == stock_id:
                        portfolio_value += price * stock_info['quantity']
                        break
            
            total_assets = current_net_worth + portfolio_value
            
            # Calculate profit (simplified)
            profit = total_assets - 2000 + 5000  # Starting cash was $2000, debt was $5000
            
            # Calculate tax (45% of profit, only if profit is positive)
            tax = round(max(0, profit * 0.45))
            
            # Show day summary with profit and tax information
            if profit > 0:
                ui.show_message(f"Day {41 - player.days_left} has begun.\n\nYour current net worth: ${current_net_worth}\nPortfolio value: ${portfolio_value}\nTotal assets: ${total_assets}\n\nEstimated profit: ${profit}\nEstimated tax (45%): ${tax}", player, stock_manager, day_manager)
            else:
                ui.show_message(f"Day {41 - player.days_left} has begun.\n\nYour current net worth: ${current_net_worth}\nPortfolio value: ${portfolio_value}\nTotal assets: ${total_assets}\n\nYou are currently at a loss of ${-profit}.", player, stock_manager, day_manager)
            
            # Show available stocks
            ui.show_available_stocks(stock_manager, player, day_manager)
            
            # Log player status after next day
            logger.log_player_status(player)
            
        elif choice == "buy":
            while True:
                result = stock_manager.buy_stocks(player, ui, logger, day_manager)
                if result == "exit":
                    break
            
        elif choice == "sell":
            while True:
                result = stock_manager.sell_stocks(player, ui, logger, day_manager)
                if result == "exit":
                    break
            
        elif choice == "bank":
            bank.visit(player, ui, logger)
            
        elif choice == "hospital":
            hospital.visit(player, ui)
            
        elif choice == "broker":
            broker.visit(player, ui)
            
        elif choice == "trading_app":
            trading_app.visit(player, ui)
            
        elif choice == "darkweb":
            darkweb.visit(player, ui)
            
        elif choice == "high_scores":
            high_scores.show(ui)
            
        elif choice == "help":
            ui.show_help(player, stock_manager, day_manager)
            
        elif choice == "quit":
            if ui.ask_yes_no("Are you sure you want to quit?"):
                game_running = False
        
        # Check if game should end
        if player.days_left <= 0:
            ui.show_message("You've completed your 40 days of trading. Time to see your results.", player, stock_manager, day_manager)
            # Sell all remaining stocks
            stock_manager.sell_all_stocks(player, ui, logger, day_manager)
            # Calculate portfolio value
            portfolio_value = 0
            for stock_id, stock_info in player.portfolio.items():
                # Find current market price
                for market_stock_id, _, _, price in stock_manager.get_available_stocks():
                    if market_stock_id == stock_id:
                        portfolio_value += price * stock_info['quantity']
                        break
            
            # Calculate final score and profit
            final_score = player.cash + player.bank_savings - player.debt
            total_assets = final_score + portfolio_value
            profit = total_assets - 2000 + 5000  # Starting cash was $2000, debt was $5000
            
            # Calculate tax (45% of profit, only if profit is positive)
            tax = round(max(0, profit * 0.45))
            
            if profit > 0:
                ui.show_message(f"Your final score is: ${final_score}\nPortfolio value: ${portfolio_value}\nTotal assets: ${total_assets}\n\nYour profit: ${profit}\nTax (45%): ${tax}\nNet profit after tax: ${profit - tax}", player, stock_manager, day_manager)
            else:
                # Check if player is in debt
                if player.debt > player.cash + player.bank_savings:
                    debt_remaining = player.debt - (player.cash + player.bank_savings)
                    hours_needed = round(debt_remaining / 10)  # $10 per hour at Mandy's
                    ui.show_message(f"Your final score is: ${final_score}\nPortfolio value: ${portfolio_value}\nTotal assets: ${total_assets}\n\nYou ended with a loss of ${-profit}.\n\nYou still have ${debt_remaining} in debt. You'll need to work at Mandy's for {hours_needed} hours to pay it off.", player, stock_manager, day_manager)
                else:
                    ui.show_message(f"Your final score is: ${final_score}\nPortfolio value: ${portfolio_value}\nTotal assets: ${total_assets}\n\nYou ended with a loss of ${-profit}, but at least you're not in debt!", player, stock_manager, day_manager)
            
            # Check if it's a high score
            high_scores.add_score(player.name, final_score, player.health, player.fame)
            high_scores.show(ui)
            # Log game end
            logger.log_game_end(player, "DAYS_OVER", final_score)
            game_running = False
        
        # Check if player is dead
        if player.health <= 0:
            ui.show_message("Your health has dropped to 0. Game over!", player, stock_manager, day_manager)
            # Calculate final score
            final_score = player.cash + player.bank_savings - player.debt
            # Log game end
            logger.log_game_end(player, "HEALTH_ZERO", final_score)
            game_running = False
    
    ui.show_message("Thanks for playing Yolo Terminal!", player, stock_manager, day_manager)

if __name__ == "__main__":
    main()
