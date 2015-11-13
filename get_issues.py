import requests
import pprint
from settings import *
'''
Creation of a token is documented at
https://help.github.com/articles/creating-an-access-token-for-command-line-use/
'''

def calculate_pages(request):
    for item in request.headers['link'].split(','):
#        print item
        if 'last' in item.split(';')[1]:
            start = item.split(';')[0].find('page')
            end = item.split(';')[0].find('>')
            return int(item.split(';')[0][start:end].split('=')[1])


"""get_all_issues_of_organization will list down all the issues of all
 repos of an organization """

def get_all_issues_of_organization(request):
    global result
    if request is None:
        url = "https://api.github.com/orgs/Virtual-Labs/issues?filter=all&state=all"
#       Sending request to list all the issues under Virtual-Labs organization
        request = requests.get(url, auth=auth1)
#        print "Number of pages: ", calculate_pages(request)
        result = request.json()
        url = request.links['next']['url']
        new_request = requests.get(url, auth=auth1)
        get_all_issues_of_organization(new_request)

    else:
#        print request.links.keys()   """Everytime it returns ['prev', 'first',
#                                       'last', 'next'] but only in last page we
#                                         get ['prev', 'first']"""
        if 'last' not in request.links.keys():
            result.extend(request.json())
            return
        else:
            url = request.links['next']['url']
            new_request = requests.get(url, auth=auth1)
            result.extend(request.json())
            get_all_issues_of_organization(new_request)


def print_all_issues():
        for issue in result:
            print "\n issue URL:"+issue['url']
            for label in issue['labels']:
                    print "label name:"+label['name']

def get_only_issues_with_lables():
        for issue in result:
            if issue['labels'] == []:
                pass
            else:
                re = filter_issues(issue['labels'],filter_labels)
                if re == True:
                    print "\n issue URL:"+issue['url']
                    for label in issue['labels']:
                        print "label name:"+label['name']


"""filter_issues function filters issues based on labels(filter_labels) passed
as a list.This function gets lables names from a single issue and form a
 list(label_names),later label_names is converted into a set and filter_labels
 is also converted into a set,If comparision of both the sets fetch a set of
 filter_lables, then the search is True else False     """

def filter_issues(labels, filter_labels):
    label_names =[]
    for label in labels:
        label_names.append(label['name'])
    if set(filter_labels).intersection(set(label_names)) == set(filter_labels):
        return True
    else:
        return False

def get_issues_for_each_repo(repos):
    for repo in repos:
        url = "%s%s%s" % ('https://api.github.com/repositories/',
                          repo['id'],
                          '/issues')
        print url
        result = requests.get(url, auth=auth1).json()
        if (result == []):
            pass
        else:
            pprint.pprint(result)

def get_repos(get_object):
    global repos
    if get_object is None:
        url = 'https://api.github.com/orgs/Virtual-Labs/repos'
        request = requests.get(url, auth=auth1)
        get_repos(request)

    else:
        if 'last' not in get_object.links.keys():
            repos.extend(get_object.json())
            return
        else:
            url = get_object.links['next']['url']
            request = requests.get(url, auth=auth1)
            repos.extend(get_object.json())
            get_repos(request)


if __name__ == '__main__':
  result = []
  get_all_issues_of_organization(None)
  filter_labels=['help wanted']
#  print_all_issues()
  get_only_issues_with_lables()

#  repos = []
#  get_repos(None)
#  pprint.pprint(repos)
#  get_issues_for_each_repo(repos)
#  filter_lables([])
