#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Locations module for Yolo Terminal game.
Simplified to just handle days instead of locations.
"""

from typing import Dict, List, Optional, Tuple
import questionary

class DayManager:
    """
    DayManager class to manage days in the game.
    """
    
    def __init__(self):
        """Initialize the day manager."""
        pass
    
    def get_current_day(self, player) -> int:
        """
        Get the current day number.
        
        Args:
            player: Player object
            
        Returns:
            int: Current day number (1-40)
        """
        return 41 - player.days_left
    
    def get_day_description(self, player) -> str:
        """
        Get a description of the current day.
        
        Args:
            player: Player object
            
        Returns:
            str: Description of the current day
        """
        day = self.get_current_day(player)
        
        if day == 1:
            return "Day 1 - Your trading journey begins"
        elif day < 10:
            return f"Day {day} - Early days of trading"
        elif day < 20:
            return f"Day {day} - Building your portfolio"
        elif day < 30:
            return f"Day {day} - Advancing your strategy"
        elif day < 40:
            return f"Day {day} - Final stretch"
        else:
            return f"Day {day} - Last day of trading"
