#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hospital module for Yolo Terminal game.
Handles health management with insurance premiums and copays.
"""

from typing import Dict, List, Optional, Tuple, Any

class Hospital:
    """
    Hospital class to handle health management.
    """
    
    def __init__(self):
        """Initialize the hospital."""
        self.treatment_cost_per_point = 3500  # Base cost per health point
        self.insurance_premium = 500  # Insurance premium per visit
        self.copay_percentage = 20  # Copay percentage (20%)
    
    def visit(self, player, ui) -> None:
        """
        Handle player's visit to the hospital.
        
        Args:
            player: Player object
            ui: UI object for user interaction
        """
        ui.clear_screen()
        ui.show_message("Welcome to the Hospital!")
        
        if player.health >= 100:
            ui.show_message("The doctor says: You're in perfect health, no treatment needed.")
            return
        
        # Calculate treatment options
        max_treatment = 100 - player.health
        
        # Calculate costs with insurance
        premium_cost = self.insurance_premium
        treatment_costs = []
        
        for i in range(1, max_treatment + 1):
            if i % 5 == 0 or i == max_treatment:
                base_cost = i * self.treatment_cost_per_point
                copay_cost = int(base_cost * (self.copay_percentage / 100))
                total_cost = premium_cost + copay_cost
                treatment_costs.append((i, copay_cost, total_cost))
        
        # Check if player can afford any treatment
        if not treatment_costs or player.cash < treatment_costs[0][2]:
            ui.show_message("The doctor says: You can't afford any treatment with your current insurance plan!")
            return
        
        # Show treatment options
        ui.clear_screen()
        print(f"Your Health: {player.health}/100")
        print(f"Your Cash: ${player.cash}")
        print(f"Insurance Premium: ${premium_cost}")
        print(f"Copay: {self.copay_percentage}% of treatment cost")
        print("\nTreatment Options:")
        
        options = []
        for i, (health_points, copay, total_cost) in enumerate(treatment_costs, 1):
            if total_cost <= player.cash:
                options.append((health_points, copay, total_cost))
                print(f"  {i}. Recover {health_points} health points - Copay: ${copay} - Total: ${total_cost}")
        
        if not options:
            ui.show_message("The doctor says: You can't afford any treatment with your current insurance plan!")
            return
        
        print("  0. Exit")
        
        choice = ui.get_input("Select a treatment plan: ", input_type=int, default=0, min_value=0, max_value=len(options))
        
        if choice == 0:
            return
        
        # Apply treatment
        health_points, copay, total_cost = options[choice - 1]
        
        if not ui.ask_yes_no(f"Confirm spending ${total_cost} to recover {health_points} health points?"):
            return
        
        player.cash -= total_cost
        player.health += health_points
        
        ui.show_message(f"Treatment complete! Your health is now {player.health}/100")
