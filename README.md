# 📰 Google News CLI Tool

An interactive command-line utility built with Node.js that parses live Google News RSS feeds right inside the terminal. It supports quick parameter filters for targeted information fetching.

## 🚀 Key Features
* **Interactive Terminal UI:** Built using native Node modules for streamlined reading.
* **Topic Filtering:** Pull live stories directly by streaming targeted topics (e.g., `technology`).
* **Keyword Search:** Deep-scan titles using string pattern configurations.

## 🛠️ Tech Stack
* **Runtime Engine:** Node.js
* **Data Format:** XML/RSS Feed Parsing

## 💻 Local Setup & Execution
1. Install core dependencies:
   ```bash
   npm install
   ```
2. Launch the interactive interface:
   ```bash
   node google-news-cli.js
   ```
3. Run with targeted flags:
   ```bash
   node google-news-cli.js --topic technology --limit 5
   ```
