#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bank module for Yolo Terminal game.
Handles banking operations.
"""

from typing import Dict, List, Optional, Tuple, Any

class Bank:
    """
    Bank class to handle banking operations.
    """
    
    def __init__(self):
        """Initialize the bank."""
        self.deposit_interest_rate = 0.01  # 1% interest on deposits
        self.debt_interest_rate = 0.10  # 10% interest on debt
    
    def update_interest(self, player) -> None:
        """
        Update interest on player's bank savings and debt.
        
        Args:
            player: Player object
        """
        # Update bank savings interest
        player.bank_savings += int(player.bank_savings * self.deposit_interest_rate)
        
        # Update debt interest
        player.debt += int(player.debt * self.debt_interest_rate)
    
    def visit(self, player, ui, logger=None) -> None:
        """
        Handle player's visit to the bank.
        
        Args:
            player: Player object
            ui: UI object for user interaction
            logger: GameLogger object for logging (optional)
        """
        ui.clear_screen()
        ui.show_message("Welcome to the Bank!")
        
        while True:
            ui.clear_screen()
            print(f"Cash: ${player.cash}")
            print(f"Bank Savings: ${player.bank_savings}")
            print(f"Student Loan Debt: ${player.debt}")
            print("\nBank Menu:")
            print("  1. Deposit")
            print("  2. Withdraw")
            print("  3. Pay Loan")
            print("  0. Exit")
            
            choice = ui.get_input("Select an option: ", input_type=int, default=0, min_value=0, max_value=3)
            
            if choice == 0:
                break
            elif choice == 1:
                self._deposit(player, ui, logger)
            elif choice == 2:
                self._withdraw(player, ui, logger)
            elif choice == 3:
                self._repay_debt(player, ui, logger)
    
    def _deposit(self, player, ui, logger=None) -> None:
        """
        Handle player's deposit to the bank.
        
        Args:
            player: Player object
            ui: UI object for user interaction
            logger: GameLogger object for logging (optional)
        """
        if player.cash <= 0:
            ui.show_message("You don't have any cash to deposit.")
            return
        
        amount = ui.get_input(f"How much would you like to deposit? (max ${player.cash}): ", 
                             input_type=int, default=0, min_value=0, max_value=player.cash)
        
        if amount <= 0:
            return
        
        player.cash -= amount
        player.bank_savings += amount
        
        # Log the transaction if logger is provided
        if logger:
            logger.log_bank_transaction(player, "DEPOSIT", amount)
        
        ui.show_message(f"You deposited ${amount}. New balance: ${player.bank_savings}")
    
    def _withdraw(self, player, ui, logger=None) -> None:
        """
        Handle player's withdrawal from the bank.
        
        Args:
            player: Player object
            ui: UI object for user interaction
            logger: GameLogger object for logging (optional)
        """
        if player.bank_savings <= 0:
            ui.show_message("You don't have any savings to withdraw.")
            return
        
        amount = ui.get_input(f"How much would you like to withdraw? (max ${player.bank_savings}): ", 
                             input_type=int, default=0, min_value=0, max_value=player.bank_savings)
        
        if amount <= 0:
            return
        
        player.bank_savings -= amount
        player.cash += amount
        
        # Log the transaction if logger is provided
        if logger:
            logger.log_bank_transaction(player, "WITHDRAW", amount)
        
        ui.show_message(f"You withdrew ${amount}. New balance: ${player.bank_savings}")
    
    def _repay_debt(self, player, ui, logger=None) -> None:
        """
        Handle player's debt repayment.
        
        Args:
            player: Player object
            ui: UI object for user interaction
            logger: GameLogger object for logging (optional)
        """
        if player.debt <= 0:
            ui.show_message("You don't have any student loan debt to repay.")
            return
        
        if player.cash <= 0:
            ui.show_message("You don't have any cash to repay your debt.")
            return
        
        max_repay = min(player.cash, player.debt)
        amount = ui.get_input(f"How much debt would you like to repay? (max ${max_repay}): ", 
                             input_type=int, default=0, min_value=0, max_value=max_repay)
        
        if amount <= 0:
            return
        
        player.cash -= amount
        player.debt -= amount
        
        # Log the transaction if logger is provided
        if logger:
            logger.log_bank_transaction(player, "REPAY", amount)
        
        ui.show_message(f"You repaid ${amount} of your student loan. Remaining debt: ${player.debt}")
