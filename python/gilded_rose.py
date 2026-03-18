# -*- coding: utf-8 -*-


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


# -- Strategy Pattern: each item type has its own update strategy --


class NormalItemUpdater:
    """Normal items: quality -1 per day, -2 after expired, min 0"""

    def update(self, item):
        item.quality = max(0, item.quality - 1)
        item.sell_in -= 1
        if item.sell_in < 0:
            item.quality = max(0, item.quality - 1)


class AgedBrieUpdater:
    """Aged Brie: quality increases over time, +2 after expired, max 50"""

    def update(self, item):
        item.quality = min(50, item.quality + 1)
        item.sell_in -= 1
        if item.sell_in < 0:
            item.quality = min(50, item.quality + 1)


class SulfurasUpdater:
    """Sulfuras: legendary item, never changes"""

    def update(self, item):
        pass


class BackstagePassUpdater:
    """Backstage passes: quality increases as concert approaches, drops to 0 after"""

    def update(self, item):
        if item.sell_in <= 0:
            # Concert already happened, do nothing before sell_in update
            pass
        else:
            item.quality = min(50, item.quality + 1)
            if item.sell_in <= 10:
                item.quality = min(50, item.quality + 1)
            if item.sell_in <= 5:
                item.quality = min(50, item.quality + 1)

        item.sell_in -= 1

        if item.sell_in < 0:
            item.quality = 0


class ConjuredItemUpdater:
    """Conjured items: degrade twice as fast as normal items"""

    def update(self, item):
        item.quality = max(0, item.quality - 2)
        item.sell_in -= 1
        if item.sell_in < 0:
            item.quality = max(0, item.quality - 2)


# -- Factory Pattern: selects the correct strategy based on item name --


class ItemUpdaterFactory:
    _updaters = {
        "Aged Brie": AgedBrieUpdater,
        "Sulfuras, Hand of Ragnaros": SulfurasUpdater,
        "Backstage passes to a TAFKAL80ETC concert": BackstagePassUpdater,
        "Conjured Mana Cake": ConjuredItemUpdater,
    }

    @classmethod
    def create(cls, item):
        updater_class = cls._updaters.get(item.name)
        if updater_class is None and item.name.startswith("Conjured"):
            updater_class = ConjuredItemUpdater
        if updater_class is None:
            updater_class = NormalItemUpdater
        return updater_class()


# -- Main class --


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            updater = ItemUpdaterFactory.create(item)
            updater.update(item)