import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def fetch_profile_data(github_data, owner_login):
    """Fetch and return profile data for a given GitHub owner login."""
    profile = github_data.get(owner_login, {}).get('profile', {})
    return profile

def generate_comparison_dataframe(primary_profile, secondary_profile):
    """Generate a DataFrame comparing the primary and secondary profiles."""
    comparison_df = pd.DataFrame({
        'Metric': ['Public Repos', 'Followers', 'Following', 'Created At'],
        'Primary Owner': [
            primary_profile.get('public_repos', 0),
            primary_profile.get('followers', 0),
            primary_profile.get('following', 0),
            primary_profile.get('created_at', 'N/A')
        ],
        'Secondary Owner': [
            secondary_profile.get('public_repos', 0) if secondary_profile else 'N/A',
            secondary_profile.get('followers', 0) if secondary_profile else 'N/A',
            secondary_profile.get('following', 0) if secondary_profile else 'N/A',
            secondary_profile.get('created_at', 'N/A') if secondary_profile else 'N/A'
        ]
    })
    return comparison_df

def plot_comparison_bar_chart(comparison_df):
    """Plot a bar chart comparing metrics of two profiles with a blue color palette and better layout."""    
    fig = go.Figure()

    blue_palette = ['#1f77b4', '#aec7e8']  # Dark blue and light blue

    # Adjust bar width to prevent overlapping
    bar_width = 0.4

    # Create bar traces
    fig.add_trace(go.Bar(
        x=comparison_df['Metric'],
        y=comparison_df['Primary Owner'],
        name='Primary Owner',
        text=comparison_df['Primary Owner'],
        textposition='auto',
        marker_color=blue_palette[0],
        width=bar_width,
        opacity=0.8
    ))

    fig.add_trace(go.Bar(
        x=comparison_df['Metric'],
        y=comparison_df['Secondary Owner'],
        name='Secondary Owner',
        text=comparison_df['Secondary Owner'],
        textposition='auto',
        marker_color=blue_palette[1],
        width=bar_width,
        opacity=0.8
    ))

    # Update layout
    fig.update_layout(
        title='Profile Comparison',
        xaxis_title='Metric',
        yaxis_title='Value',
        barmode='group',
        bargap=0.3,  # Increase gap between groups
        template='plotly_dark',  # Ensure dark background theme
        xaxis=dict(
            tickvals=comparison_df['Metric'],  # Ensure all metrics are displayed
            ticktext=comparison_df['Metric'],  # Label each metric
            tickangle=-45,  # Rotate x-axis labels for better readability
        ),
        margin=dict(l=40, r=40, t=40, b=80)  # Adjust margins for better layout
    )

    return fig

def display_comparison_with_description(primary_profile, secondary_profile):
    """Generate and display the comparison chart with a description."""
    comparison_df = generate_comparison_dataframe(primary_profile, secondary_profile)
    fig = plot_comparison_bar_chart(comparison_df)
    
    # Display the chart
    st.plotly_chart(fig)
    
    # Determine which profile has higher followers and repos
    primary_followers = primary_profile.get('followers', 0)
    primary_repos = primary_profile.get('public_repos', 0)
    secondary_followers = secondary_profile.get('followers', 0) if secondary_profile else 0
    secondary_repos = secondary_profile.get('public_repos', 0) if secondary_profile else 0
    
    if primary_followers > secondary_followers and primary_repos > secondary_repos:
        description = "The Primary Owner has more followers and repositories than the Secondary Owner. This suggests that the Primary Owner is likely a more engaging user on GitHub compared to the Secondary Owner."
    elif secondary_followers > primary_followers and secondary_repos > primary_repos:
        description = "The Secondary Owner has more followers and repositories than the Primary Owner. This suggests that the Secondary Owner is likely a more engaging user on GitHub compared to the Primary Owner."
    else:
        description = "The engagement levels of the Primary and Secondary Owners are comparable based on the available metrics."

    # Display the description
    st.write(description)
