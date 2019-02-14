from jira import JIRA
# based in the following document https://media.readthedocs.org/pdf/jira/stable/jira.pdf


def login_server(server, username, password):
    jira = JIRA(server=server, basic_auth=(username, password))
    return jira


def add_watchers(jira, issue_number, username):
    issue_value = jira.issue(issue_number)
    jira.add_watcher(issue_value, username)


def add_comment(jira, issue_number, comment):
    issue_value = jira.issue(issue_number)
    jira.add_comment(issue_value, comment)


# search_query
def search_query(jira, query):
    query_result = jira.search_issues(query)
    return query_result


# assign issue
def assignee_issue(jira, issue_number, username):
    issue_value = jira.issue(issue_number)
    jira.assign_issue(issue_value, username)


# get all field of one issue
def get_all_issue_fields(jira, issue_number):
    issue_value = jira.issue(issue_number)
    for field_name in issue_value.raw['fields']:
        if 'custom' not in str(field_name):
            print("Field:", field_name, " | Value:", issue_value.raw['fields'][field_name])


def create_sub_task(jira, component, project, issue_type, parent, assignee, summary, description):
    issue_fields = {
        'project':
            {
                'key': project,
            },
        'parent':
            {
                'key': parent,
            },
        'issuetype': issue_type,
        'assignee':
            {
                'name': assignee,
            },
        'description': description,
        'summary': summary,
        'components': [{'name': component}]
    }
    new_issue = jira.create_issue(fields=issue_fields)
    return new_issue
