# -*- coding: utf-8 -*-
"""
Gilded Rose Inventory Management System

This module implements an inventory system that updates item quality based on
Gilded Rose business rules. Different item types have different degradation
strategies implemented using the Strategy pattern.
"""

from typing import List


class Item:
    """Represents an item in the inventory with name, sell_in date, and quality."""

    def __init__(self, name: str, sell_in: int, quality: int) -> None:
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self) -> str:
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


# -- Strategy Pattern: Each item type has its own update strategy --


class ItemUpdater:
    """Base interface for item update strategies."""

    def update(self, item: Item) -> None:
        """Apply daily quality update rules to an item."""
        raise NotImplementedError

    @staticmethod
    def _increase_quality(item: Item, increase_rate: int) -> None:
        """Increase quality by specified amount, clamped to maximum of 50."""
        item.quality = min(50, item.quality + increase_rate)

    @staticmethod
    def _decrease_quality(item: Item, degradation_rate: int) -> None:
        """Decrease quality by specified amount, clamped to minimum of 0."""
        item.quality = max(0, item.quality - degradation_rate)


class NormalItemUpdater(ItemUpdater):
    """
    Normal items strategy.
    
    - Quality decreases by 1 per day
    - Quality decreases by 2 per day after sell date has passed
    - Quality never goes below 0
    """

    def update(self, item: Item) -> None:
        self._decrease_quality(item, degradation_rate=1)
        item.sell_in -= 1
        if item.sell_in < 0:
            self._decrease_quality(item, degradation_rate=1)


class AgedBrieUpdater(ItemUpdater):
    """
    Aged Brie strategy.
    
    - Quality increases by 1 per day (improves with age)
    - Quality increases by 2 per day after sell date has passed
    - Quality never exceeds 50
    """

    def update(self, item: Item) -> None:
        self._increase_quality(item, increase_rate=1)
        item.sell_in -= 1
        if item.sell_in < 0:
            self._increase_quality(item, increase_rate=1)


class SulfurasUpdater(ItemUpdater):
    """
    Sulfuras strategy (legendary item).
    
    - Quality never changes (stays at 80)
    - Sell date never changes (never needs to be sold)
    """

    def update(self, item: Item) -> None:
        # Legendary item: no updates needed
        pass


class BackstagePassUpdater(ItemUpdater):
    """
    Backstage pass strategy.
    
    - Quality increases by 1 per day when more than 10 days until concert
    - Quality increases by 2 per day when 10 days or less until concert
    - Quality increases by 3 per day when 5 days or less until concert
    - Quality drops to 0 after the concert (SellIn <= 0)
    - Quality never exceeds 50 before concert
    """

    def update(self, item: Item) -> None:
        if item.sell_in > 0:
            # Concert has not happened yet, increase quality based on days remaining
            self._increase_quality(item, increase_rate=1)
            if item.sell_in <= 10:
                self._increase_quality(item, increase_rate=1)
            if item.sell_in <= 5:
                self._increase_quality(item, increase_rate=1)

        item.sell_in -= 1

        if item.sell_in < 0:
            # Concert has passed, quality drops to worthless
            item.quality = 0


class ConjuredItemUpdater(ItemUpdater):
    """
    Conjured items strategy.
    
    - Quality decreases by 2 per day (twice as fast as normal items)
    - Quality decreases by 4 per day after sell date has passed
    - Quality never goes below 0
    """

    def update(self, item: Item) -> None:
        self._decrease_quality(item, degradation_rate=2)
        item.sell_in -= 1
        if item.sell_in < 0:
            self._decrease_quality(item, degradation_rate=2)


# -- Factory Pattern: Selects the correct strategy based on item name --


class ItemUpdaterFactory:
    """
    Factory for creating the appropriate ItemUpdater strategy for a given item.
    
    Maps item names to their corresponding update strategies. Supports exact matches
    and prefix matching for Conjured items (all "Conjured *" items use same rules).
    """

    # Mapping of exact item names to their updater classes
    _UPDATER_MAP = {
        "Aged Brie": AgedBrieUpdater,
        "Sulfuras, Hand of Ragnaros": SulfurasUpdater,
        "Backstage passes to a TAFKAL80ETC concert": BackstagePassUpdater,
        "Conjured Mana Cake": ConjuredItemUpdater,
    }

    @classmethod
    def create(cls, item: Item) -> ItemUpdater:
        """
        Create and return the appropriate updater for the given item.
        
        Args:
            item: The item to create an updater for
            
        Returns:
            An ItemUpdater instance appropriate for this item's type
        """
        # First, try exact name match
        updater_class = cls._UPDATER_MAP.get(item.name)
        
        # If no exact match, check for Conjured prefix
        if updater_class is None and item.name.startswith("Conjured"):
            updater_class = ConjuredItemUpdater
        
        # Default to normal items if no specific strategy found
        if updater_class is None:
            updater_class = NormalItemUpdater
            
        return updater_class()


# -- Main class --


class GildedRose:
    """
    Main inventory system that updates item qualities according to Gilded Rose rules.
    
    Uses the Strategy pattern to apply different update rules based on item type,
    keeping the main logic clean and separation of concerns clear.
    """

    def __init__(self, items: List[Item]) -> None:
        """
        Initialize the Gilded Rose store with a list of items.
        
        Args:
            items: List of Item objects to manage
        """
        self.items = items

    def update_quality(self) -> None:
        """
        Update the quality of all items according to their type-specific rules.
        
        Each item is processed through its corresponding strategy which handles
        quality degradation, quality bounds checking, and sell date adjustments.
        """
        for item in self.items:
            updater = ItemUpdaterFactory.create(item)
            updater.update(item)