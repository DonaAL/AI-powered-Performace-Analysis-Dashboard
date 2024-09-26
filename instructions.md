Developer Performance Analytics Dashboard:

Setup and Installation:
1. Install Dependencies
Ensure you have all the required packages installed by running:
pip install -r requirements.txt

2. Configure Environment
Update the .env file with your GitHub API token and any other necessary credentials. The .env file should include:

GITHUB_TOKEN: Your GitHub API token.

3.Frontend
Run the Streamlit frontend server using:
streamlit run app.py
The system should now be live at http://localhost:8501.

Module-wise Instructions

1. Data Collection Module
Purpose: Fetches detailed data from GitHub repositories including commits, pull requests, issues, and code reviews.

How to Run:

Input the GitHub repository URL in the Streamlit app.
The data will be collected and processed.
2. Metrics Calculation Module
Purpose: Calculates various performance metrics from the collected GitHub data.

How to Run:

Metrics are automatically calculated from the fetched data.
View the metrics results in the Streamlit dashboard.
3. Dashboard Visualization Module
Purpose: Displays the calculated metrics through interactive charts and graphs.

How to Run:

View the visualizations in the Streamlit app.
Charts and graphs are automatically updated based on the latest metrics.
4. Query Module
Purpose: Processes natural language queries to display relevant charts and metrics.

How to Run:

Enter a natural language query in the Streamlit app.
The corresponding charts and metrics will be displayed.
5. Comparison Module
Purpose: Compares metrics between two GitHub profiles and displays the comparison results.

How to Run:

Provide the GitHub profiles for comparison in the Streamlit app.
View the comparison results and charts in the dashboard.

