#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Broker module for Yolo Terminal game.
Handles debt management.
"""

import random
from typing import Dict, List, Optional, Tuple, Any

class Broker:
    """
    Broker class to handle debt management.
    """
    
    def __init__(self):
        """Initialize the broker."""
        pass
    
    def visit(self, player, ui) -> None:
        """
        Handle player's visit to the broker.
        
        Args:
            player: Player object
            ui: UI object for user interaction
        """
        ui.clear_screen()
        ui.show_message("Welcome to your Student Loan Broker!")
        
        if player.debt <= 0:
            # Player has no debt, show different messages based on wealth
            if player.cash + player.bank_savings < 1000:
                ui.show_message("The broker laughs: You're broke, but at least you're debt-free!")
            elif player.cash + player.bank_savings < 100000:
                ui.show_message("The broker nods: 'Good job on paying off your loans. Here's a $1000 rebate.'")
                player.cash += 1000
            elif player.cash + player.bank_savings < 10000000:
                ui.show_message("The broker whispers into the phone: 'We've got a high-value client here...'")
            else:
                ui.show_message("The broker calls their manager: 'Please escort this client to the VIP section.'")
            return
        
        # Player has debt, show debt repayment options
        ui.clear_screen()
        print(f"Your Student Loan Debt: ${player.debt}")
        print(f"Your Cash: ${player.cash}")
        
        if player.cash <= 0:
            ui.show_message("The broker smirks while looking at their Rolex: Want to pay your loans? Try making some money first!")
            return
        
        # Calculate maximum repayment amount
        max_repay = min(player.cash, player.debt)
        
        # Show repayment options
        print("\nRepayment Options:")
        print(f"  1. Pay off all debt (${player.debt})")
        print(f"  2. Pay half of debt (${player.debt // 2})")
        print(f"  3. Pay quarter of debt (${player.debt // 4})")
        print(f"  4. Custom payment amount (max ${max_repay})")
        print("  0. Exit")
        
        choice = ui.get_input("Select an option: ", input_type=int, default=0, min_value=0, max_value=4)
        
        if choice == 0:
            return
        
        # Calculate repayment amount based on choice
        if choice == 1:
            amount = player.debt
        elif choice == 2:
            amount = player.debt // 2
        elif choice == 3:
            amount = player.debt // 4
        else:  # choice == 4
            amount = ui.get_input(f"Enter payment amount (max ${max_repay}): ", 
                                 input_type=int, default=0, min_value=0, max_value=max_repay)
        
        # Check if player has enough cash
        if amount > player.cash:
            ui.show_message("The broker smirks while looking at their Rolex: You don't have enough cash for that payment!")
            return
        
        # Confirm repayment
        if not ui.ask_yes_no(f"Confirm payment of ${amount} toward your student loans?"):
            return
        
        # Process repayment
        player.cash -= amount
        player.debt -= amount
        
        ui.show_message(f"You paid ${amount} toward your student loans. Remaining debt: ${player.debt}")
        
        # Special message if debt is fully repaid
        if player.debt <= 0:
            ui.show_message("Congratulations! You've paid off all your student loans!")
