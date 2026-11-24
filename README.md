# Betty's Bird Boutique - Customer Service Agent

A customer service chatbot built with Google ADK (Agent Development Kit) and Vertex AI for Betty's Bird Boutique, a pet store specializing in birds.

## Author

Jyoti Kumari

## Getting Started

Instructions for how to get a copy of the project running on your local machine.

### Dependencies

```
google-adk
google-cloud-discoveryengine
toolbox-core
python-dotenv
```

### Installation

1. Clone the repository.
2. Create and activate a Python virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r starter/requirements.txt
   ```
4. Create a `.env` file inside `starter/` with the following variables:
   ```
   DATASTORE_PROJECT_ID=your-gcp-project-id
   DATASTORE_LOCATION=global
   DATASTORE_ENGINE_ID=your-vertex-ai-search-engine-id
   TOOLBOX_URL=http://127.0.0.1:5000
   MYSQL_HOST=your-mysql-host
   MYSQL_PORT=3306
   MYSQL_USER=your-mysql-user
   MYSQL_PASSWORD=your-mysql-password
   ```
5. Set up the MySQL database using `starter/docs/betty_db.sql`.
6. Download the MCP Toolbox binary and start it with `tools.yaml`:
   ```
   ./toolbox --tools-file starter/tools.yaml
   ```
7. Run the agent in the ADK web previewer:
   ```
   cd starter
   adk web
   ```

## Project Overview

The agent (persona name: Bettina) has three tools:

- **get_product_price** — queries a MySQL database via MCP Toolbox for product pricing.
- **search_store_documents** — searches store PDF documents (hours, history, staff) via Vertex AI Search.
- **general_bird_search** — answers general bird knowledge questions using Grounding with Google Search (delegated to a sub-agent).

## Built With

* [Google ADK](https://google.github.io/adk-docs/) - Agent Development Kit
* [Vertex AI Search](https://cloud.google.com/generative-ai-app-builder/docs/enterprise-search-introduction) - Document search and retrieval
* [MCP Toolbox](https://github.com/googleapis/genai-toolbox) - MySQL database tool integration
* [Gemini 2.5 Flash](https://deepmind.google/models/gemini/flash/) - Underlying language model

## License
[License](../LICENSE.md)
