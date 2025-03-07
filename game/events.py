#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Events module for Yolo Terminal game.
Handles random events that can occur during the game.
"""

import random
from typing import Dict, List, Optional, Tuple, Any

class EventManager:
    """
    EventManager class to manage all random events in the game.
    """
    
    def __init__(self):
        """Initialize the event manager with all event types."""
        # Market events that affect stock prices and quantities
        self.market_events = []
        self._init_market_events()
        
        # Health events that affect player health
        self.health_events = []
        self._init_health_events()
        
        # Money events that affect player cash
        self.money_events = []
        self._init_money_events()
    
    def _init_market_events(self):
        """Initialize market events."""
        self.market_events = [
            {
                "freq": 170,
                "msg": "Analyst report: Tezla ($TZLA) electric vehicles are in high demand, with supply shortages reported!",
                "stock_id": 5,  # Tezla
                "multiply": 2,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 139,
                "msg": "FDA investigation: nWidia ($NWDA) chips found to cause overheating in devices, consumers advised to avoid!",
                "stock_id": 3,  # nWidia
                "multiply": 3,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 100,
                "msg": "Wall Street Journal reports: SBY500 ($SBY) index fund performance 'exceptional' this quarter!",
                "stock_id": 4,  # SBY500
                "multiply": 5,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 41,
                "msg": "Famous investor Warren Buffer says: 'All 2025 Nobel Prize winners use Cato Coin ($CATO) for transactions!'",
                "stock_id": 2,  # Cato Coin
                "multiply": 4,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 37,
                "msg": "SEC announces crackdown on Pitcoin ($PITCOIN) exchanges, citing market manipulation concerns!",
                "stock_id": 1,  # Pitcoin
                "multiply": 3,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 23,
                "msg": "Tech blogs report: Plantir ($PLTI) data analytics software being adopted by major corporations worldwide!",
                "stock_id": 7,  # Plantir
                "multiply": 4,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 37,
                "msg": "CNBC.com reports: SBY500 ($SBY) outperforming all other index funds, investors flocking to buy!",
                "stock_id": 4,  # SBY500
                "multiply": 8,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 15,
                "msg": "Celebrity endorsement: 'I use Plantir ($PLTI) for all my data needs!' says tech influencer Elan Mush.",
                "stock_id": 7,  # Plantir
                "multiply": 7,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 40,
                "msg": "nWidia ($NWDA) announces new AI chip that outperforms competitors by 300%, stock soaring!",
                "stock_id": 3,  # nWidia
                "multiply": 7,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 29,
                "msg": "College students worldwide adopting PinTuoTuo ($PTT) smartphones, sales skyrocketing! The Chinese e-commerce giant's US business Teniu is gaining popularity.",
                "stock_id": 6,  # PinTuoTuo
                "multiply": 7,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 45,
                "msg": "PinTuoTuo ($PTT), the Chinese e-commerce company, reports record sales through its US business Teniu, which specializes in Chinese high tech products!",
                "stock_id": 6,  # PinTuoTuo
                "multiply": 5,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 35,
                "msg": "Housing market boom driving Pitcoin ($PITCOIN) prices to new heights!",
                "stock_id": 1,  # Pitcoin
                "multiply": 8,
                "divide": 0,
                "add": 0
            },
            {
                "freq": 17,
                "msg": "Major security flaw discovered in Super Nicron ($SNCI) software, prices plummeting!",
                "stock_id": 0,  # Super Nicron
                "multiply": 0,
                "divide": 8,
                "add": 0
            },
            {
                "freq": 24,
                "msg": "Tezla ($TZLA) recalls thousands of vehicles due to battery issues, stock taking a hit!",
                "stock_id": 5,  # Tezla
                "multiply": 0,
                "divide": 5,
                "add": 0
            },
            {
                "freq": 18,
                "msg": "Government crackdown on Cato Coin ($CATO) mining operations, prices in free fall!",
                "stock_id": 2,  # Cato Coin
                "multiply": 0,
                "divide": 8,
                "add": 0
            },
            {
                "freq": 160,
                "msg": "Your college roommate gifted you two shares of Pitcoin ($PITCOIN), thanks to them!",
                "stock_id": 1,  # Pitcoin
                "multiply": 0,
                "divide": 0,
                "add": 2
            },
            {
                "freq": 45,
                "msg": "A class action lawsuit recovered your lost Super Nicron ($SNCI) shares.",
                "stock_id": 0,  # Super Nicron
                "multiply": 0,
                "divide": 0,
                "add": 6
            },
            {
                "freq": 35,
                "msg": "You received some nWidia ($NWDA) shares as part of a customer loyalty program!",
                "stock_id": 3,  # nWidia
                "multiply": 0,
                "divide": 0,
                "add": 4
            },
            {
                "freq": 140,
                "msg": "Media reports: PinTuoTuo ($PTT) phones sold through their US business Teniu have excellent quality! You bought one for $2500, but also received a free share of stock.",
                "stock_id": 6,  # PinTuoTuo
                "multiply": 0,
                "divide": 0,
                "add": 1
            },
            {
                "freq": 75,
                "msg": "US-China trade tensions ease, boosting PinTuoTuo's ($PTT) Teniu business which sells Chinese high tech products to US consumers!",
                "stock_id": 6,  # PinTuoTuo
                "multiply": 6,
                "divide": 0,
                "add": 0
            }
        ]
    
    def _init_health_events(self):
        """Initialize health events."""
        self.health_events = [
            {
                "freq": 117,
                "msg": "You were scammed by a fake investment advisor!",
                "damage": 3,
                "sound": "kill.wav"
            },
            {
                "freq": 157,
                "msg": "You stayed up all night watching stock charts and suffered a panic attack!",
                "damage": 20,
                "sound": "death.wav"
            },
            {
                "freq": 21,
                "msg": "A market crash caused you extreme stress, affecting your health.",
                "damage": 1,
                "sound": "dog.wav"
            },
            {
                "freq": 100,
                "msg": "Trading platform outage prevented you from selling at the peak, causing anxiety!",
                "damage": 1,
                "sound": "harley.wav"
            },
            {
                "freq": 35,
                "msg": "A hacker stole your trading password, causing you stress!",
                "damage": 1,
                "sound": "hit.wav"
            },
            {
                "freq": 313,
                "msg": "A group of angry investors blamed you for bad stock tips!",
                "damage": 10,
                "sound": "flee.wav"
            },
            {
                "freq": 120,
                "msg": "You and your friend lost money on a hot stock tip that turned out to be a scam!",
                "damage": 5,
                "sound": "death.wav"
            },
            {
                "freq": 29,
                "msg": "You were threatened by someone who lost money following your advice!",
                "damage": 3,
                "sound": "el.wav"
            },
            {
                "freq": 43,
                "msg": "You ate cheap fast food while trading and got food poisoning!",
                "damage": 1,
                "sound": "vomit.wav"
            },
            {
                "freq": 45,
                "msg": "Your terrible stock pick was mocked on social media, damaging your reputation!",
                "damage": 1,
                "sound": "level.wav"
            },
            {
                "freq": 48,
                "msg": "You were fined $40 for illegal parking while rushing to make a trade!",
                "damage": 1,
                "sound": "lan.wav"
            },
            {
                "freq": 33,
                "msg": "You spilled coffee on your laptop while checking stock prices!",
                "damage": 1,
                "sound": "breath.wav"
            }
        ]
    
    def _init_money_events(self):
        """Initialize money events."""
        self.money_events = [
            {
                "freq": 60,
                "msg": "A fake investment advisor scammed you out of some money!",
                "ratio": 10
            },
            {
                "freq": 125,
                "msg": "A hacker gained access to your trading account and stole funds!",
                "ratio": 10
            },
            {
                "freq": 100,
                "msg": "The IRS audited your trading activity and imposed a penalty!",
                "ratio": 40
            },
            {
                "freq": 65,
                "msg": "Your trading platform charged unexpected fees for inactivity!",
                "ratio": 20
            },
            {
                "freq": 35,
                "msg": "Your phone company charged extra for market data usage!",
                "ratio": 15
            },
            {
                "freq": 27,
                "msg": "A regulatory fine for pattern day trading without sufficient funds!",
                "ratio": 10
            },
            {
                "freq": 40,
                "msg": "You developed carpal tunnel syndrome from too much trading, requiring medical treatment...",
                "ratio": 5
            }
        ]
    
    def handle_events(self, player, stock_manager) -> List[str]:
        """
        Handle all random events that can occur during the game.
        
        Args:
            player: Player object
            stock_manager: StockManager object
            
        Returns:
            List[str]: List of event messages to display to the player
        """
        news_reports = []
        
        # Handle market events
        market_msg = self._handle_market_events(player, stock_manager)
        if market_msg:
            news_reports.append(f"【Market News】{market_msg}")
        
        # Handle health events
        health_msg = self._handle_health_events(player)
        if health_msg:
            news_reports.append(f"【Health Event】{health_msg}")
        
        # Handle money events
        money_msg = self._handle_money_events(player)
        if money_msg:
            news_reports.append(f"【Financial Event】{money_msg}")
        
        # Handle hacker events if enabled
        if player.hacker_actions_enabled:
            hacker_msg = self._handle_hacker_events(player)
            if hacker_msg:
                news_reports.append(f"【Hacker Event】{hacker_msg}")
        
        return news_reports
    
    def _handle_market_events(self, player, stock_manager) -> str:
        """
        Handle market events that affect stock prices and quantities.
        
        Args:
            player: Player object
            stock_manager: StockManager object
            
        Returns:
            str: Event message if an event occurred, None otherwise
        """
        for event in self.market_events:
            if random.randint(0, 950) % event["freq"] == 0:
                stock_id = event["stock_id"]
                
                # Skip if stock not available
                if not stock_manager.available_stocks.get(stock_id, False):
                    continue
                
                # Get stock
                stock = stock_manager.stock_types[stock_id]
                
                # Apply event effects
                if event["multiply"] > 0:
                    stock.multiply_price(event["multiply"])
                
                if event["divide"] > 0:
                    stock.divide_price(event["divide"])
                
                if event["add"] > 0:
                    # Special case for the last event (adds debt)
                    if event == self.market_events[-1]:
                        player.debt += 2500
                    
                    # Add stock to portfolio if player has space
                    add_count = min(event["add"], player.portfolio_capacity - player.portfolio_used)
                    if add_count > 0:
                        player.add_to_portfolio(
                            stock_id,
                            stock.ticker,
                            stock.name,
                            add_count,
                            0  # Free stocks
                        )
                
                # Return the event message
                return event["msg"]
        
        return None
    
    def _handle_health_events(self, player) -> str:
        """
        Handle health events that affect player health.
        
        Args:
            player: Player object
            
        Returns:
            str: Event message if an event occurred, None otherwise
        """
        for event in self.health_events:
            if random.randint(0, 1000) % event["freq"] == 0:
                # Apply health damage
                player.health -= event["damage"]
                
                # Check if player needs medical care
                if player.health < 85 and player.days_left > 3:
                    # Player needs medical care
                    delay_days = 1 + random.randint(0, 1)
                    
                    # Calculate medical cost
                    medical_cost = delay_days * (1000 + random.randint(0, 8500))
                    
                    # Add to debt
                    player.debt += medical_cost
                    
                    # Increase health
                    player.health += 10
                    if player.health > 100:
                        player.health = 100
                    
                    # Decrease days left
                    player.days_left -= delay_days
                    
                    # Return the event message
                    return f"Your health deteriorated and you were rushed to the hospital. The doctor says you need {delay_days} days of rest.\n" \
                           f"While unconscious, you received IV fluids and treatment.\n" \
                           f"Your insurance has a high deductible, so you now owe ${medical_cost} in medical bills."
                
                # Return the event message
                return f"{event['msg']}\nYour health decreased by {event['damage']} points."
        
        return None
    
    def _handle_money_events(self, player) -> str:
        """
        Handle money events that affect player cash.
        
        Args:
            player: Player object
            
        Returns:
            str: Event message if an event occurred, None otherwise
        """
        for event in self.money_events:
            if random.randint(0, 1000) % event["freq"] == 0:
                # Calculate money loss
                money_loss = (player.cash * event["ratio"]) // 100
                
                # Apply money loss
                player.cash -= money_loss
                if player.cash < 0:
                    player.cash = 0
                
                # Return the event message
                return f"{event['msg']}\nYou lost {event['ratio']}% of your cash."
        
        return None
    
    def _handle_hacker_events(self, player) -> str:
        """
        Handle hacker events that affect player's bank savings.
        
        Args:
            player: Player object
            
        Returns:
            str: Event message if an event occurred, None otherwise
        """
        if random.randint(0, 1000) % 25 == 0:
            if player.bank_savings < 1000:
                return None
            
            if player.bank_savings > 100000:
                # Large savings, can lose or gain money
                amount = player.bank_savings // (2 + random.randint(0, 19))
                
                if random.randint(0, 20) % 3 != 0:
                    # Lose money
                    player.bank_savings -= amount
                    return f"Hackers breached your bank's network and modified the database. Your savings decreased by ${amount}."
                else:
                    # Gain money
                    player.bank_savings += amount
                    return f"Hackers breached your bank's network and modified the database. Your savings increased by ${amount}!"
            else:
                # Smaller savings, always gain money
                amount = player.bank_savings // (1 + random.randint(0, 14))
                player.bank_savings += amount
                return f"Hackers breached your bank's network and modified the database. Your savings increased by ${amount}!"
        
        return None
