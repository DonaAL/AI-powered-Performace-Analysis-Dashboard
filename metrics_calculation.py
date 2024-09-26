import pandas as pd

def calculate_commit_frequency(commits):
    if not commits:
        return pd.Series()
    
    df_commits = pd.DataFrame([{
        'sha': commit.sha,
        'date': commit.commit.author.date
    } for commit in commits if hasattr(commit.commit, 'author') and hasattr(commit.commit.author, 'date')])
    
    if df_commits.empty:
        return pd.Series()
    
    df_commits['date'] = pd.to_datetime(df_commits['date'])
    df_commits.set_index('date', inplace=True)
    daily_commits = df_commits.resample('D').size()
    
    return daily_commits

def calculate_pr_merge_rate(pull_requests):
    if not pull_requests:
        return {
            'total_prs': 0,
            'merged_prs': 0,
            'merge_rate': 0
        }
    
    df_prs = pd.DataFrame([{
        'title': pr.title,
        'state': pr.state,
        'merged_at': pr.merged_at
    } for pr in pull_requests if hasattr(pr, 'state') and hasattr(pr, 'title')])
    
    if df_prs.empty:
        return {
            'total_prs': 0,
            'merged_prs': 0,
            'merge_rate': 0
        }
    
    total_prs = len(df_prs)
    merged_prs = len(df_prs[df_prs['state'] == 'closed'])
    
    return {
        'total_prs': total_prs,
        'merged_prs': merged_prs,
        'merge_rate': merged_prs / total_prs if total_prs > 0 else 0
    }

def calculate_issue_resolution_time(issues):
    if not issues:
        return 0
    
    df_issues = pd.DataFrame([{
        'title': issue.title,
        'created_at': issue.created_at,
        'closed_at': issue.closed_at
    } for issue in issues if issue.closed_at is not None and hasattr(issue, 'created_at')])
    
    if df_issues.empty:
        return 0
    
    df_issues['created_at'] = pd.to_datetime(df_issues['created_at'])
    df_issues['closed_at'] = pd.to_datetime(df_issues['closed_at'])
    df_issues['resolution_time'] = (df_issues['closed_at'] - df_issues['created_at']).dt.days
    
    average_resolution_time = df_issues['resolution_time'].mean()
    
    return average_resolution_time

def calculate_contributor_activity(commits):
    if not commits:
        return pd.Series()
    
    df_commits = pd.DataFrame([{
        'sha': commit.sha,
        'author': commit.commit.author.name
    } for commit in commits if hasattr(commit.commit, 'author') and hasattr(commit.commit.author, 'name')])
    
    if df_commits.empty:
        return pd.Series()
    
    contributor_activity = df_commits['author'].value_counts()
    
    return contributor_activity

def calculate_top_issues(issues):
    if not issues:
        return pd.DataFrame()
    
    df_issues = pd.DataFrame([{
        'title': issue.title,
        'comments': issue.comments
    } for issue in issues if hasattr(issue, 'comments')])
    
    if df_issues.empty:
        return pd.DataFrame()
    
    top_issues = df_issues.sort_values(by='comments', ascending=False)
    
    return top_issues.head(10)  # Top 10 issues

def calculate_pr_review_time(pull_requests):
    if not pull_requests:
        return 0
    
    df_prs = pd.DataFrame([{
        'title': pr.title,
        'created_at': pr.created_at,
        'merged_at': pr.merged_at
    } for pr in pull_requests if pr.merged_at is not None and hasattr(pr, 'created_at')])
    
    if df_prs.empty:
        return 0
    
    df_prs['created_at'] = pd.to_datetime(df_prs['created_at'])
    df_prs['merged_at'] = pd.to_datetime(df_prs['merged_at'])
    df_prs['review_time'] = (df_prs['merged_at'] - df_prs['created_at']).dt.days
    
    average_review_time = df_prs['review_time'].mean()
    
    return average_review_time

def calculate_issue_age(issues):
    if not issues:
        return 0
    
    df_issues = pd.DataFrame([{
        'title': issue.title,
        'created_at': issue.created_at,
        'closed_at': issue.closed_at
    } for issue in issues if issue.closed_at is not None and hasattr(issue, 'created_at')])
    
    if df_issues.empty:
        return 0
    
    df_issues['created_at'] = pd.to_datetime(df_issues['created_at'])
    df_issues['closed_at'] = pd.to_datetime(df_issues['closed_at'])
    df_issues['age'] = (df_issues['closed_at'] - df_issues['created_at']).dt.days
    
    average_issue_age = df_issues['age'].mean()
    
    return average_issue_age

def calculate_metrics(data):
    commits = data.get('commits', [])
    pull_requests = data.get('pull_requests', [])
    issues = data.get('issues', [])

    metrics = {
        'commit_frequency': calculate_commit_frequency(commits),
        'pr_merge_rate': calculate_pr_merge_rate(pull_requests),
        'issue_resolution_time': calculate_issue_resolution_time(issues),
        'contributor_activity': calculate_contributor_activity(commits),
        'top_issues': calculate_top_issues(issues),
        'pr_review_time': calculate_pr_review_time(pull_requests),
        'issue_age': calculate_issue_age(issues)
    }

    return metrics
