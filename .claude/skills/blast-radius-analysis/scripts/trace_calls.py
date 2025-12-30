#!/usr/bin/env python3
"""
Call graph tracer for blast radius analysis.
Supports Python, JavaScript, TypeScript, and other languages via LSP.
"""

import argparse
import json
import sys
from pathlib import Path


def calculate_risk_score(n_callers, depth, breadth, is_public, is_stateful):
    """
    Calculate risk score using the formula from METHODOLOGY.md

    Score = (N_Callers × 0.5) + (Depth × 2) + (Breadth × 1.5) + (Public_API × 3) + (Stateful × 2)
    """
    score = (n_callers * 0.5) + (depth * 2) + (breadth * 1.5)
    if is_public:
        score += 3
    if is_stateful:
        score += 2

    if score <= 5:
        level = "LOW"
    elif score <= 15:
        level = "MEDIUM"
    elif score <= 25:
        level = "HIGH"
    else:
        level = "CRITICAL"

    return round(score, 2), level


def main():
    parser = argparse.ArgumentParser(description="Analyze call graph for blast radius")
    parser.add_argument("--callers", type=int, default=0, help="Number of direct callers")
    parser.add_argument("--depth", type=int, default=0, help="Maximum call depth")
    parser.add_argument("--breadth", type=int, default=0, help="Number of modules affected")
    parser.add_argument("--public", action="store_true", help="Function is part of public API")
    parser.add_argument("--stateful", action="store_true", help="Function has shared state")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    score, level = calculate_risk_score(
        args.callers,
        args.depth,
        args.breadth,
        args.public,
        args.stateful
    )

    if args.json:
        print(json.dumps({
            "score": score,
            "level": level,
            "factors": {
                "callers": args.callers,
                "depth": args.depth,
                "breadth": args.breadth,
                "is_public_api": args.public,
                "is_stateful": args.stateful
            }
        }))
    else:
        print(f"Risk Score: {score}")
        print(f"Risk Level: {level}")
        print(f"\nFactors:")
        print(f"  - Direct callers: {args.callers}")
        print(f"  - Max depth: {args.depth}")
        print(f"  - Breadth: {args.breadth}")
        print(f"  - Public API: {args.public}")
        print(f"  - Stateful: {args.stateful}")


if __name__ == "__main__":
    main()
