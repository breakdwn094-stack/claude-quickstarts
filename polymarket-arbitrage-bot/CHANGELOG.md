# Changelog

All notable changes to the Polymarket Arbitrage Bot will be documented in this file.

## [1.0.0] - 2024-12-28

### Added
- Initial release of Polymarket Arbitrage Bot
- Market scanning functionality to fetch all active markets from Polymarket Gamma API
- Arbitrage detection algorithm to identify YES + NO < $1.00 opportunities
- Order book price fetching for accurate pricing
- Trade execution capability using py-clob-client
- Configurable parameters (min profit, min liquidity, scan interval, max trade size)
- JSON export of discovered opportunities
- Comprehensive logging to console and file
- Environment variable configuration via .env file
- Detailed README with step-by-step deployment instructions
- Support for both monitoring mode and trading mode
