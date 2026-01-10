# Getting Started with Financial Data Analyst

This guide will walk you through setting up and using the Financial Data Analyst app.

## Step 1: Get Your Anthropic API Key

1. Go to **https://console.anthropic.com/**
2. Sign up or log in to your account
3. Navigate to **API Keys** in the dashboard
4. Click **Create Key**
5. Copy your API key (it starts with `sk-ant-`)

## Step 2: Configure Your Environment

1. Open the `.env.local` file in the `financial-data-analyst` directory
2. Replace `your_api_key_here` with your actual API key:

```env
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

3. Save the file

## Step 3: Start the Development Server

In your terminal, run:

```bash
cd /home/user/claude-quickstarts/financial-data-analyst
npm run dev
```

You should see output like:
```
> financial-assistant@0.1.0 dev
> next dev

  ▲ Next.js 14.2.15
  - Local:        http://localhost:3000
  - Ready in 2.3s
```

## Step 4: Open the App

1. Open your web browser
2. Go to **http://localhost:3000**
3. You should see the Financial Data Analyst interface!

## Step 5: Using the App

### Chat Interface (Left Panel)

- **Select a Model**: Click the dropdown in the top-right to choose between:
  - Claude 3 Haiku (fast, cost-effective)
  - Claude 4.5 Haiku (balanced performance)
  - Claude 3.5 Sonnet (most capable, recommended)

### Upload Files

1. **Click the paperclip icon** (📎) at the bottom left of the chat input
2. Select a file:
   - **Text/CSV files**: For data analysis
   - **PDF documents**: For extracting financial data
   - **Images**: For analyzing charts or screenshots
3. The file preview will appear above the input box

### Example Use Cases

#### 1. Analyze CSV Data
Upload a CSV file with financial data and ask:
- "What are the trends in this data?"
- "Create a bar chart showing revenue by quarter"
- "Show me a line chart of sales over time"

#### 2. Extract PDF Data
Upload a financial report PDF and ask:
- "Extract the key financial metrics from this report"
- "Create a pie chart showing the budget allocation"
- "What's the revenue breakdown by product?"

#### 3. Analyze Images
Upload a screenshot of a chart and ask:
- "What insights can you extract from this chart?"
- "Recreate this as an interactive visualization"

### Understanding the Visualizations (Right Panel)

When Claude generates charts, they appear on the right side:

- **Navigation**: Use the dots on the right edge to switch between multiple charts
- **Chart Types Available**:
  - 📊 **Bar Charts**: Compare single metrics
  - 📊 **Multi-Bar Charts**: Compare multiple metrics side-by-side
  - 📈 **Line Charts**: Show trends over time
  - 🥧 **Pie Charts**: Display distributions
  - 📉 **Area Charts**: Show volume or cumulative data
  - 📊 **Stacked Area Charts**: Display component breakdowns

### Tips for Best Results

1. **Be specific**: "Create a bar chart of revenue by quarter" works better than "show me the data"
2. **Ask follow-ups**: You can refine charts by asking for changes
3. **Try different models**: Sonnet is more capable but slower; Haiku is faster
4. **Upload quality data**: Well-structured CSVs and readable PDFs work best

## Example Queries to Try

```
"Generate sample quarterly revenue data and show it as a line chart"

"Create a pie chart showing market share distribution for tech companies"

"Show me a multi-bar chart comparing sales and costs by product"

"Generate financial data for the last 6 months and visualize the trend"
```

## Troubleshooting

### API Key Issues
- **Error: "Authentication Error"**: Check your API key in `.env.local`
- **Error: "Invalid API key"**: Make sure you copied the full key including `sk-ant-`

### Server Not Starting
- Make sure you ran `npm install` first
- Check that port 3000 isn't already in use
- Try `npm run dev` again

### Charts Not Appearing
- Ensure you're asking Claude to create visualizations
- Try being more explicit: "Create a chart showing..."
- Check the browser console for errors (F12)

## Stopping the App

To stop the development server:
1. Go to your terminal where `npm run dev` is running
2. Press `Ctrl + C` (or `Cmd + C` on Mac)

## Need Help?

- Check the main [README.md](README.md) for more details
- Review the [CHANGELOG.md](CHANGELOG.md) for features
- Visit https://docs.anthropic.com/ for Claude API documentation
