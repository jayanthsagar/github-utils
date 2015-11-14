import requests
import pprint
from settings import *
'''
Creation of a token is documented at
https://help.github.com/articles/creating-an-access-token-for-command-line-use/
'''

class Get_issues:
    def calculate_pages(request):
        for item in request.headers['link'].split(','):
    #        print item
            if 'last' in item.split(';')[1]:
                start = item.split(';')[0].find('page')
                end = item.split(';')[0].find('>')
                return int(item.split(';')[0][start:end].split('=')[1])


    """get_all_issues_of_organization takes Organization ID and request as input and writes all the issues of all
     repos of an organization into a list(result) """

    def get_all_issues(self,option,id,request):
        global result
        if request is None:
            if option == "org":
                url = "%s%s%s" %("https://api.github.com/orgs/", id ,"/issues?filter=all&state=all")
            elif option == "institute":
                pass
            elif option == "lab":
                pass
            else:
                print "choose option within (org, institute, lab) only"
            print url
    #       Sending request to list all the issues under Virtual-Labs organization
            request = requests.get(url, auth=auth1)
    #        print "Number of pages: ", calculate_pages(request)
            result = request.json()
            print result
            if 'last' not in request.links.keys():
                return
            else:
                url = request.links['next']['url']
                new_request = requests.get(url, auth=auth1)
                self.get_all_issues(option,id,new_request)

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
                self.get_all_issues(option,id,new_request)


    def write_all_issues_to_a_file_after_applying_filter(self,filter):
        filter_labels = filter.split(',')
        count = 0
#        print filter_labels
        f = open("./templates/result.html",'w')
        for issue in result:
            if issue['labels'] == []:
                pass
            else:
                re = self.filter_issues(issue['labels'],filter_labels)
                labels = []
                if re == True:
                    count = count+1
                    for label in issue['labels']:
                        labels.append(str(label['name']).encode('utf8'))
                    string="<br>URL of repo: %s<br>Labels: %s<br>Title of Issue %s<br>State of issue: %s<br>created by:%s<br>"% (issue['html_url'],labels,issue['title'],issue['state'],issue['user']['login'])
                    f.write("<tr> %s  <tr> " % string.encode('utf8'))
        f.write(str(count))
        f.close()

    def filter_issues_with_lables(self,filter_labels):
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

    def filter_issues(self,labels, filter_labels):
        label_names =[]
        for label in labels:
            label_names.append(label['name'])
        if set(filter_labels).intersection(set(label_names)) == set(filter_labels):
            return True
        else:
            return False

    def get_issues_for_a_single_repo(self,repo_name):
        self.get_repos(None)
        for repo in self.repos:
            url = "%s%s%s" % ('https://api.github.com/repositories/',
                              repo['id'],
                              '/issues?filter=all&state=all')
#            print url
            result = requests.get(url, auth=auth1).json()
            if (result == []):
                pass
            else:
                for a in result:
                    print a['html_url']

    def get_issues_for_each_repo(self,repos):
        for repo in repos:
            url = "%s%s%s" % ('https://api.github.com/repositories/',
                              repo['id'],
                              '/issues?filter=all&state=all')
            print url
            result = requests.get(url, auth=auth1).json()
            if (result == []):
                pass
            else:
                pprint.pprint(result)

    def get_repos(self,get_object):
        global repos
        if get_object is None:
            url = 'https://api.github.com/orgs/Virtual-Labs/repos'
            request = requests.get(url, auth=auth1)
            self.get_repos(request)

        else:
            if 'last' not in get_object.links.keys():
                self.repos.extend(get_object.json())
                return
            else:
                url = get_object.links['next']['url']
                request = requests.get(url, auth=auth1)
                self.repos.extend(get_object.json())
                self.get_repos(request)

#c = Get_issues()
#if __name__ == '__main__':
#c.result = []
#c.repos = []
#c.get_all_issues('org','Virtual-Labs',None)
#c.print_all_issues()
#c.get_issues_for_a_single_repo('cse02-iiith')
#  filter_labels=['help wanted']
#  print_all_issues()
#  get_only_issues_with_lables()
#  get_repos(None)
#  pprint.pprint(repos)
#  get_issues_for_each_repo(repos)
#  filter_lables([])
