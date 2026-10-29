# -*- coding: utf-8 -*-
from client import GenParkQuantTriangularArbitrageBellmanFordDetector

def main():
    detector = GenParkQuantTriangularArbitrageBellmanFordDetector(default_fee=0.0005)
    print("=== GenPark Quant Triangular Arbitrage Detector ===")

    # Market ticker snapshot: BTC/USDT, ETH/USDT, ETH/BTC
    tickers = [
        {"pair": "BTC/USDT", "rate": 65000.0},
        {"pair": "ETH/USDT", "rate": 3300.0},
        {"pair": "ETH/BTC", "rate": 0.052} # 3300 / 65000 = 0.05077; 0.052 represents 2.4% price dislocation!
    ]

    res = detector.detect_arbitrage_cycles(tickers)
    print(f"Arbitrage Found: {res['has_arbitrage']}")
    if res["has_arbitrage"]:
        print(f"Net Profit Margin: +{res['net_roi_pct']}%")
        print(f"Optimal Execution Loop: {' -> '.join(res['cycle_path'])}")

if __name__ == "__main__":
    main()
