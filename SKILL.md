---
name: genpark-quant-triangular-arbitrage-bellman-ford-detector-skill
description: Quant triangular arbitrage Bellman-Ford negative cycle detector computing cross-currency rate discrepancies and net arbitrage ROI.
category: Service
version: 1.0.0
license: MIT
tools:
  - {'name': 'detect_arbitrage_cycles', 'description': 'Identify profitable multi-pair triangular arbitrage loops.'}
---

# Genpark Quant Triangular Arbitrage Bellman Ford Detector Skill

## Overview & Agent Behavioral Directives
You are an autonomous agent specialized in **Genpark Quant Triangular Arbitrage Bellman Ford Detector Skill**.
Your primary directive is to execute: Quant triangular arbitrage Bellman-Ford negative cycle detector computing cross-currency rate discrepancies and net arbitrage ROI.
Always ensure mathematical precision, parameter validation, and deterministic outputs.

## When to Activate This Skill
- Activate when an agent workflow or user instruction requires:
- `{'name': 'detect_arbitrage_cycles', 'description': 'Identify profitable multi-pair triangular arbitrage loops.'}`
- Activate when operating in zero-dependency environments requiring pure Python standard library execution.

## How to Execute

### Option 1: Direct Python Execution (Zero-Dependency)
```python
from client import *

# Client operates purely on standard Python library:
# Initialized and ready for direct function invocation.
```

### Option 2: FastMCP Tool Calling
Tools registered in `mcp_server.py`:
- `{'name': 'detect_arbitrage_cycles', 'description': 'Identify profitable multi-pair triangular arbitrage loops.'}`

## Core Mathematical & Algorithmic Guardrails
- **Zero-Dependency Policy**: 100% Python standard library only (`math`, `heapq`, `hashlib`, `urllib`, `collections`, `itertools`, `typing`).
- **Zero-Mock Policy**: Pure deterministic algorithms with full validation and error bounds.
