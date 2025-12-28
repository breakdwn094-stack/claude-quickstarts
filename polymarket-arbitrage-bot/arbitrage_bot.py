#!/usr/bin/env python3
"""
Polymarket Arbitrage Bot

This bot scans Polymarket for arbitrage opportunities where:
- YES price + NO price < $1.00 (guaranteed profit)

Concept: If you can buy YES + NO for less than $1 total, you lock in profit
regardless of outcome since one will always pay out $1.

Example:
- YES = $0.48, NO = $0.49
- Total cost = $0.97
- Guaranteed payout = $1.00
- Profit = $0.03 per share (3%)

Copyright 2024 - MIT License
"""

import os
import sys
import time
import logging
import json
from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from decimal import Decimal, ROUND_DOWN

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('arbitrage_bot.log')
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class ArbitrageOpportunity:
    """Represents an arbitrage opportunity"""
    market_id: str
    market_question: str
    yes_price: float
    no_price: float
    total_cost: float
    profit_per_share: float
    profit_percentage: float
    yes_token_id: str
    no_token_id: str
    volume: float
    liquidity: float
    timestamp: datetime


class PolymarketArbitrageBot:
    """
    Arbitrage bot that scans Polymarket for profitable opportunities.

    The bot looks for markets where YES + NO < $1.00, which guarantees
    a profit regardless of the outcome.
    """

    # API Endpoints
    CLOB_API = "https://clob.polymarket.com"
    GAMMA_API = "https://gamma-api.polymarket.com"

    def __init__(
        self,
        min_profit_threshold: float = 0.01,  # Minimum 1% profit
        min_liquidity: float = 100.0,        # Minimum $100 liquidity
        scan_interval: int = 30,             # Seconds between scans
        execute_trades: bool = False,        # Whether to execute trades
        private_key: Optional[str] = None,   # For trade execution
        max_trade_size: float = 50.0,        # Maximum trade size in USDC
    ):
        """
        Initialize the arbitrage bot.

        Args:
            min_profit_threshold: Minimum profit percentage to consider (0.01 = 1%)
            min_liquidity: Minimum market liquidity in USDC
            scan_interval: Seconds between market scans
            execute_trades: Whether to automatically execute trades
            private_key: Wallet private key (required if execute_trades=True)
            max_trade_size: Maximum trade size per opportunity
        """
        self.min_profit_threshold = min_profit_threshold
        self.min_liquidity = min_liquidity
        self.scan_interval = scan_interval
        self.execute_trades = execute_trades
        self.private_key = private_key or os.getenv("POLYMARKET_PRIVATE_KEY")
        self.max_trade_size = max_trade_size

        # Track opportunities found
        self.opportunities_found: list[ArbitrageOpportunity] = []
        self.total_potential_profit = 0.0

        # Initialize CLOB client if trading is enabled
        self.clob_client = None
        if self.execute_trades:
            self._init_trading_client()

        logger.info("=" * 60)
        logger.info("Polymarket Arbitrage Bot Initialized")
        logger.info("=" * 60)
        logger.info(f"Min profit threshold: {self.min_profit_threshold * 100:.1f}%")
        logger.info(f"Min liquidity: ${self.min_liquidity:.2f}")
        logger.info(f"Scan interval: {self.scan_interval} seconds")
        logger.info(f"Trade execution: {'ENABLED' if self.execute_trades else 'DISABLED (monitoring only)'}")
        logger.info("=" * 60)

    def _init_trading_client(self):
        """Initialize the CLOB client for trading"""
        try:
            from py_clob_client.client import ClobClient

            if not self.private_key:
                logger.warning("No private key provided - trade execution disabled")
                self.execute_trades = False
                return

            self.clob_client = ClobClient(
                self.CLOB_API,
                key=self.private_key,
                chain_id=137,  # Polygon mainnet
                signature_type=0,  # EOA wallet
            )
            self.clob_client.set_api_creds(self.clob_client.create_or_derive_api_creds())
            logger.info("Trading client initialized successfully")

        except ImportError:
            logger.error("py-clob-client not installed. Run: pip install py-clob-client")
            self.execute_trades = False
        except Exception as e:
            logger.error(f"Failed to initialize trading client: {e}")
            self.execute_trades = False

    def fetch_markets(self) -> list[dict]:
        """
        Fetch all active markets from Polymarket.

        Returns:
            List of market dictionaries
        """
        markets = []
        offset = 0
        limit = 100

        try:
            while True:
                # Fetch markets from Gamma API
                response = requests.get(
                    f"{self.GAMMA_API}/markets",
                    params={
                        "active": "true",
                        "closed": "false",
                        "limit": limit,
                        "offset": offset,
                    },
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()

                if not data:
                    break

                markets.extend(data)

                if len(data) < limit:
                    break

                offset += limit
                time.sleep(0.2)  # Rate limiting

            logger.info(f"Fetched {len(markets)} active markets")
            return markets

        except requests.RequestException as e:
            logger.error(f"Failed to fetch markets: {e}")
            return []

    def get_token_prices(self, token_id: str) -> tuple[Optional[float], Optional[float]]:
        """
        Get the best bid and ask prices for a token.

        Args:
            token_id: The token ID to get prices for

        Returns:
            Tuple of (best_bid, best_ask) or (None, None) if unavailable
        """
        try:
            response = requests.get(
                f"{self.CLOB_API}/book",
                params={"token_id": token_id},
                timeout=10
            )
            response.raise_for_status()
            book = response.json()

            # Get best bid (highest buy price)
            bids = book.get("bids", [])
            best_bid = float(bids[0]["price"]) if bids else None

            # Get best ask (lowest sell price)
            asks = book.get("asks", [])
            best_ask = float(asks[0]["price"]) if asks else None

            return best_bid, best_ask

        except Exception as e:
            logger.debug(f"Failed to get prices for token {token_id}: {e}")
            return None, None

    def get_midpoint_price(self, token_id: str) -> Optional[float]:
        """
        Get the midpoint price for a token.

        Args:
            token_id: The token ID

        Returns:
            Midpoint price or None if unavailable
        """
        try:
            response = requests.get(
                f"{self.CLOB_API}/midpoint",
                params={"token_id": token_id},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return float(data.get("mid", 0))
        except Exception:
            return None

    def analyze_market(self, market: dict) -> Optional[ArbitrageOpportunity]:
        """
        Analyze a single market for arbitrage opportunities.

        Args:
            market: Market data dictionary

        Returns:
            ArbitrageOpportunity if found, None otherwise
        """
        try:
            # Get market tokens (YES and NO)
            tokens = market.get("tokens", [])
            clob_token_ids = market.get("clobTokenIds", [])

            # Skip if not a binary market
            if len(tokens) != 2 or len(clob_token_ids) != 2:
                return None

            # Identify YES and NO tokens
            yes_token_id = None
            no_token_id = None
            yes_price = None
            no_price = None

            for i, token in enumerate(tokens):
                outcome = token.get("outcome", "").upper()
                token_id = clob_token_ids[i] if i < len(clob_token_ids) else None
                price = float(token.get("price", 0))

                if outcome == "YES":
                    yes_token_id = token_id
                    yes_price = price
                elif outcome == "NO":
                    no_token_id = token_id
                    no_price = price

            # If we couldn't identify tokens by outcome, use position
            if yes_token_id is None or no_token_id is None:
                if len(clob_token_ids) >= 2:
                    yes_token_id = clob_token_ids[0]
                    no_token_id = clob_token_ids[1]
                    yes_price = float(tokens[0].get("price", 0)) if tokens else 0
                    no_price = float(tokens[1].get("price", 0)) if len(tokens) > 1 else 0

            # Skip if prices are not available
            if not yes_price or not no_price:
                return None

            # Get more accurate prices from order book if available
            if yes_token_id:
                _, yes_ask = self.get_token_prices(yes_token_id)
                if yes_ask:
                    yes_price = yes_ask

            if no_token_id:
                _, no_ask = self.get_token_prices(no_token_id)
                if no_ask:
                    no_price = no_ask

            # Calculate arbitrage opportunity
            total_cost = yes_price + no_price

            # Only consider if total cost < $1.00 (arbitrage exists)
            if total_cost >= 1.0:
                return None

            profit_per_share = 1.0 - total_cost
            profit_percentage = profit_per_share / total_cost

            # Check minimum profit threshold
            if profit_percentage < self.min_profit_threshold:
                return None

            # Check liquidity
            liquidity = float(market.get("liquidity", 0))
            volume = float(market.get("volume", 0))

            if liquidity < self.min_liquidity:
                return None

            return ArbitrageOpportunity(
                market_id=market.get("id", ""),
                market_question=market.get("question", "Unknown"),
                yes_price=yes_price,
                no_price=no_price,
                total_cost=total_cost,
                profit_per_share=profit_per_share,
                profit_percentage=profit_percentage,
                yes_token_id=yes_token_id or "",
                no_token_id=no_token_id or "",
                volume=volume,
                liquidity=liquidity,
                timestamp=datetime.now()
            )

        except Exception as e:
            logger.debug(f"Error analyzing market: {e}")
            return None

    def scan_for_opportunities(self) -> list[ArbitrageOpportunity]:
        """
        Scan all markets for arbitrage opportunities.

        Returns:
            List of arbitrage opportunities found
        """
        logger.info("Scanning markets for arbitrage opportunities...")

        markets = self.fetch_markets()
        opportunities = []

        for market in markets:
            opportunity = self.analyze_market(market)
            if opportunity:
                opportunities.append(opportunity)
                self._log_opportunity(opportunity)

        logger.info(f"Found {len(opportunities)} arbitrage opportunities")
        return opportunities

    def _log_opportunity(self, opp: ArbitrageOpportunity):
        """Log details of an arbitrage opportunity"""
        logger.info("=" * 60)
        logger.info(f"ARBITRAGE OPPORTUNITY FOUND!")
        logger.info(f"Market: {opp.market_question[:80]}...")
        logger.info(f"YES Price: ${opp.yes_price:.4f}")
        logger.info(f"NO Price:  ${opp.no_price:.4f}")
        logger.info(f"Total Cost: ${opp.total_cost:.4f}")
        logger.info(f"Profit per share: ${opp.profit_per_share:.4f} ({opp.profit_percentage * 100:.2f}%)")
        logger.info(f"Market Liquidity: ${opp.liquidity:,.2f}")
        logger.info(f"Market Volume: ${opp.volume:,.2f}")
        logger.info("=" * 60)

    def execute_arbitrage(self, opportunity: ArbitrageOpportunity) -> bool:
        """
        Execute an arbitrage trade.

        This buys equal amounts of YES and NO tokens to lock in profit.

        Args:
            opportunity: The arbitrage opportunity to execute

        Returns:
            True if successful, False otherwise
        """
        if not self.execute_trades or not self.clob_client:
            logger.info("Trade execution disabled - logging opportunity only")
            return False

        try:
            from py_clob_client.clob_types import MarketOrderArgs, OrderType
            from py_clob_client.order_builder.constants import BUY

            # Calculate trade size (buy equal shares of YES and NO)
            # Limit by max_trade_size and available liquidity
            shares_to_buy = min(
                self.max_trade_size / opportunity.total_cost,
                opportunity.liquidity * 0.1 / opportunity.total_cost  # Use max 10% of liquidity
            )

            if shares_to_buy < 1:
                logger.warning("Trade size too small, skipping")
                return False

            logger.info(f"Executing arbitrage: buying {shares_to_buy:.2f} shares each of YES and NO")

            # Buy YES tokens
            yes_order = MarketOrderArgs(
                token_id=opportunity.yes_token_id,
                amount=shares_to_buy * opportunity.yes_price,
                side=BUY,
                order_type=OrderType.FOK  # Fill or Kill
            )

            signed_yes = self.clob_client.create_market_order(yes_order)
            yes_result = self.clob_client.post_order(signed_yes, OrderType.FOK)
            logger.info(f"YES order result: {yes_result}")

            # Buy NO tokens
            no_order = MarketOrderArgs(
                token_id=opportunity.no_token_id,
                amount=shares_to_buy * opportunity.no_price,
                side=BUY,
                order_type=OrderType.FOK
            )

            signed_no = self.clob_client.create_market_order(no_order)
            no_result = self.clob_client.post_order(signed_no, OrderType.FOK)
            logger.info(f"NO order result: {no_result}")

            expected_profit = shares_to_buy * opportunity.profit_per_share
            logger.info(f"Trade executed! Expected profit: ${expected_profit:.4f}")

            return True

        except Exception as e:
            logger.error(f"Failed to execute trade: {e}")
            return False

    def save_opportunities(self, opportunities: list[ArbitrageOpportunity], filename: str = "opportunities.json"):
        """Save opportunities to a JSON file for analysis"""
        data = []
        for opp in opportunities:
            data.append({
                "market_id": opp.market_id,
                "market_question": opp.market_question,
                "yes_price": opp.yes_price,
                "no_price": opp.no_price,
                "total_cost": opp.total_cost,
                "profit_per_share": opp.profit_per_share,
                "profit_percentage": opp.profit_percentage,
                "volume": opp.volume,
                "liquidity": opp.liquidity,
                "timestamp": opp.timestamp.isoformat(),
            })

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved {len(opportunities)} opportunities to {filename}")

    def run(self, continuous: bool = True):
        """
        Run the arbitrage bot.

        Args:
            continuous: If True, run continuously. If False, run once.
        """
        logger.info("Starting Polymarket Arbitrage Bot...")

        try:
            while True:
                scan_start = time.time()

                # Scan for opportunities
                opportunities = self.scan_for_opportunities()

                if opportunities:
                    # Save opportunities to file
                    self.save_opportunities(opportunities)

                    # Sort by profit percentage (best first)
                    opportunities.sort(key=lambda x: x.profit_percentage, reverse=True)

                    # Execute trades if enabled
                    if self.execute_trades:
                        for opp in opportunities[:3]:  # Execute top 3 opportunities
                            self.execute_arbitrage(opp)
                            time.sleep(1)  # Small delay between trades

                    # Track statistics
                    self.opportunities_found.extend(opportunities)
                    potential_profit = sum(o.profit_per_share * 100 for o in opportunities)
                    self.total_potential_profit += potential_profit

                    logger.info(f"Potential profit this scan (at $100 per opportunity): ${potential_profit:.2f}")
                    logger.info(f"Total potential profit found: ${self.total_potential_profit:.2f}")

                if not continuous:
                    break

                # Wait for next scan
                scan_duration = time.time() - scan_start
                sleep_time = max(0, self.scan_interval - scan_duration)

                logger.info(f"Next scan in {sleep_time:.0f} seconds...")
                time.sleep(sleep_time)

        except KeyboardInterrupt:
            logger.info("\nBot stopped by user")
            self._print_summary()

    def _print_summary(self):
        """Print a summary of the bot's findings"""
        logger.info("\n" + "=" * 60)
        logger.info("SESSION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total opportunities found: {len(self.opportunities_found)}")
        logger.info(f"Total potential profit: ${self.total_potential_profit:.2f}")

        if self.opportunities_found:
            avg_profit = sum(o.profit_percentage for o in self.opportunities_found) / len(self.opportunities_found)
            logger.info(f"Average profit percentage: {avg_profit * 100:.2f}%")

        logger.info("=" * 60)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Polymarket Arbitrage Bot")
    parser.add_argument(
        "--min-profit",
        type=float,
        default=0.01,
        help="Minimum profit threshold (0.01 = 1%%)"
    )
    parser.add_argument(
        "--min-liquidity",
        type=float,
        default=100.0,
        help="Minimum market liquidity in USDC"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Scan interval in seconds"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Enable trade execution (requires POLYMARKET_PRIVATE_KEY env var)"
    )
    parser.add_argument(
        "--max-trade",
        type=float,
        default=50.0,
        help="Maximum trade size in USDC"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run once and exit (don't run continuously)"
    )

    args = parser.parse_args()

    bot = PolymarketArbitrageBot(
        min_profit_threshold=args.min_profit,
        min_liquidity=args.min_liquidity,
        scan_interval=args.interval,
        execute_trades=args.execute,
        max_trade_size=args.max_trade,
    )

    bot.run(continuous=not args.once)


if __name__ == "__main__":
    main()
