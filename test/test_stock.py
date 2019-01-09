from stock import Stock_Exchange, trade_book

import unittest


class TestStock(unittest.TestCase):
    
    def setUp(self):
        self.se = Stock_Exchange()
    
    def test_calculate_dividend(self):
        """
        Test dividend amount
        """
        divident = self.se.calculate_dividend(10, 'ALE')
        self.assertEqual(2.3, divident)

    def test_calculate_dividend_zero(self):
        """
        Test dividend amount having zero
        """
        divident = self.se.calculate_dividend(0, 'ALE')
        self.assertEqual(0.0, divident)

    def test_calculate_pe(self):
        """
        Test  P/E ratio
        """
        pe = self.se.calculate_pe(100, 'POP')
        self.assertEqual(12.5, pe)

    def test_calculate_pe_zero(self):
        """
        Test  P/E ratio with zero
        """
        pe = self.se.calculate_pe(0, 'ALE')
        self.assertEqual(0, pe)

    def test_trade_book(self):
        """
        Test trade book entry
        """
        self.se.register_trade(5, 'ALE', 10, 'B')
        entry = trade_book[0][:4]
        self.assertEqual(['ALE', 5, 10, 'B'], entry)

    def test_volume_weight_stock_price(self):
        """
        Test volume weighted stock price
        """
        self.se.register_trade(2, 'ALE', 10, 'S')
        vwsp = self.se.volume_weight_stock_price('ALE')
        self.assertEqual(7.0, vwsp)

    def test_geometric_mean(self):
        """
        Test geometric mean
        """
        gmean = self.se.geometric_mean()
        self.assertEqual(1, gmean)
        
    def tearDown(self):
        self.se = None
