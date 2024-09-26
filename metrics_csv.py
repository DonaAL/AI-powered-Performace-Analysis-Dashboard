import pandas as pd
import os

def ensure_directory_exists(directory):
    """Ensure the directory exists, create it if not."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def export_commit_frequency(commit_frequency, file_path='./'):
    ensure_directory_exists(file_path)
    df_commit_frequency = pd.DataFrame(commit_frequency, columns=['Commit Frequency'])
    full_path = os.path.join(file_path, 'commit_frequency.csv')
    df_commit_frequency.to_csv(full_path, index=True)
    print(f"Commit frequency saved to '{full_path}'.")

def export_pr_merge_rate(pr_merge_rate, file_path='./'):
    ensure_directory_exists(file_path)
    df_pr_merge_rate = pd.DataFrame([pr_merge_rate], columns=['Total PRs', 'Merged PRs', 'Merge Rate'])
    full_path = os.path.join(file_path, 'pr_merge_rate.csv')
    df_pr_merge_rate.to_csv(full_path, index=False)
    print(f"PR merge rate saved to '{full_path}'.")

def export_issue_resolution_time(issue_resolution_time, file_path='./'):
    ensure_directory_exists(file_path)
    df_issue_resolution = pd.DataFrame([{'Average Resolution Time': issue_resolution_time}])
    full_path = os.path.join(file_path, 'issue_resolution_time.csv')
    df_issue_resolution.to_csv(full_path, index=False)
    print(f"Issue resolution time saved to '{full_path}'.")

def export_contributor_activity(contributor_activity, file_path='./'):
    ensure_directory_exists(file_path)
    df_contributor_activity = pd.DataFrame(contributor_activity)
    full_path = os.path.join(file_path, 'contributor_activity.csv')
    df_contributor_activity.to_csv(full_path, index=True)
    print(f"Contributor activity saved to '{full_path}'.")

def export_top_issues(top_issues, file_path='./'):
    ensure_directory_exists(file_path)
    df_top_issues = pd.DataFrame(top_issues)
    full_path = os.path.join(file_path, 'top_issues.csv')
    df_top_issues.to_csv(full_path, index=False)
    print(f"Top issues saved to '{full_path}'.")

def export_pr_review_time(pr_review_time, file_path='./'):
    ensure_directory_exists(file_path)
    df_pr_review_time = pd.DataFrame([{'Average Review Time': pr_review_time}])
    full_path = os.path.join(file_path, 'pr_review_time.csv')
    df_pr_review_time.to_csv(full_path, index=False)
    print(f"PR review time saved to '{full_path}'.")

def export_issue_age(issue_age, file_path='./'):
    ensure_directory_exists(file_path)
    df_issue_age = pd.DataFrame([{'Average Issue Age': issue_age}])
    full_path = os.path.join(file_path, 'issue_age.csv')
    df_issue_age.to_csv(full_path, index=False)
    print(f"Issue age saved to '{full_path}'.")

def export_all_metrics(metrics, file_path='./'):
    """Export all metrics to the specified file path, ensuring the directory exists."""
    ensure_directory_exists(file_path)
    export_commit_frequency(metrics['commit_frequency'], file_path)
    export_pr_merge_rate(metrics['pr_merge_rate'], file_path)
    export_issue_resolution_time(metrics['issue_resolution_time'], file_path)
    export_contributor_activity(metrics['contributor_activity'], file_path)
    export_top_issues(metrics['top_issues'], file_path)
    export_pr_review_time(metrics['pr_review_time'], file_path)
    export_issue_age(metrics['issue_age'], file_path)
    print(f"All metrics exported to CSV files at '{file_path}'.")

