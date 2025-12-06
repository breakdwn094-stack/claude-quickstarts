# 🏠 Starting the Financial App on Your Computer

Hey! Here's what to do when you get home to your computer.

## Step 1: Open Your Terminal/Command Prompt

**On Mac:**
- Press `Command + Space`
- Type "Terminal"
- Press Enter

**On Windows:**
- Press `Windows Key`
- Type "Command Prompt" or "PowerShell"
- Press Enter

**On Linux:**
- Press `Ctrl + Alt + T`

## Step 2: Navigate to the Project

Copy and paste this command into your terminal:

```bash
cd /home/user/claude-quickstarts/financial-data-analyst
```

Press Enter.

## Step 3: Start the App

Copy and paste this command:

```bash
npm run dev
```

Press Enter.

Wait a few seconds. You'll see something like:
```
✓ Ready in 2.8s
- Local: http://localhost:3000
```

## Step 4: Open in Your Browser

1. Open your favorite web browser (Chrome, Safari, Firefox, etc.)
2. In the address bar, type: `http://localhost:3000`
3. Press Enter

**You should see the Financial Data Analyst app!** 🎉

## Step 5: Using the App

1. **Pick a model**: Click the dropdown in the top right and select "Claude 3.5 Sonnet" (recommended)

2. **Try asking something simple** like:
   ```
   Generate sample revenue data for the last 6 months and show it as a line chart
   ```

3. **Or upload a file**:
   - Click the paperclip icon (📎)
   - Choose a CSV, PDF, or image
   - Ask Claude to analyze it!

## If Something Goes Wrong

### "npm: command not found"
You need to install Node.js first:
- Go to https://nodejs.org/
- Download and install the LTS version
- Restart your terminal and try again

### "Port 3000 is already in use"
Something else is using that port. Try:
```bash
npm run dev -- -p 3001
```
Then open `http://localhost:3001` instead

### Still stuck?
Come back here and ask me! I'm happy to help troubleshoot.

---

## Want to Stop the App?

In the terminal where it's running, press:
- `Ctrl + C` (on Mac/Linux/Windows)

---

Good luck! You've got this! 💪
