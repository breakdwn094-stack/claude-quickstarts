# Polymarket Arbitrage Bot

A Python bot that scans Polymarket for arbitrage opportunities where you can profit regardless of the outcome.

## What is Arbitrage?

**The Simple Concept:** On Polymarket, every market has YES and NO outcomes. If YES wins, you get $1. If NO wins, you get $1. If you can buy BOTH for less than $1 total, you're guaranteed profit!

**Example:**
- YES price = $0.48
- NO price = $0.49
- Total cost = $0.97
- Guaranteed payout = $1.00
- **Profit = $0.03 per share (3%)**

Scale that across thousands of trades = real money.

---

## How to Set Up (Step-by-Step for Beginners)

### Step 1: Install Python

**Windows:**
1. Go to [python.org/downloads](https://python.org/downloads)
2. Download Python 3.11 or newer
3. Run the installer
4. **IMPORTANT:** Check the box that says "Add Python to PATH"
5. Click "Install Now"

**Mac:**
1. Open Terminal (search for "Terminal" in Spotlight)
2. Install Homebrew by pasting this command:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Python:
   ```bash
   brew install python
   ```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Step 2: Download This Bot

**Option A - Using Git (recommended):**
```bash
git clone https://github.com/anthropics/claude-quickstarts.git
cd claude-quickstarts/polymarket-arbitrage-bot
```

**Option B - Manual Download:**
1. Download the files from this folder
2. Put them in a folder on your computer
3. Open a terminal/command prompt in that folder

### Step 3: Set Up the Environment

Open a terminal/command prompt in the bot folder and run these commands:

**Windows:**
```bash
# Create a virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Run the Bot (Monitoring Mode)

To scan for opportunities WITHOUT trading (safe mode):

```bash
python arbitrage_bot.py
```

The bot will:
1. Scan all Polymarket markets every 30 seconds
2. Print any arbitrage opportunities it finds
3. Save opportunities to `opportunities.json`
4. NOT execute any trades (just watching)

**Example Output:**
```
============================================================
ARBITRAGE OPPORTUNITY FOUND!
Market: Will Bitcoin reach $100,000 by end of 2025?...
YES Price: $0.4800
NO Price:  $0.4900
Total Cost: $0.9700
Profit per share: $0.0300 (3.09%)
Market Liquidity: $15,234.00
Market Volume: $125,678.00
============================================================
```

### Step 5: Customize the Bot (Optional)

**Change how picky the bot is:**

```bash
# Only show opportunities with at least 2% profit
python arbitrage_bot.py --min-profit 0.02

# Only show markets with at least $500 liquidity
python arbitrage_bot.py --min-liquidity 500

# Scan every 60 seconds instead of 30
python arbitrage_bot.py --interval 60

# Run once and exit (don't loop)
python arbitrage_bot.py --once
```

---

## How to Execute Trades (Advanced)

**WARNING: This involves real money. Only do this if you understand the risks!**

### Step 1: Get a Polygon Wallet

1. Install [MetaMask](https://metamask.io) browser extension
2. Create a new wallet (save your recovery phrase!)
3. Add the Polygon network:
   - Network Name: Polygon Mainnet
   - RPC URL: https://polygon-rpc.com
   - Chain ID: 137
   - Symbol: MATIC
   - Explorer: https://polygonscan.com

### Step 2: Fund Your Wallet

1. Get USDC on Polygon network
2. Bridge from Ethereum or buy directly on Polygon
3. You also need a tiny bit of MATIC for gas fees (~$0.01 per trade)

### Step 3: Set Up Your Private Key

1. In MetaMask, click the three dots > Account Details > Show Private Key
2. Copy your private key
3. Create a `.env` file in the bot folder:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` and paste your private key:
   ```
   POLYMARKET_PRIVATE_KEY=your_actual_private_key_here
   ```

**NEVER share your private key with anyone!**

### Step 4: Approve Token Spending

Before trading, you need to approve Polymarket to use your USDC. This is a one-time setup:

1. Go to [Polymarket.com](https://polymarket.com)
2. Connect your MetaMask wallet
3. Try to make a small trade manually
4. This will prompt you to approve token spending

### Step 5: Run with Trading Enabled

```bash
# Execute trades automatically (max $50 per trade)
python arbitrage_bot.py --execute --max-trade 50

# More conservative settings
python arbitrage_bot.py --execute --max-trade 20 --min-profit 0.02 --min-liquidity 1000
```

---

## Running 24/7 (Keep the Bot Running)

### Option A: Run on Your Computer

**Windows:**
1. Open Command Prompt
2. Navigate to bot folder
3. Run `venv\Scripts\activate`
4. Run `python arbitrage_bot.py`
5. Keep the window open

**Mac/Linux:**
```bash
# Use 'screen' to keep running after closing terminal
screen -S arbitrage
source venv/bin/activate
python arbitrage_bot.py
# Press Ctrl+A, then D to detach
# Run 'screen -r arbitrage' to reconnect
```

### Option B: Run on a Cloud Server (Recommended)

**Using a cheap $5/month server:**

1. Create an account on [DigitalOcean](https://digitalocean.com), [Vultr](https://vultr.com), or [Linode](https://linode.com)
2. Create a $5/month Ubuntu server
3. SSH into your server
4. Run these commands:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip python3-venv git -y

# Clone the repo
git clone https://github.com/anthropics/claude-quickstarts.git
cd claude-quickstarts/polymarket-arbitrage-bot

# Set up environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create your .env file
cp .env.example .env
nano .env  # Add your private key, then Ctrl+X to save

# Run with screen (stays running after disconnect)
screen -S arbitrage
python arbitrage_bot.py --execute
# Press Ctrl+A, then D to detach
```

---

## Important Notes

### Risks to Understand

1. **Slippage:** Prices can change between when you see an opportunity and when you trade
2. **Liquidity:** Low liquidity markets might not fill your orders
3. **Gas Fees:** Every trade costs a small amount of MATIC
4. **Smart Contract Risk:** Bugs in Polymarket's contracts could cause losses
5. **Market Manipulation:** Others might post fake opportunities

### Why Don't More People Do This?

- Opportunities are rare (markets are efficient)
- Other bots are competing for the same opportunities
- Profit margins are small (1-3% typically)
- You need capital to make meaningful money

### Legal Notice

- Polymarket is NOT available in the US
- Check your local laws before trading
- This is not financial advice
- Trade at your own risk

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'requests'"**
```bash
pip install -r requirements.txt
```

**"No opportunities found"**
- This is normal! Arbitrage opportunities are rare
- Try lowering `--min-profit` to 0.005 (0.5%)
- Be patient and let it run

**"Failed to initialize trading client"**
- Make sure your `.env` file has the correct private key
- Check that `py-clob-client` is installed

**"Connection timeout"**
- Check your internet connection
- Polymarket API might be temporarily down
- Try again in a few minutes

---

## Command Reference

```bash
# Basic monitoring (no trades)
python arbitrage_bot.py

# All options
python arbitrage_bot.py \
  --min-profit 0.01 \      # Minimum 1% profit (default)
  --min-liquidity 100 \    # Minimum $100 liquidity (default)
  --interval 30 \          # Scan every 30 seconds (default)
  --max-trade 50 \         # Max $50 per trade (default)
  --execute \              # Enable trading (default: off)
  --once                   # Run once and exit (default: continuous)
```

---

## Files Explained

- `arbitrage_bot.py` - The main bot code
- `requirements.txt` - Python packages needed
- `.env.example` - Example configuration (copy to `.env`)
- `.env` - Your actual configuration (don't commit this!)
- `opportunities.json` - Saved opportunities (created automatically)
- `arbitrage_bot.log` - Log file (created automatically)

---

## Questions?

If you have questions or issues, please open a GitHub issue in this repository.

Good luck and happy arbitraging! (But remember: no guarantees in trading!)
