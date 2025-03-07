#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trading App module for Yolo Terminal game.
Handles increasing player's portfolio capacity.
"""

from typing import Dict, List, Optional, Tuple, Any

class TradingApp:
    """
    TradingApp class to handle increasing player's portfolio capacity.
    """
    
    def __init__(self):
        """Initialize the trading app."""
        self.upgrade_cost = 30000  # Cost to upgrade trade book
        self.upgrade_amount = 10  # Amount of capacity increase per upgrade
        self.max_capacity = 140  # Maximum portfolio capacity
    
    def visit(self, player, ui) -> None:
        """
        Handle player's visit to the trading app.
        
        Args:
            player: Player object
            ui: UI object for user interaction
        """
        ui.clear_screen()
        ui.show_message("Welcome to Robinwood Trading App!")
        
        if player.portfolio_capacity >= self.max_capacity:
            ui.show_message("The app says: You already have our maximum trade book size. We can't offer any further upgrades.")
            return
        
        if player.cash < self.upgrade_cost:
            ui.show_message(f"The app says: You don't have enough cash to upgrade your trade book. You need at least ${self.upgrade_cost}.")
            return
        
        # Calculate upgrade cost based on player's wealth
        actual_cost = self.upgrade_cost
        if player.cash > self.upgrade_cost * 2:
            actual_cost = player.cash // 2  # If player is rich, charge more
        
        if not ui.ask_yes_no(f"Robinwood Premium offers to increase your trade book capacity from {player.portfolio_capacity} to {player.portfolio_capacity + self.upgrade_amount} for ${actual_cost}. Upgrade?"):
            return
        
        # Apply upgrade
        player.cash -= actual_cost
        player.portfolio_capacity += self.upgrade_amount
        
        ui.show_message(f"Upgrade complete! Your trade book capacity is now {player.portfolio_capacity}")
