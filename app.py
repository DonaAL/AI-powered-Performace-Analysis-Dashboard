import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.io import write_image
import plotly.io as pio

# Ensure that the kaleido package is installed for exporting charts
# You can install it using: pip install kaleido
pio.kaleido.scope.default_format = "png"

from github_data import collect_github_data
from metrics_calculation import calculate_metrics
from metrics_csv import export_all_metrics
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
from query_module import handle_user_query  # Import the query handling function
import comparison

def main():
    st.set_page_config(layout="wide")
    st.title("Developer Performance Analytics Dashboard")

    # Sidebar inputs
    st.sidebar.header("Repository Information")
    repo_url = st.sidebar.text_input("Enter GitHub repository URL (owner/repo):", "octocat/Hello-World")
    token = st.sidebar.text_input("Enter your GitHub token:", type="password")
    second_owner_login = st.sidebar.text_input("Enter secondary owner's GitHub login (optional):", "")

    st.sidebar.header("Filters")
    pr_states = st.sidebar.multiselect("Filter Pull Requests by State", ['open', 'closed', 'all'], default=['all'])
    issue_labels = st.sidebar.multiselect("Filter Issues by Label", [])

    if st.sidebar.button("Fetch Data"):
        with st.spinner("Fetching data..."):
            try:
                # Fetch data from GitHub
                data = collect_github_data(repo_url, token, second_owner_login)
                if data:
                    st.success("Data successfully fetched!")

                    if second_owner_login:
                        primary_profile = data['owner_profile']
                        secondary_profile = data['second_owner_profile']
                        comparison_df = comparison.generate_comparison_dataframe(primary_profile, secondary_profile)
                        comparison_chart = comparison.plot_comparison_bar_chart(comparison_df)
                        data['comparison_results'] = comparison_chart  # Add comparison results to data 

                    # Calculate Metrics and Visualizations
                    metrics = calculate_metrics(data)
                    st.session_state.metrics = metrics
                    # Repository Information Box
                    st.markdown(
                        """
                        <div style="border: 2px solid #d1d5db; border-radius: 5px; padding: 10px;">
                            <h2 style="text-align: center; margin: 0;">Repository Information</h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    # Display repository information
                    repo_info = data['repo_info']
                    st.markdown(f"**Name:** {repo_info['name']}")
                    st.markdown(f"**Description:** {repo_info['description']}")
                    st.markdown(f"**URL:** [Repository Link]({repo_info['url']})")
                    st.markdown(f"**Stars:** {repo_info['stars']}")
                    st.markdown(f"**Forks:** {repo_info['forks']}")
                    st.markdown(f"**Watchers:** {repo_info['watchers']}")
                    st.markdown(f"**Primary Language:** {repo_info['language']}")

                    # Alerts and Insights
                    avg_pr_review_time = metrics.get('pr_review_time', 0)
                    if avg_pr_review_time > 20:
                        st.warning(f"⚠️ The average PR review time is {avg_pr_review_time:.2f} days, which is higher than the recommended threshold!")

                    avg_issue_resolution_time = metrics.get('issue_resolution_time', 0)
                    if avg_issue_resolution_time > 30:
                        st.warning(f"⚠️ The average issue resolution time is {avg_issue_resolution_time:.2f} days, which is higher than the recommended threshold!")

                    # Repository Languages and Metrics Box
                    st.markdown(
                        """
                        <div style="border: 2px solid #d1d5db; border-radius: 5px; padding: 10px;">
                            <h2 style="text-align: center; margin: 0;">Metrics</h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    with st.container():
                        st.markdown(
    """
    <div style="border: 2px solid #d1d5db; border-radius: 5px; padding: 10px;">
        <h3>Calculated Metrices</h3>
        <ul style="list-style-type: none; padding: 0; font-size: 18px;">
            <li><strong>Commit Frequency</strong>: Shows the number of commits made on a daily basis.</li>
            <li><strong>PR Merge Rate</strong>: Represents the ratio of merged pull requests to total pull requests.</li>
            <li><strong>Issue Resolution Time</strong>: Indicates the average time taken to resolve issues.</li>
            <li><strong>Contributor Activity</strong>: Displays the activity level of contributors based on commit counts.</li>
            <li><strong>Top Issues</strong>: Lists the issues with the most comments.</li>
            <li><strong>PR Review Time</strong>: Measures the average time taken to review and merge pull requests.</li>
            <li><strong>Issue Age</strong>: Shows the average age of issues from creation to closure.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)
                        
                 
                    # Repository Languages and Metrics
                    languages = data['languages']
                    
                    # Define columns for charts and descriptions
                    col1, col2 = st.columns([1, 2])  # Adjust column widths if needed

                    # Language Distribution Chart
                    with col1:
                        st.write("### Repository Language Distribution")
                        if languages:
                            lang_df = pd.DataFrame(list(languages.items()), columns=['Language', 'Bytes'])
                            fig_languages = plot_language_distribution(lang_df)
                            st.plotly_chart(fig_languages, use_container_width=True)
                            # Export button
                            if st.button("Export Language Distribution Chart as PNG"):
                                fig_languages.write_image("language_distribution_chart.png")
                                st.success("Chart saved as language_distribution_chart.png")
                        else:
                            st.write("No language data available.")

                    # Commit Frequency Chart
                    with col2:
                        st.write("### Commit Frequency")
                        commit_frequency_df = metrics.get('commit_frequency', pd.DataFrame())
                        if not commit_frequency_df.empty:
                            if commit_frequency_df.index.tz is not None:
                                commit_frequency_df.index = commit_frequency_df.index.tz_localize(None)

                            start_date = st.date_input("Start Date", commit_frequency_df.index.min().date())
                            end_date = st.date_input("End Date", commit_frequency_df.index.max().date())

                            filtered_df = commit_frequency_df.loc[start_date:end_date]
                            if not filtered_df.empty:
                                fig_commits = plot_commit_frequency(filtered_df)
                                st.plotly_chart(fig_commits, use_container_width=True)
                                # Export button
                                if st.button("Export Commit Frequency Chart as PNG"):
                                    fig_commits.write_image("commit_frequency_chart.png")
                                    st.success("Chart saved as commit_frequency_chart.png")
                            else:
                                st.write("No commit frequency data available for the selected date range.")
                        else:
                            st.write("No commit frequency data available.")

                    # Next set of charts
                    col1, col2 = st.columns([1, 2])  # Reuse columns

                    # Pull Request Merge Rate Chart
                    with col1:
                        st.write("### Pull Request Merge Rate")
                        merge_rate = metrics.get('pr_merge_rate', {})
                        fig_merge_rate = plot_pull_request_merge_rate(merge_rate)
                        st.plotly_chart(fig_merge_rate, use_container_width=True)
                        # Export button
                        if st.button("Export PR Merge Rate Chart as PNG"):
                            fig_merge_rate.write_image("pr_merge_rate_chart.png")
                            st.success("Chart saved as pr_merge_rate_chart.png")

                    # Average Issue Resolution Time Gauge
                    with col2:
                        st.write("### Average Issue Resolution Time")
                        avg_issue_resolution_time = metrics.get('issue_resolution_time', 0)
                        fig_issue_resolution_time = plot_average_issue_resolution_time(avg_issue_resolution_time)
                        st.plotly_chart(fig_issue_resolution_time, use_container_width=True)
                        # Export button
                        if st.button("Export Issue Resolution Time Gauge as PNG"):
                            fig_issue_resolution_time.write_image("issue_resolution_time_gauge.png")
                            st.success("Chart saved as issue_resolution_time_gauge.png")

                    # Contributor Activity and Top Issues
                    col1, col2 = st.columns([1, 2])

                    with col1:
                        st.write("### Contributor Activity")
                        contributor_activity_df = metrics.get('contributor_activity', pd.DataFrame())
                        if not contributor_activity_df.empty:
                            fig_contributor_activity = plot_contributor_activity(contributor_activity_df)
                            st.plotly_chart(fig_contributor_activity, use_container_width=True)
                            # Export button
                            if st.button("Export Contributor Activity Chart as PNG"):
                                fig_contributor_activity.write_image("contributor_activity_chart.png")
                                st.success("Chart saved as contributor_activity_chart.png")
                        else:
                            st.write("No contributor activity data available.")

                    with col2:
                        st.write("### Top Issues by Comments")
                        top_issues_df = metrics.get('top_issues', pd.DataFrame())
                        if not top_issues_df.empty and {'title', 'comments'}.issubset(top_issues_df.columns):
                            fig_top_issues = plot_top_issues_by_comments(top_issues_df)
                            st.plotly_chart(fig_top_issues, use_container_width=True)
                            # Export button
                            if st.button("Export Top Issues Chart as PNG"):
                                fig_top_issues.write_image("top_issues_chart.png")
                                st.success("Chart saved as top_issues_chart.png")
                        else:
                            st.write("No top issues data available.")

                    # Average PR Review Time and Issue Age
                    col1, col2 = st.columns([1, 2])

                    with col1:
                        st.write("### Average Pull Request Review Time")
                        avg_pr_review_time = metrics.get('pr_review_time', 0)
                        fig_pr_review_time = plot_average_pull_request_review_time(avg_pr_review_time)
                        st.plotly_chart(fig_pr_review_time, use_container_width=True)
                        # Export button
                        if st.button("Export PR Review Time Gauge as PNG"):
                            fig_pr_review_time.write_image("pr_review_time_gauge.png")
                            st.success("Chart saved as pr_review_time_gauge.png")

                    with col2:
                        st.write("### Average Issue Age")
                        avg_issue_age = metrics.get('issue_age', 0)
                        fig_issue_age = plot_average_issue_age(avg_issue_age)
                        st.plotly_chart(fig_issue_age, use_container_width=True)
                        # Export button
                        if st.button("Export Issue Age Gauge as PNG"):
                            fig_issue_age.write_image("issue_age_gauge.png")
                            st.success("Chart saved as issue_age_gauge.png")

                    # Detailed Views using Expanders

                    # Pull Requests with Code Reviews
                    with st.expander("Pull Request Details"):
                        pr_data = []
                        for pr in data.get('pull_requests', []):
                            # Filter PRs based on selected states
                            if 'all' in pr_states or pr.state in pr_states:
                                pr_data.append({
                                    "Title": pr.title,
                                    "State": pr.state,
                                    "Created At": pr.created_at,
                                    "Reviews Count": len(pr.reviews) if pr.reviews else 0
                                })
                        if pr_data:
                            pr_df = pd.DataFrame(pr_data)
                            st.dataframe(pr_df)
                        else:
                            st.write("No pull requests found.")

                    # Issues with Details
                    with st.expander("Issue Details"):
                        issue_data = []
                        for issue in data.get('issues', []):
                            # Filter issues based on selected labels
                            if not issue_labels or any(label.name in issue_labels for label in issue.labels):
                                issue_data.append({
                                    "Title": issue.title,
                                    "State": issue.state,
                                    "Created At": issue.created_at,
                                    "Comments": issue.comments
                                })
                        if issue_data:
                            issue_df = pd.DataFrame(issue_data)
                            st.dataframe(issue_df)
                        else:
                            st.write("No issues found.")

                    # Export metrics to CSV with custom path if provided
                    st.subheader("Export Metrics to CSV")
                    custom_path="C:\\Users\\donaa\\OneDrive\\Desktop\\surspa2\\csv"
                    if st.button("Export Metrics"):
                        if custom_path:
                            export_all_metrics(metrics, file_path=custom_path)
                        else:
                            export_all_metrics(metrics)  # Default path (current directory)
                        st.success("Metrics exported successfully!")

                    # Profile Information
                    st.markdown(
                        """
                        <div style="border: 2px solid #d1d5db; border-radius: 5px; padding: 10px;">
                            <h2 style="text-align: center; margin: 0;">Profile Information</h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    profile_col1, profile_col2 = st.columns(2)

                    with profile_col1:
                        st.markdown("**Primary Owner Profile:**")
                        primary_owner_profile = data.get('owner_profile', {})
                        st.markdown(f"**Username:** {primary_owner_profile.get('login', 'N/A')}")
                        st.markdown(f"**Name:** {primary_owner_profile.get('name', 'N/A')}")
                        st.markdown(f"**Bio:** {primary_owner_profile.get('bio', 'N/A')}")
                        st.markdown(f"**Location:** {primary_owner_profile.get('location', 'N/A')}")
                        st.markdown(f"**Company:** {primary_owner_profile.get('company', 'N/A')}")
                        st.markdown(f"**Email:** {primary_owner_profile.get('email', 'N/A')}")
                        st.markdown(f"**Public Repos:** {primary_owner_profile.get('public_repos', 0)}")
                        st.markdown(f"**Followers:** {primary_owner_profile.get('followers', 0)}")
                        st.markdown(f"**Following:** {primary_owner_profile.get('following', 0)}")
                        st.markdown(f"**Created At:** {primary_owner_profile.get('created_at', 'N/A')}")
                        st.markdown(f"**Updated At:** {primary_owner_profile.get('updated_at', 'N/A')}")
                        st.markdown(f"**Profile URL:** [Profile Link](https://github.com/{primary_owner_profile.get('login', 'N/A')})")

                    with profile_col2:
                        secondary_owner_login = data.get('second_owner_profile', {}).get('login')
                        if secondary_owner_login:
                            st.markdown("**Secondary Owner Profile:**")
                            secondary_owner_profile = data.get('second_owner_profile', {})
                            st.markdown(f"**Username:** {secondary_owner_profile.get('login', 'N/A')}")
                            st.markdown(f"**Name:** {secondary_owner_profile.get('name', 'N/A')}")
                            st.markdown(f"**Bio:** {secondary_owner_profile.get('bio', 'N/A')}")
                            st.markdown(f"**Location:** {secondary_owner_profile.get('location', 'N/A')}")
                            st.markdown(f"**Company:** {secondary_owner_profile.get('company', 'N/A')}")
                            st.markdown(f"**Email:** {secondary_owner_profile.get('email', 'N/A')}")
                            st.markdown(f"**Public Repos:** {secondary_owner_profile.get('public_repos', 0)}")
                            st.markdown(f"**Followers:** {secondary_owner_profile.get('followers', 0)}")
                            st.markdown(f"**Following:** {secondary_owner_profile.get('following', 0)}")
                            st.markdown(f"**Created At:** {secondary_owner_profile.get('created_at', 'N/A')}")
                            st.markdown(f"**Updated At:** {secondary_owner_profile.get('updated_at', 'N/A')}")
                            st.markdown(f"**Profile URL:** [Profile Link](https://github.com/{secondary_owner_profile.get('login', 'N/A')})")                      
                        else:
                                st.markdown("**Secondary Owner Profile:**")
                                st.markdown("No secondary owner information available.")
                    st.markdown(
                        """
                        <div style="border: 2px solid #d1d5db; border-radius: 5px; padding: 10px; margin-top: 20px;">
                            <h2 style="text-align: center; margin: 0;">Comparison Results</h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    comparison_chart = data.get('comparison_results')
                    if comparison_chart:
                        st.write("### Metrics Comparison")
                        st.plotly_chart(comparison_chart, use_container_width=True)
                        
                    else:
                     st.write("No comparison data available.")


                else:
                    st.error("Failed to fetch data. Please check your inputs and try again.")

            except Exception as e:
                st.error(f"Error fetching data: {e}")


    # Query Section
    st.sidebar.header("Natural Language Queries")
    query = st.sidebar.text_input("Enter your query:", "")
    if st.sidebar.button("Submit Query"):
        if 'metrics' in st.session_state and query:
            with st.spinner("Processing query..."):
                try:
                    # Handle the user's query and display results
                    fig, description = handle_user_query(query, st.session_state.metrics)
                    st.write("### Query Results")
                    if fig:
                        st.write(description)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No results for the given query.")
                except Exception as e:
                    st.error(f"Error processing query: {e}")
        else:
            if not query:
                st.warning("Please enter a query.")
            if 'metrics' not in st.session_state:
                st.warning("No metrics available. Please fetch data first.")

if __name__ == "__main__":
    main()