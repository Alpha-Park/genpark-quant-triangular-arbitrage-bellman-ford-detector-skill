# -*- coding: utf-8 -*-
import sys, json
from client import GenParkQuantTriangularArbitrageBellmanFordDetector

detector = GenParkQuantTriangularArbitrageBellmanFordDetector()

def run_tool(name, args):
    if name == "detect_arbitrage_cycles":
        tickers = args.get("tickers", [])
        return detector.detect_arbitrage_cycles(tickers)
    else:
        raise ValueError(f"Unknown tool: {name}")

def main():
    if "--test" in sys.argv:
        print("[TEST] Running GenPark Triangular Arbitrage Bellman-Ford Self-Test...")
        # Artificially mispriced triangular loop: EUR/USD, USD/JPY, EUR/JPY
        tickers = [
            {"pair": "EUR/USD", "rate": 1.10, "fee": 0.0001},
            {"pair": "USD/JPY", "rate": 150.0, "fee": 0.0001},
            {"pair": "EUR/JPY", "rate": 160.0, "fee": 0.0001}
        ]
        res = detector.detect_arbitrage_cycles(tickers)
        assert "has_arbitrage" in res
        print("[TEST] All tests passed successfully!")
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            res = run_tool(req.get("name"), req.get("arguments", {}))
            print(json.dumps({"jsonrpc": "2.0", "id": req.get("id"), "result": res}))
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}))
        sys.stdout.flush()

if __name__ == "__main__":
    main()
