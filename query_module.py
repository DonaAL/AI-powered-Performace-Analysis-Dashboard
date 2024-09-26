import pandas as pd
from charts import (
    plot_language_distribution,
    plot_commit_frequency,
    plot_pull_request_merge_rate,
    plot_average_issue_resolution_time,
    plot_contributor_activity,
    plot_top_issues_by_comments,
    plot_average_pull_request_review_time,
    plot_average_issue_age
)

def handle_user_query(query: str, metrics: dict):
    """
    Process the natural language query to determine which chart to display.
    
    Args:
    - query (str): The user's query.
    - metrics (dict): The dictionary of calculated metrics.
    
    Returns:
    - tuple: (Figure, string) where Figure is the Plotly chart and string is the description.
    """
    query = query.lower()

    if 'language distribution' in query:
        df = pd.DataFrame(metrics.get('languages', {}).items(), columns=['Language', 'Bytes'])
        if not df.empty:
            fig = plot_language_distribution(df)
            description = "Language Distribution"
        else:
            fig, description = None, "No language data available."

    elif 'commit frequency' in query:
        df = metrics.get('commit_frequency', pd.DataFrame())
        if not df.empty:
            fig = plot_commit_frequency(df)
            description = "Commit Frequency Over Time"
        else:
            fig, description = None, "No commit frequency data available."

    elif 'pr merge rate' in query:
        merge_rate = metrics.get('pr_merge_rate', {})
        if merge_rate:
            fig = plot_pull_request_merge_rate(merge_rate)
            description = "Pull Request Merge Rate"
        else:
            fig, description = None, "No pull request merge rate data available."

    elif 'issue resolution time' in query:
        avg_resolution_time = metrics.get('issue_resolution_time', 0)
        if avg_resolution_time:
            fig = plot_average_issue_resolution_time(avg_resolution_time)
            description = "Average Issue Resolution Time"
        else:
            fig, description = None, "No issue resolution time data available."

    elif 'contributor activity' in query:
        df = metrics.get('contributor_activity', pd.DataFrame())
        if not df.empty:
            fig = plot_contributor_activity(df)
            description = "Contributor Activity"
        else:
            fig, description = None, "No contributor activity data available."

    elif 'top issues by comments' in query:
        df = metrics.get('top_issues', pd.DataFrame())
        if not df.empty:
            fig = plot_top_issues_by_comments(df)
            description = "Top Issues by Comments"
        else:
            fig, description = None, "No top issues data available."

    elif 'pr review time' in query:
        avg_review_time = metrics.get('pr_review_time', 0)
        if avg_review_time:
            fig = plot_average_pull_request_review_time(avg_review_time)
            description = "Average Pull Request Review Time"
        else:
            fig, description = None, "No pull request review time data available."

    elif 'issue age' in query:
        avg_issue_age = metrics.get('issue_age', 0)
        if avg_issue_age:
            fig = plot_average_issue_age(avg_issue_age)
            description = "Average Issue Age"
        else:
            fig, description = None, "No issue age data available."

    else:
        fig, description = None, "Query not recognized. Please ask about available metrics."

    return fig, description
