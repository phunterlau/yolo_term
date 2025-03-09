#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Game state management for Yolo Terminal game.
"""

import random
import string
from typing import Dict, Any, Optional

from game.player import Player
from game.stocks import StockManager
from game.locations import DayManager
from game.events import EventManager
from game.bank import Bank
from game.hospital import Hospital
from game.trading_app import TradingApp
from game.darkweb import Darkweb
from game.broker import Broker
from game.high_scores import HighScores
from game.logger import GameLogger
from game.headlines import get_random_headline

# Game state storage (in-memory for simplicity)
# In a production environment, you would use a database
game_states = {}

def generate_token() -> str:
    """Generate a unique token for a game."""
    # Generate a random token with letters and numbers
    letters_and_digits = string.ascii_letters + string.digits
    token = ''.join(random.choice(letters_and_digits) for i in range(10))
    return token

def create_new_game(player_name: str) -> Dict[str, Any]:
    """
    Create a new game state.
    
    Args:
        player_name: Name of the player
        
    Returns:
        dict: Game state
    """
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
    
    # Generate a unique game ID
    game_id = str(random.randint(10000, 99999))
    
    # Generate a unique token for this game
    token = generate_token()
    
    # Create game state
    game_state = {
        'game_id': game_id,
        'token': token,
        'player': player,
        'stock_manager': stock_manager,
        'day_manager': day_manager,
        'event_manager': event_manager,
        'bank': bank,
        'hospital': hospital,
        'trading_app': trading_app,
        'darkweb': darkweb,
        'broker': broker,
        'high_scores': high_scores,
        'logger': logger,
        'news_reports': [],
        'message': "Welcome to Yolo Terminal! Day 1 has begun. Let's jump into the stock market!",
        'show_stocks': False  # Don't show stocks automatically on first day
    }
    
    # Store game state by both game_id and token
    game_states[game_id] = game_state
    game_states[token] = game_state
    
    return game_state

def get_game_state(game_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a game state by ID or token.
    
    Args:
        game_id: Game ID or token
        
    Returns:
        dict: Game state or None if not found
    """
    return game_states.get(game_id)

def get_game_state_data(game_state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get serializable game state data.
    
    Args:
        game_state: Game state
        
    Returns:
        dict: Serializable game state data
    """
    player = game_state['player']
    stock_manager = game_state['stock_manager']
    day_manager = game_state['day_manager']
    
    # Get available stocks
    available_stocks = []
    for stock_id, ticker, name, price in stock_manager.get_available_stocks():
        available_stocks.append({
            'id': stock_id,
            'ticker': ticker,
            'name': name,
            'price': price
        })
    
    # Get portfolio
    portfolio = []
    for stock_id, stock_info in player.portfolio.items():
        # Check if stock is available in market
        market_price = 0
        for market_stock in available_stocks:
            if market_stock['id'] == stock_id:
                market_price = market_stock['price']
                break
        
        portfolio.append({
            'id': stock_id,
            'ticker': stock_info['ticker'],
            'name': stock_info['name'],
            'quantity': stock_info['quantity'],
            'price': stock_info['price'],
            'market_price': market_price
        })
    
    # Get current day description
    current_day = day_manager.get_day_description(player)
    
    # Get a random headline
    headline, agency, _ = get_random_headline()
    
    # Get net worth history
    net_worth_history = game_state['logger'].get_net_worth_history()
    
    # Include show_stocks flag if it exists in the game state
    show_stocks = game_state.get('show_stocks', False)
    
    return {
        'game_id': game_state['game_id'],
        'token': game_state['token'],  # Include the token in the response
        'player': {
            'name': player.name,
            'days_left': player.days_left,
            'cash': player.cash,
            'debt': player.debt,
            'bank_savings': player.bank_savings,
            'health': player.health,
            'fame': player.fame,
            'portfolio_capacity': player.portfolio_capacity,
            'portfolio_used': player.portfolio_used
        },
        'current_day': current_day,
        'available_stocks': available_stocks,
        'portfolio': portfolio,
        'headline': {
            'text': headline,
            'agency': agency
        },
        'news_reports': game_state['news_reports'],
        'message': game_state['message'],
        'net_worth_history': net_worth_history,
        'show_stocks': show_stocks
    }
