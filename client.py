# -*- coding: utf-8 -*-
"""
GenPark Quant Triangular Arbitrage Bellman-Ford Detector
Standard Library only: math, typing.
Constructs directed currency exchange graph with negative logarithm edge weights,
detects negative weight cycles (profitable arbitrage loops), and computes net ROI.
"""

import math
from typing import Dict, List, Tuple, Any

class GenParkQuantTriangularArbitrageBellmanFordDetector:
    def __init__(self, default_fee: float = 0.001):
        self.default_fee = default_fee

    def detect_arbitrage_cycles(self, tickers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        tickers: list of {"pair": "ETH/USDT", "rate": 3200.0, "fee": 0.001}
        Each pair A/B with rate R represents: 1 A = R B (forward) and 1 B = (1/R) A (inverse).
        """
        vertices = set()
        edges = [] # list of (u, v, weight, rate, fee)

        for item in tickers:
            base, quote = item["pair"].split("/")
            rate = float(item["rate"])
            fee = float(item.get("fee", self.default_fee))

            vertices.add(base)
            vertices.add(quote)

            # Forward edge base -> quote: get R * (1 - fee) quote for 1 base
            eff_rate_fwd = rate * (1.0 - fee)
            w_fwd = -math.log(eff_rate_fwd)
            edges.append((base, quote, w_fwd, eff_rate_fwd, fee))

            # Inverse edge quote -> base: get (1 / rate) * (1 - fee) base for 1 quote
            eff_rate_inv = (1.0 / rate) * (1.0 - fee)
            w_inv = -math.log(eff_rate_inv)
            edges.append((quote, base, w_inv, eff_rate_inv, fee))

        vert_list = list(vertices)
        if not vert_list:
            return {"has_arbitrage": False, "opportunities": []}

        source = vert_list[0]
        dist = {v: float('inf') for v in vertices}
        parent = {v: None for v in vertices}
        edge_used = {v: None for v in vertices}
        dist[source] = 0.0

        # Relax |V| - 1 times
        for _ in range(len(vertices) - 1):
            for u, v, w, eff_r, fee in edges:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    parent[v] = u
                    edge_used[v] = eff_r

        # N-th relaxation to find negative weight cycle
        cycle_nodes = []
        for u, v, w, eff_r, fee in edges:
            if dist[u] + w < dist[v] - 1e-8:
                # Negative cycle found! Trace back
                curr = v
                for _ in range(len(vertices)):
                    curr = parent[curr]
                
                # Trace cycle
                cycle = [curr]
                nxt = parent[curr]
                while nxt != curr and nxt not in cycle:
                    cycle.append(nxt)
                    nxt = parent[nxt]
                cycle.append(curr)
                cycle.reverse()
                cycle_nodes = cycle
                break

        if not cycle_nodes or len(cycle_nodes) < 3:
            return {"has_arbitrage": False, "opportunities": []}

        # Calculate exact multiplier around cycle
        multiplier = 1.0
        cycle_pairs = []
        for i in range(len(cycle_nodes) - 1):
            u = cycle_nodes[i]
            v = cycle_nodes[i+1]
            match = next((e for e in edges if e[0] == u and e[1] == v), None)
            if match:
                multiplier *= match[3]
                cycle_pairs.append(f"{u}->{v}")

        net_roi_pct = round((multiplier - 1.0) * 100, 3)

        return {
            "has_arbitrage": net_roi_pct > 0.0,
            "net_roi_pct": net_roi_pct,
            "cycle_path": cycle_nodes,
            "trade_sequence": cycle_pairs,
            "total_effective_multiplier": round(multiplier, 6)
        }
