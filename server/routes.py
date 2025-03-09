#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API routes for Yolo Terminal game.
"""

from flask import Blueprint, request, jsonify, render_template, send_from_directory

from .game_state import (
    create_new_game,
    get_game_state,
    get_game_state_data
)

# Create a blueprint for the API routes
api = Blueprint('api', __name__)

# Create a blueprint for the main routes
main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@api.route('/new_game', methods=['POST'])
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

@api.route('/game/<game_id>', methods=['GET'])
def get_game(game_id):
    """Get game state."""
    game_state = get_game_state(game_id)
    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    return jsonify(get_game_state_data(game_state))

@api.route('/game/<game_id>/next_day', methods=['POST'])
def next_day(game_id):
    """Advance to the next day."""
    game_state = get_game_state(game_id)
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
    game_state['show_stocks'] = True  # Show available stocks when a new day begins
    
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

@api.route('/game/<game_id>/buy', methods=['POST'])
def buy_stocks(game_id):
    """Buy stocks."""
    game_state = get_game_state(game_id)
    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    data = request.json
    stock_id = data.get('stock_id')
    amount = int(data.get('amount', 1))  # Ensure amount is an integer
    
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

@api.route('/game/<game_id>/sell', methods=['POST'])
def sell_stocks(game_id):
    """Sell stocks."""
    game_state = get_game_state(game_id)
    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    data = request.json
    stock_id = data.get('stock_id')
    amount = int(data.get('amount', 1))  # Ensure amount is an integer
    
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

@api.route('/game/<game_id>/bank', methods=['POST'])
def bank_action(game_id):
    """Perform bank actions."""
    game_state = get_game_state(game_id)
    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    data = request.json
    action = data.get('action')
    amount = int(data.get('amount', 0))  # Ensure amount is an integer
    
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
        logger.log_bank_transaction(player, "DEPOSIT", amount)
        
        game_state['message'] = f"You deposited ${amount} into your savings account."
    
    elif action == 'withdraw':
        # Validate amount
        if amount > player.bank_savings:
            return jsonify({'error': "You don't have enough savings."}), 400
        
        # Process withdrawal
        player.bank_savings -= amount
        player.cash += amount
        
        # Log the withdrawal
        logger.log_bank_transaction(player, "WITHDRAW", amount)
        
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
        logger.log_bank_transaction(player, "REPAY", amount)
        
        game_state['message'] = f"You repaid ${amount} of your debt."
    
    else:
        return jsonify({'error': 'Invalid action'}), 400
    
    return jsonify(get_game_state_data(game_state))

@api.route('/game/<game_id>/hospital', methods=['POST'])
def hospital_action(game_id):
    """Visit the hospital."""
    game_state = get_game_state(game_id)
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

@api.route('/game/<game_id>/broker', methods=['POST'])
def broker_action(game_id):
    """Visit the student loan broker."""
    game_state = get_game_state(game_id)
    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    data = request.json
    amount = int(data.get('amount', 0))  # Ensure amount is an integer
    
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
    logger.log_bank_transaction(player, "REPAY", amount)
    
    game_state['message'] = f"You repaid ${amount} of your student loan debt."
    
    return jsonify(get_game_state_data(game_state))

@api.route('/game/<game_id>/trading_app', methods=['POST'])
def trading_app_action(game_id):
    """Use the trading app."""
    game_state = get_game_state(game_id)
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

@api.route('/game/<game_id>/darkweb', methods=['POST'])
def darkweb_action(game_id):
    """Visit the darkweb."""
    game_state = get_game_state(game_id)
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

@api.route('/game/<game_id>/chart', methods=['GET'])
def get_chart_data(game_id):
    """Get chart data for a game."""
    game_state = get_game_state(game_id)
    if not game_state:
        return jsonify({'error': 'Game not found'}), 404
    
    # Get net worth history
    net_worth_history = game_state['logger'].get_net_worth_history()
    
    # Check if game is completed (40 days)
    player = game_state['player']
    game_completed = player.days_left <= 0 or player.health <= 0
    
    # Calculate final score
    final_score = player.cash + player.bank_savings - player.debt
    
    # Calculate portfolio value
    portfolio_value = 0
    stock_manager = game_state['stock_manager']
    for stock_id, stock_info in player.portfolio.items():
        # Find current market price
        for market_stock_id, _, _, price in stock_manager.get_available_stocks():
            if market_stock_id == stock_id:
                portfolio_value += price * stock_info['quantity']
                break
    
    # Calculate total assets
    total_assets = final_score + portfolio_value
    
    # Return chart data
    return jsonify({
        'net_worth_history': net_worth_history,
        'game_completed': game_completed,
        'final_score': final_score,
        'portfolio_value': portfolio_value,
        'total_assets': total_assets,
        'player_name': player.name,
        'days_left': player.days_left
    })

@api.route('/high_scores', methods=['GET'])
def get_high_scores():
    """Get high scores."""
    from .game_state import game_states
    
    # Combine high scores from all games
    all_scores = []
    for game_state in game_states.values():
        all_scores.extend(game_state['high_scores'].get_scores())
    
    # Sort by score (descending)
    all_scores.sort(key=lambda x: x['score'], reverse=True)
    
    # Take top 10
    top_scores = all_scores[:10]
    
    return jsonify(top_scores)
