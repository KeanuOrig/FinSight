# FinSight

## Description
**FinSight** is an AI-powered stock analysis platform designed to aid investors in making smarter, data-driven decisions.

## Tech Stack
- **Backend**: Python, Django - https://github.com/KeanuOrig/FinSight
- **Frontend**: React, Typescript - https://github.com/KeanuOrig/FinSight-React

## Project Structure

The project is organized into distinct apps, each serving a unique purpose to ensure modularity and scalability.

1. **Core App**
   - The central part of the project, handling general-purpose views and utilities.

2. **Stock Data and Analysis**
   - This app manages stock data retrieval, financial insights, and market analysis features to give users comprehensive information about selected stocks.

3. **AI Integration (ChatGPT)**
   - Manages AI-related features, such as chatbot integration, analysis, and personalized recommendations powered by ChatGPT.

4. **API (REST API Endpoints)**
   - Provides REST API endpoints for frontend integration or external access, allowing smooth data flow and interaction.

5. **Users (Authentication & Profile Management)**
   - Handles user management, including registration, authentication, and profile management, ensuring secure access and personalized user experience.

6. **Reports (Report Generation & Viewing)**
   - Responsible for report generation, enabling users to view or download stock analysis reports for detailed insights.

## Getting Started

To get started with **FinSight**, clone the repository, set up a virtual environment, and install the necessary dependencies from `requirements.txt`. Ensure to configure your `.env` file with appropriate keys for Django settings and AI model integration.

### Prerequisites
- Python 3.x
- Django
- django-environ (for environment variable management)

### Getting Started: Setup and Operations Guide
1. Migrate the Database

2. Input env values

3. Create Superuser and Load Initial Data
   - Run the following API to create a superuser and seed the database with initial fixture data.
   - URL: /api/create-superuser-and-load-fixtures/
   - This will create a superuser (with default credentials) and load stock data into the database.
  
4. Login to Admin Panel
   - Go to the Django admin panel: /admin
   - Use the following credentials to log in:
   - Username: admin
   - Password: admin
   - Once logged in, you can manage your stock data, adjust settings, or perform other administrative tasks.
     
5. Import or Modify Stock Data
   - Navigate to the admin panel, and locate the stock data section.
   - Import new stock data or modify existing records as needed.
     
6. Run Stock Data Analysis
   - Use the following API endpoint to analyze stock data for a given symbol:
   - URL Format: /stocks/predict/<str:symbol>/
   - Replace <str:symbol> with the stock symbol you want to analyze (e.g., /stocks/predict/AAPL/ for Apple).
   - The API will return predictive analytics and insights about the stock.
     
7. Frontend Option (Optional)
   - If you want a frontend interface for your application, you can serve it by running the following React app:
   - Frontend Repo: FinSight-React
   - Follow the setup instructions in the repo to get it running on your local server.
   - This will provide a user-friendly UI to interact with the data and predictions.
