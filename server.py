#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask server for Yolo Terminal game.
Provides API endpoints for the web interface.
"""

import os
import json
import random
import string
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

# Import game modules
from game.player import Player
from game.stocks import Stock, StockManager
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

# Create Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Enable CORS for all routes

# Game state storage (in-memory for simplicity)
# In a production environment, you would use a database
game_states = {}

def generate_token():
    """Generate a unique token for a game."""
    # Generate a random token with letters and numbers
    letters_and_digits = string.ascii_letters + string.digits
    token = ''.join(random.choice(letters_and_digits) for i in range(10))
    return token

def create_new_game(player_name):
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
        'message': "Welcome to Yolo Terminal! Day 1 has begun."
    }
    
    # Store game state by both game_id and token
    game_states[game_id] = game_state
    game_states[token] = game_state
    
    return game_state

def get_game_state_data(game_state):
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
        'net_worth_history': net_worth_history
    }

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/new_game', methods=['POST'])
def new_game():
    """Create a new game."""
    data = request.json
    player_name = data.get('player_name', 'Trader')
    
    # Truncate to 10 characters if longer
    if len(player_name) > 10:
        player_name = player_name[:10]
    
    # Check for emoji or non-ASCII characters
    if not all(ord(c) < 128 for c in player_name):
        return jsonify({'error': 'Please use only ASCII characters (no emoji)'}), 400
    
    game_state = create_new_game(player_name)
    
    # Return game state data
    return jsonify(get_game_state_data(game_state))

@app.route('/api/game/<game_id>', methods=['GET'])
def get_game(game_id):
    """Get game state."""
    game_state = game_states.get(game_id)
    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    return jsonify(get_game_state_data(game_state))

@app.route('/api/game/<game_id>/next_day', methods=['POST'])
def next_day(game_id):
    """Advance to the next day."""
    game_state = game_states.get(game_id)
    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    player = game_state['player']
    stock_manager = game_state['stock_manager']
    day_manager = game_state['day_manager']
    event_manager = game_state['event_manager']
    bank = game_state['bank']
    logger = game_state['logger']
    
    # Handle next day
    player.days_left -= 1
    
    # Log travel event
    logger.log_next_day(player, stock_manager)
    
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
    
    # Set message - simplified to just show day info
    message = f"Day {41 - player.days_left} has begun. Check out today's available stocks!"
    
    # Update game state
    game_state['news_reports'] = news_reports
    game_state['message'] = message
    
    # Log player status after next day
    logger.log_player_status(player, stock_manager)
    
    # Check if game should end
    game_over = False
    game_over_reason = None
    final_score = 0
    
    if player.days_left <= 0:
        game_over = True
        game_over_reason = "DAYS_OVER"
        
        # Sell all remaining stocks
        stock_manager.sell_all_stocks(player, None, logger, day_manager)
        
        # Calculate final score and profit
        final_score = player.cash + player.bank_savings - player.debt
        portfolio_value = 0  # Portfolio should be empty after selling all stocks
        total_assets = final_score + portfolio_value
        profit = total_assets - 2000 + 5000  # Starting cash was $2000, debt was $5000
        
        # Calculate tax (45% of profit, only if profit is positive)
        tax = round(max(0, profit * 0.45))
        
        if profit > 0:
            game_state['message'] = f"Your final score is: ${final_score}\nPortfolio value: ${portfolio_value}\nTotal assets: ${total_assets}\n\nYour profit: ${profit}\nTax (45%): ${tax}\nNet profit after tax: ${profit - tax}"
        else:
            # Check if player is in debt
            if player.debt > player.cash + player.bank_savings:
                debt_remaining = player.debt - (player.cash + player.bank_savings)
                hours_needed = round(debt_remaining / 10)  # $10 per hour at Mandy's
                game_state['message'] = f"Your final score is: ${final_score}\nPortfolio value: ${portfolio_value}\nTotal assets: ${total_assets}\n\nYou ended with a loss of ${-profit}.\n\nYou still have ${debt_remaining} in debt. You'll need to work at Mandy's for {hours_needed} hours to pay it off."
            else:
                game_state['message'] = f"Your final score is: ${final_score}\nPortfolio value: ${portfolio_value}\nTotal assets: ${total_assets}\n\nYou ended with a loss of ${-profit}, but at least you're not in debt!"
        
        # Check if it's a high score
        game_state['high_scores'].add_score(player.name, final_score, player.health, player.fame)
        
        # Log game end
        logger.log_game_end(player, game_over_reason, final_score, stock_manager)
    
    # Check if player is dead
    if player.health <= 0:
        game_over = True
        game_over_reason = "HEALTH_ZERO"
        
        # Calculate final score
        final_score = player.cash + player.bank_savings - player.debt
        
        game_state['message'] = "Your health has dropped to 0. Game over!"
        
        # Log game end
        logger.log_game_end(player, game_over_reason, final_score, stock_manager)
    
    # Return game state data with game over info
    response_data = get_game_state_data(game_state)
    if game_over:
        response_data['game_over'] = True
        response_data['game_over_reason'] = game_over_reason
        response_data['final_score'] = final_score
        response_data['high_scores'] = game_state['high_scores'].get_scores()
    
    return jsonify(response_data)

@app.route('/api/game/<game_id>/buy', methods=['POST'])
def buy_stocks(game_id):
    """Buy stocks."""
    game_state = game_states.get(game_id)
    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    data = request.json
    stock_id = data.get('stock_id')
    amount = data.get('amount', 1)
    
    player = game_state['player']
    stock_manager = game_state['stock_manager']
    logger = game_state['logger']
    
    # Find the stock
    stock_found = False
    for market_stock_id, ticker, name, price in stock_manager.get_available_stocks():
        if market_stock_id == stock_id:
            stock_found = True
            
            # Check if player has enough money
            if player.cash < price:
                return jsonify({'error': "You don't have enough cash to buy even one share of this stock."}), 400
            
            # Calculate max amount player can buy
            max_buy = min(player.cash // price, player.portfolio_capacity - player.portfolio_used)
            if max_buy <= 0:
                return jsonify({'error': "You don't have enough space in your trade book or cash to buy this stock."}), 400
            
            # Validate amount
            if amount > max_buy:
                amount = max_buy
            
            # Process purchase
            player.cash -= price * amount
            player.add_to_portfolio(stock_id, ticker, name, amount, price)
            
            # Log the purchase
            logger.log_buy(player, stock_id, ticker, name, amount, price)
            
            game_state['message'] = f"You bought {amount} shares of ${ticker} for ${price * amount}."
            break
    
    if not stock_found:
        return jsonify({'error': 'Stock not found'}), 404
    
    return jsonify(get_game_state_data(game_state))

@app.route('/api/game/<game_id>/sell', methods=['POST'])
def sell_stocks(game_id):
    """Sell stocks."""
    game_state = game_states.get(game_id)
    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    data = request.json
    stock_id = data.get('stock_id')
    amount = data.get('amount', 1)
    
    player = game_state['player']
    stock_manager = game_state['stock_manager']
    logger = game_state['logger']
    
    # Check if player has the stock
    if stock_id not in player.portfolio:
        return jsonify({'error': 'Stock not found in portfolio'}), 404
    
    stock_info = player.portfolio[stock_id]
    
    # Check if the stock is available in the market
    market_price = 0
    is_available = False
    for market_stock_id, ticker, name, price in stock_manager.get_available_stocks():
        if market_stock_id == stock_id:
            market_price = price
            is_available = True
            break
    
    if not is_available:
        return jsonify({'error': f"${stock_info['ticker']} is not currently tradable in the market."}), 400
    
    # Validate amount
    if amount > stock_info['quantity']:
        amount = stock_info['quantity']
    
    # Process sale
    player.cash += market_price * amount
    player.remove_from_portfolio(stock_id, amount)
    
    # Log the sale
    logger.log_sell(player, stock_id, stock_info['ticker'], stock_info['name'], amount, market_price, stock_info['price'])
    
    game_state['message'] = f"You sold {amount} shares of ${stock_info['ticker']} for ${market_price * amount}."
    
    return jsonify(get_game_state_data(game_state))

@app.route('/api/game/<game_id>/bank', methods=['POST'])
def bank_action(game_id):
    """Perform bank actions."""
    game_state = game_states.get(game_id)
    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    data = request.json
    action = data.get('action')
    amount = data.get('amount', 0)
    
    player = game_state['player']
    bank = game_state['bank']
    logger = game_state['logger']
    
    if action == 'deposit':
        # Validate amount
        if amount > player.cash:
            return jsonify({'error': "You don't have enough cash."}), 400
        
        # Process deposit
        player.cash -= amount
        player.bank_savings += amount
        
        # Log the deposit
        logger.log_bank_deposit(player, amount)
        
        game_state['message'] = f"You deposited ${amount} into your savings account."
    
    elif action == 'withdraw':
        # Validate amount
        if amount > player.bank_savings:
            return jsonify({'error': "You don't have enough savings."}), 400
        
        # Process withdrawal
        player.bank_savings -= amount
        player.cash += amount
        
        # Log the withdrawal
        logger.log_bank_withdraw(player, amount)
        
        game_state['message'] = f"You withdrew ${amount} from your savings account."
    
    elif action == 'repay':
        # Validate amount
        if amount > player.cash:
            return jsonify({'error': "You don't have enough cash."}), 400
        
        if amount > player.debt:
            amount = player.debt
        
        # Process repayment
        player.cash -= amount
        player.debt -= amount
        
        # Log the repayment
        logger.log_debt_repay(player, amount)
        
        game_state['message'] = f"You repaid ${amount} of your debt."
    
    else:
        return jsonify({'error': 'Invalid action'}), 400
    
    return jsonify(get_game_state_data(game_state))

@app.route('/api/game/<game_id>/hospital', methods=['POST'])
def hospital_action(game_id):
    """Visit the hospital."""
    game_state = game_states.get(game_id)
    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    player = game_state['player']
    hospital = game_state['hospital']
    
    # Check if player has enough cash for copay
    copay = 200
    if player.cash < copay:
        return jsonify({'error': f"You need ${copay} for the hospital copay, but you only have ${player.cash}."}), 400
    
    # Calculate cost based on current health
    health_needed = 100 - player.health
    health_cost = health_needed * 10000  # $10,000 per health point
    total_cost = copay + health_cost
    
    # Check if player has enough cash for total cost
    if player.cash < total_cost:
        return jsonify({'error': f"You need ${total_cost} to fully restore your health (${copay} copay + ${health_cost} treatment cost due to your health insurance), but you only have ${player.cash}."}), 400
    
    # Process hospital visit
    player.cash -= total_cost
    player.health = 100
    
    game_state['message'] = f"You spent ${total_cost} at the hospital (${copay} copay + ${health_cost} treatment cost due to your health insurance) and restored your health to 100."
    
    return jsonify(get_game_state_data(game_state))

@app.route('/api/game/<game_id>/broker', methods=['POST'])
def broker_action(game_id):
    """Visit the student loan broker."""
    game_state = game_states.get(game_id)
    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    data = request.json
    amount = data.get('amount', 0)
    
    player = game_state['player']
    logger = game_state['logger']
    
    # Validate amount
    if amount > player.cash:
        return jsonify({'error': "You don't have enough cash."}), 400
    
    if amount > player.debt:
        amount = player.debt
    
    # Process repayment
    player.cash -= amount
    player.debt -= amount
    
    # Log the repayment
    logger.log_debt_repay(player, amount)
    
    game_state['message'] = f"You repaid ${amount} of your student loan debt."
    
    return jsonify(get_game_state_data(game_state))

@app.route('/api/game/<game_id>/trading_app', methods=['POST'])
def trading_app_action(game_id):
    """Use the trading app."""
    game_state = game_states.get(game_id)
    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    player = game_state['player']
    
    # Calculate cost for upgrade
    cost = 30000  # $30,000 for 10 additional slots
    
    # Check if player has enough cash
    if player.cash < cost:
        return jsonify({'error': f"You need ${cost} to upgrade your trade book capacity, but you only have ${player.cash}."}), 400
    
    # Process upgrade
    player.cash -= cost
    player.portfolio_capacity += 10  # Add 10 slots instead of 50
    
    game_state['message'] = f"You spent ${cost} to upgrade your trade book capacity by 10 slots to {player.portfolio_capacity}."
    
    return jsonify(get_game_state_data(game_state))

@app.route('/api/game/<game_id>/darkweb', methods=['POST'])
def darkweb_action(game_id):
    """Visit the darkweb."""
    game_state = game_states.get(game_id)
    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    player = game_state['player']
    
    # Check if player has visited the darkweb too many times
    if player.darkweb_visits >= 3:
        return jsonify({'error': "You've visited the darkweb too many times today. Try again tomorrow."}), 400
    
    # Process darkweb visit
    player.darkweb_visits += 1
    
    # Random reward
    reward = random.randint(50, 200)
    player.cash += reward
    
    # Random health penalty
    health_penalty = random.randint(5, 15)
    player.health = max(0, player.health - health_penalty)
    
    game_state['message'] = f"You visited the darkweb and found ${reward}, but lost {health_penalty} health points."
    
    return jsonify(get_game_state_data(game_state))

@app.route('/api/high_scores', methods=['GET'])
def get_high_scores():
    """Get high scores."""
    # Combine high scores from all games
    all_scores = []
    for game_state in game_states.values():
        all_scores.extend(game_state['high_scores'].get_scores())
    
    # Sort by score (descending)
    all_scores.sort(key=lambda x: x['score'], reverse=True)
    
    # Take top 10
    top_scores = all_scores[:10]
    
    return jsonify(top_scores)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
