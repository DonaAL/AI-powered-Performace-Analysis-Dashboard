import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Define a color palette with shades of blue
blue_palette = {
    "background": "#1e1e1e",  # Dark background for the theme
    "text": "#FFFFFF",  # White text for contrast
    "primary": "#1E90FF",  # Main color
    "secondary": "#4682B4",  # Slightly lighter shade
    "tertiary": "#87CEEB",  # Even lighter shade
    "quaternary": "#B0C4DE",  # Lightest shade
    "highlight": "#00BFFF",  # Bright highlight color
}

def update_plotly_colors(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        paper_bgcolor=blue_palette["background"],
        plot_bgcolor=blue_palette["background"],
        font_color=blue_palette["text"],
        colorway=[
            blue_palette["primary"],
            blue_palette["secondary"],
            blue_palette["tertiary"],
            blue_palette["quaternary"],
            blue_palette["highlight"]
        ]
    )
    return fig

def plot_language_distribution(df: pd.DataFrame) -> go.Figure:
    if 'Language' not in df.columns or 'Bytes' not in df.columns:
        raise ValueError("DataFrame must contain 'Language' and 'Bytes' columns")
    fig = px.pie(df, names='Language', values='Bytes', title='Language Distribution',
                 color_discrete_sequence=[blue_palette["primary"]])
    fig = update_plotly_colors(fig)
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return fig

def plot_commit_frequency(commit_frequency_data) -> go.Figure:
    if isinstance(commit_frequency_data, pd.Series):
        commit_frequency_df = commit_frequency_data.to_frame(name='commit_frequency')
    elif isinstance(commit_frequency_data, list):
        commit_frequency_df = pd.DataFrame(commit_frequency_data, columns=['commit_frequency'])
    elif isinstance(commit_frequency_data, pd.DataFrame):
        commit_frequency_df = commit_frequency_data
    else:
        raise TypeError("Invalid data type for commit_frequency_data")
    
    fig = px.line(commit_frequency_df, x=commit_frequency_df.index, y='commit_frequency', title='Commit Frequency Over Time',
                  markers=True, line_shape='linear', color_discrete_sequence=[blue_palette["primary"]])
    fig = update_plotly_colors(fig)
    fig.update_layout(xaxis_title='Date', yaxis_title='Commit Count')
    return fig

def plot_pull_request_merge_rate(merge_rate: dict) -> go.Figure:
    if 'total_prs' not in merge_rate or 'merged_prs' not in merge_rate:
        raise ValueError("merge_rate dictionary must contain 'total_prs' and 'merged_prs'")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=['Total PRs', 'Merged PRs'], y=[merge_rate['total_prs'], merge_rate['merged_prs']],
                         marker_color=[blue_palette["secondary"], blue_palette["tertiary"]]))
    fig = update_plotly_colors(fig)
    fig.update_layout(title='Pull Request Merge Rate', xaxis_title='PRs', yaxis_title='Count',
                      xaxis=dict(tickvals=['Total PRs', 'Merged PRs'], ticktext=['Total PRs', 'Merged PRs']))
    return fig

def plot_average_issue_resolution_time(avg_resolution_time: float) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=float(avg_resolution_time),
        title={"text": "Avg. Issue Resolution Time (Days)"},
        gauge={'axis': {'range': [None, 30]},
               'bar': {'color': blue_palette["highlight"]},
               'steps': [{'range': [0, 10], 'color': blue_palette["tertiary"]},
                         {'range': [10, 20], 'color': blue_palette["quaternary"]},
                         {'range': [20, 30], 'color': blue_palette["secondary"]}]}
    ))
    fig = update_plotly_colors(fig)
    return fig

def plot_contributor_activity(contributor_activity_series) -> go.Figure:
    if isinstance(contributor_activity_series, pd.Series):
        contributor_activity_df = contributor_activity_series.reset_index()
        contributor_activity_df.columns = ['contributor', 'contributor_activity']
    elif isinstance(contributor_activity_series, pd.DataFrame):
        contributor_activity_df = contributor_activity_series
    else:
        raise TypeError("Invalid data type for contributor_activity_series")
    
    fig = px.bar(contributor_activity_df, x='contributor', y='contributor_activity', title='Contributor Activity',
                 color='contributor_activity', color_continuous_scale=[blue_palette["primary"], blue_palette["tertiary"]])
    fig = update_plotly_colors(fig)
    fig.update_layout(xaxis_title='Contributor', yaxis_title='Activity Count', xaxis_tickangle=-45)
    return fig

def plot_top_issues_by_comments(top_issues_df: pd.DataFrame) -> go.Figure:
    if 'title' not in top_issues_df.columns or 'comments' not in top_issues_df.columns:
        raise ValueError("DataFrame must contain 'title' and 'comments' columns")
    fig = px.bar(top_issues_df, x='title', y='comments', title='Top Issues by Comments',
                 labels={'title': 'Issue Title', 'comments': 'Number of Comments'},
                 color='comments', color_continuous_scale=[blue_palette["primary"], blue_palette["tertiary"]])
    fig = update_plotly_colors(fig)
    fig.update_layout(xaxis_title='Issue Title', yaxis_title='Number of Comments', xaxis_tickangle=-45)
    return fig

def plot_average_pull_request_review_time(avg_review_time: float) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=float(avg_review_time),
        title={"text": "Avg. PR Review Time (Days)"},
        gauge={'axis': {'range': [None, 30]},
               'bar': {'color': blue_palette["highlight"]},
               'steps': [{'range': [0, 10], 'color': blue_palette["tertiary"]},
                         {'range': [10, 20], 'color': blue_palette["quaternary"]},
                         {'range': [20, 30], 'color': blue_palette["secondary"]}]}
    ))
    fig = update_plotly_colors(fig)
    return fig

def plot_average_issue_age(avg_issue_age: float) -> go.Figure:
    # Ensure the value is a standard Python float
    avg_issue_age = float(avg_issue_age)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_issue_age,
        title={"text": "Avg. Issue Age (Days)"},
        gauge={'axis': {'range': [None, 30]},
               'bar': {'color': blue_palette["highlight"]},
               'steps': [{'range': [0, 10], 'color': blue_palette["tertiary"]},
                         {'range': [10, 20], 'color': blue_palette["quaternary"]},
                         {'range': [20, 30], 'color': blue_palette["secondary"]}]}
    ))
    fig = update_plotly_colors(fig)
    return fig
