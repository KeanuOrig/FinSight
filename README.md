# FinSight

## Description
**FinSight** is an AI-powered stock analysis platform designed to aid investors in making smarter, data-driven decisions.

## Tech Stack
- **Backend**: Python, Django

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
