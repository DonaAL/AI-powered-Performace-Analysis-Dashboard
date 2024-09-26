from github import Github, RateLimitExceededException
import time
from concurrent.futures import ThreadPoolExecutor

MAX_PAGES = 1  # Limit to 1 page for demonstration
MAX_CONTRIBUTORS_PAGES = 1  # Limit contributors pages to avoid high load

def fetch_paginated_data(fetch_function, *args, **kwargs):
    all_items = []
    page = 1
    while page <= MAX_PAGES:
        print(f"Fetching page {page}")
        try:
            items = fetch_function(*args, **kwargs)
            if not items:
                break
            all_items.extend(items)
            page += 1
        except RateLimitExceededException as e:
            print(f"Rate limit exceeded: {e}. Sleeping for 60 seconds.")
            time.sleep(60)  # Sleep to avoid hitting the rate limit
        except Exception as e:
            print(f"Error fetching data on page {page}: {e}")
            break
    return all_items

def collect_github_data(repo_url, token, second_owner_login=None):
    g = Github(token)
    repo = g.get_repo(repo_url)

    def fetch_commits():
        return repo.get_commits()

    def fetch_pull_requests():
        return repo.get_pulls(state='all', sort='created', direction='desc')

    def fetch_issues():
        return repo.get_issues(state='all', sort='created', direction='desc')

    def fetch_languages():
        return repo.get_languages()

    def fetch_contributors():
        # Fetch contributors with a page limit to avoid high load
        return fetch_paginated_data(repo.get_contributors)

    def fetch_profile_data(username):
        user = g.get_user(username)
        profile_data = {
            'login': user.login,
            'name': user.name,
            'bio': user.bio,
            'public_repos': user.public_repos,
            'followers': user.followers,
            'following': user.following,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
            'company': user.company,
            'location': user.location,
            'email': user.email
        }
        return profile_data

    repo_info = {
        'name': repo.name,
        'description': repo.description,
        'url': repo.html_url,
        'stars': repo.stargazers_count,
        'forks': repo.forks_count,
        'watchers': repo.watchers_count,
        'language': repo.language,
    }

    try:
        commits = fetch_paginated_data(fetch_commits)
        pull_requests = fetch_paginated_data(fetch_pull_requests)
        issues = fetch_paginated_data(fetch_issues)
        languages = fetch_languages()
        contributors = fetch_contributors()

        # Fetch code reviews for each pull request
        for pr in pull_requests:
            try:
                reviews = pr.get_reviews()
                pr.reviews = list(reviews)  # Convert to list for easy processing
            except Exception as e:
                print(f"Error fetching reviews for PR {pr.number}: {e}")

        # Fetch profile data for repository owner
        owner_profile = fetch_profile_data(repo.owner.login)
        
        # Fetch profile data for the second owner if provided
        second_owner_profile = None
        if second_owner_login:
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = {
                    executor.submit(fetch_profile_data, repo.owner.login): 'first_owner',
                    executor.submit(fetch_profile_data, second_owner_login): 'second_owner'
                }
                results = {}
                for future in futures:
                    owner_type = futures[future]
                    try:
                        results[owner_type] = future.result()
                    except Exception as e:
                        print(f"Error fetching {owner_type} profile: {e}")

            second_owner_profile = results.get('second_owner')

        return {
            'repo_info': repo_info,
            'commits': commits,
            'pull_requests': pull_requests,
            'issues': issues,
            'languages': languages,
            'contributors': contributors,
            'owner_profile': owner_profile,
            'second_owner_profile': second_owner_profile
        }
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
