# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class NormalItemTest(unittest.TestCase):
    """Tests for normal items"""

    def test_quality_decreases_by_1(self):
        items = [Item("Normal Item", 10, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(19, items[0].quality)

    def test_sell_in_decreases_by_1(self):
        items = [Item("Normal Item", 10, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(9, items[0].sell_in)

    def test_quality_degrades_twice_as_fast_after_sell_by(self):
        items = [Item("Normal Item", 0, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(18, items[0].quality)

    def test_quality_never_negative(self):
        items = [Item("Normal Item", 5, 0)]
        GildedRose(items).update_quality()
        self.assertEqual(0, items[0].quality)

    def test_quality_never_negative_when_expired(self):
        items = [Item("Normal Item", 0, 1)]
        GildedRose(items).update_quality()
        self.assertEqual(0, items[0].quality)


class AgedBrieTest(unittest.TestCase):
    """Tests for Aged Brie"""

    def test_quality_increases_with_age(self):
        items = [Item("Aged Brie", 10, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(21, items[0].quality)

    def test_quality_increases_twice_after_sell_by(self):
        items = [Item("Aged Brie", 0, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(22, items[0].quality)

    def test_quality_never_exceeds_50(self):
        items = [Item("Aged Brie", 10, 50)]
        GildedRose(items).update_quality()
        self.assertEqual(50, items[0].quality)

    def test_quality_never_exceeds_50_when_expired(self):
        items = [Item("Aged Brie", 0, 49)]
        GildedRose(items).update_quality()
        self.assertEqual(50, items[0].quality)


class SulfurasTest(unittest.TestCase):
    """Tests for Sulfuras, Hand of Ragnaros"""

    def test_quality_never_changes(self):
        items = [Item("Sulfuras, Hand of Ragnaros", 5, 80)]
        GildedRose(items).update_quality()
        self.assertEqual(80, items[0].quality)

    def test_sell_in_never_changes(self):
        items = [Item("Sulfuras, Hand of Ragnaros", 5, 80)]
        GildedRose(items).update_quality()
        self.assertEqual(5, items[0].sell_in)

    def test_quality_stays_80_when_expired(self):
        items = [Item("Sulfuras, Hand of Ragnaros", -1, 80)]
        GildedRose(items).update_quality()
        self.assertEqual(80, items[0].quality)


class BackstagePassTest(unittest.TestCase):
    """Tests for Backstage passes"""

    def test_quality_increases_by_1_when_more_than_10_days(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 15, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(21, items[0].quality)

    def test_quality_increases_by_2_when_10_days_or_less(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 10, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(22, items[0].quality)

    def test_quality_increases_by_3_when_5_days_or_less(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(23, items[0].quality)

    def test_quality_drops_to_0_after_concert(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 0, 50)]
        GildedRose(items).update_quality()
        self.assertEqual(0, items[0].quality)

    def test_quality_never_exceeds_50(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 49)]
        GildedRose(items).update_quality()
        self.assertEqual(50, items[0].quality)


class ConjuredItemTest(unittest.TestCase):
    """Tests for Conjured items (new feature)"""

    def test_quality_degrades_by_2(self):
        items = [Item("Conjured Mana Cake", 10, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(18, items[0].quality)

    def test_quality_degrades_by_4_after_sell_by(self):
        items = [Item("Conjured Mana Cake", 0, 20)]
        GildedRose(items).update_quality()
        self.assertEqual(16, items[0].quality)

    def test_quality_never_negative(self):
        items = [Item("Conjured Mana Cake", 5, 1)]
        GildedRose(items).update_quality()
        self.assertEqual(0, items[0].quality)

    def test_quality_never_negative_when_expired(self):
        items = [Item("Conjured Mana Cake", 0, 3)]
        GildedRose(items).update_quality()
        self.assertEqual(0, items[0].quality)


if __name__ == '__main__':
    unittest.main()