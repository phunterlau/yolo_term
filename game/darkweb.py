#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Darkweb module for Yolo Terminal game.
Handles darkweb hacking facility activities.
"""

import random
from typing import Dict, List, Optional, Tuple, Any

class Darkweb:
    """
    Darkweb class to handle darkweb hacking facility activities.
    """
    
    def __init__(self):
        """Initialize the darkweb."""
        self.entry_fee = 15  # Cost to access the darkweb
        self.max_visits = 3  # Maximum number of visits allowed
        
        # Tips that can be shown in the darkweb
        self.tips = [
            "Trading stocks is a great way to make money, but watch out for SEC investigations.",
            "If your health drops below 85, you might be hospitalized, which costs money and time.",
            "Student loan debt increases over time due to interest, pay it off quickly.",
            "Bank savings generate interest, but loan interest rates are higher.",
            "Some market events can dramatically affect stock prices, stay informed.",
            "You can upgrade your trade book size through Robinwood, but it's expensive.",
            "Hospital visits can restore health, but insurance premiums and copays add up.",
            "Your final score is cash + bank savings - debt.",
            "Some stocks are more profitable than others, figure out which ones.",
            "If your health drops to 0, the game ends.",
            "If your debt is too high, you might face financial penalties.",
            "Enabling hacker actions can affect your bank savings, but it's risky.",
            "The market is volatile - prices change daily.",
            "Buy low, sell high is the key to success.",
            "Diversify your portfolio to minimize risk."
        ]
        
        # News that can be shown in the darkweb
        self.news = [
            "SEC announces investigation into market manipulation of certain tech stocks.",
            "Cryptocurrency regulations tightening, prices expected to fluctuate.",
            "Major security breach at Super Nicron, stock prices likely to be affected.",
            "nWidia facing class action lawsuit over chip defects.",
            "SBY500 index fund expected to announce record dividends.",
            "Tezla recalls electric vehicles due to battery issues.",
            "PinTuoTuo smartphones gaining market share in college demographic.",
            "Plantir data analytics software found to have security vulnerabilities.",
            "Government crackdown on darkweb activities intensifying.",
            "Healthcare costs rising, insurance premiums expected to increase.",
            "Trading app fees increasing across the industry.",
            "Bank interest rates adjusting due to federal policy changes.",
            "Student loan interest rates expected to rise.",
            "SEC increasing penalties for insider trading.",
            "New trading regulations coming into effect next quarter."
        ]
    
    def visit(self, player, ui) -> None:
        """
        Handle player's visit to the darkweb.
        
        Args:
            player: Player object
            ui: UI object for user interaction
        """
        ui.clear_screen()
        ui.show_message("Welcome to the Darkweb Hacking Facility!")
        
        if player.darkweb_visits >= self.max_visits:
            ui.show_message("The admin says: You've been here too many times today. Come back tomorrow to avoid detection.")
            return
        
        if player.cash < self.entry_fee:
            ui.show_message(f"The admin says: Access costs ${self.entry_fee}, and you don't have enough cash.")
            return
        
        # Pay entry fee
        player.cash -= self.entry_fee
        player.darkweb_visits += 1
        
        # Show darkweb menu
        while True:
            ui.clear_screen()
            print("Darkweb Menu:")
            print("  1. Trading Strategies")
            print("  2. Market Insider Info")
            print("  3. Hacking Operations")
            print("  0. Exit")
            
            choice = ui.get_input("Select an option: ", input_type=int, default=0, min_value=0, max_value=3)
            
            if choice == 0:
                break
            elif choice == 1:
                self._show_tips(player, ui)
            elif choice == 2:
                self._show_news(player, ui)
            elif choice == 3:
                self._hacker_actions(player, ui)
        
        # Give small reward for visiting
        reward = random.randint(1, 10)
        player.cash += reward
        ui.show_message(f"Thanks for visiting! The admin gives you ${reward} for your trouble.")
    
    def _show_tips(self, player, ui) -> None:
        """
        Show random tips to the player.
        
        Args:
            player: Player object
            ui: UI object for user interaction
        """
        ui.clear_screen()
        print("Trading Strategies (from anonymous sources):")
        
        # Show 3 random tips
        shown_tips = []
        for _ in range(3):
            tip = random.choice(self.tips)
            while tip in shown_tips:
                tip = random.choice(self.tips)
            shown_tips.append(tip)
            print(f"- {tip}")
        
        input("\nPress Enter to continue...")
    
    def _show_news(self, player, ui) -> None:
        """
        Show random news to the player.
        
        Args:
            player: Player object
            ui: UI object for user interaction
        """
        ui.clear_screen()
        print("Market Insider Information (unverified):")
        
        # Show 2 random news
        shown_news = []
        for _ in range(2):
            news = random.choice(self.news)
            while news in shown_news:
                news = random.choice(self.news)
            shown_news.append(news)
            print(f"- {news}")
        
        input("\nPress Enter to continue...")
    
    def _hacker_actions(self, player, ui) -> None:
        """
        Handle hacker actions.
        
        Args:
            player: Player object
            ui: UI object for user interaction
        """
        ui.clear_screen()
        
        if not player.hacker_actions_enabled:
            if not ui.ask_yes_no("WARNING: Hacking operations can affect your bank account balance, with both positive and negative outcomes. Enable hacking operations?"):
                return
            
            player.hacker_actions_enabled = True
            ui.show_message("Hacking operations enabled. Your bank account may now be subject to random modifications.")
        else:
            ui.show_message("Hacking operations are already enabled. Your bank account may be subject to random modifications.")
