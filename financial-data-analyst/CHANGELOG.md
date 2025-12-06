# Changelog

All notable changes to the Financial Data Analyst quickstart will be documented in this file.

## [0.1.0] - 2025-12-06

### Added
- Initial release of Financial Data Analyst quickstart
- Next.js 14 application with TypeScript and Tailwind CSS
- Integration with Claude AI (Haiku, Claude 4.5 Haiku, and Sonnet 3.5)
- Multi-format file upload support:
  - Text/Code files (.txt, .md, .html, .py, .csv, etc)
  - PDF documents with text extraction using PDF.js
  - Image file support
- Interactive data visualization using Recharts:
  - Line Charts for time series data and trends
  - Bar Charts for single metric comparisons
  - Multi-Bar Charts for multiple metrics comparison
  - Area Charts for volume/quantity over time
  - Stacked Area Charts for component breakdowns
  - Pie Charts for distribution analysis
- Chat-based interface for natural language data analysis
- Dark mode support with theme switching
- Tool-based chart generation using Claude's tool use capabilities
- Responsive design with shadcn/ui components
- Edge runtime API routes for optimal performance
- File preview components for uploaded files
- Chart pagination for navigating multiple visualizations
- Comprehensive README with setup instructions and use cases

### Technical Components
- `app/finance/page.tsx`: Main chat interface with file upload and visualization
- `app/api/finance/route.ts`: API route for Claude AI integration with tool use
- `components/ChartRenderer.tsx`: Chart rendering component supporting 6 chart types
- `components/FilePreview.tsx`: File preview component for uploads
- `components/TopNavBar.tsx`: Navigation bar with theme switcher
- `utils/fileHandling.ts`: File processing utilities for text, images, and PDFs
- `types/chart.ts`: TypeScript definitions for chart data structures
