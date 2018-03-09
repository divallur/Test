import github3
import json
import types
import base64
import sys
import time
from github3.orgs import Organization


USERNAME=sys.argv[1]
PASSWORD=sys.argv[2]

url='xxx'
sess = github3.enterprise_login(url=url, password=PASSWORD, username=USERNAME)

###Creating organization

def create_org(self, org_name, org_display_name, admin_owner_name):
    """Create a new organization.

    If no login was provided, it will be anonymous.

    :param str org_name: (required), The name for the new organization.
    :param str org_display_name: (required), The organization's display name.
    :param str admin_owner_name: (required), The login name of the user who will manage this organization.
    :returns: :class:`Organization <github3.orgs.Organization>`
    """
    args = {'login': org_name, 'profile_name': org_display_name, 'admin': admin_owner_name}
    url = self._build_url('admin', 'organizations')
    result_json = self._json(self._post(url, data=args), 201)
    return self._instance_or_null(Organization, result_json)
github3.github.GitHub.create_org = create_org
org = sess.create_org(sys.argv[3], sys.argv[3], sys.argv[4])



###Forking repository to created organization

repo = sess.repository('interactive-applecom', sys.argv[5])
fork = repo.create_fork(organization=sys.argv[3])
#print fork.name
time.sleep(30)

###Creating an integration branch in forked repository

def sha(self):
   url = self._build_url('repos','interactive-applecom',fork.name,'commits/refs/heads/master')
   result_json = self._json(self._get(url),200)
   b = result_json.get('sha')
   return b     
github3.github.GitHub.sha = sha
b = sess.sha() 
fork.create_ref('refs/heads/integration', b)
  
###Making integration branch as default branch


def default_branch(self,reponame,defaultbranch):
   args = {'name' : reponame ,'default_branch': defaultbranch}
   url = self._build_url('repos',sys.argv[3],fork.name)
   result_json = self._json(self._post(url, data=args), 201)
github3.github.GitHub.default_branch = default_branch
branch = sess.default_branch(fork.name,"integration")

###Creating a team in forked repository

#def team1(self,teamname,reponame,permission):
   #args = {'name' : teamname ,'repo_name': reponame , 'permission' : "admin"}
   #url = self._build_url('orgs',sys.argv[3],'teams')
   #result_json = self._json(self._post(url, data=args), 201)
#github3.github.GitHub.team1 = team1
#te = sess.team1(sys.argv[8],fork.name,"admin")



#def team1(self):
team1 = org.create_team(sys.argv[6],permission='admin')
#team2 = org.create_team(sys.argv[8],permission='admin')
#print team1.id
#team.add_repository(fork.name)
#team.edit(sys.argv[8], permission='admin')

#print a.as_json()
#c = a.id
 #c = a.get('id')

#github3.github.GitHub.team1 = team1
#c = sess.team1()

#v = requests.post('https://interactive-git-dev.rno.apple.com/api/v3/orgs/%s/teams' % (args.orgname), data=json.dumps({ "name": teamname , "description": "team","repo_name": reponame,"permission": "push"}), verify=False, auth=(uname, pw))
#POST /orgs/:org/teams
#PUT /teams/:id/repos/:org/:repo

#GET /orgs/:org/teams

#def teamid(self):
   #url = self._build_url('orgs',sys.argv[3],'teams')
   
   #result_json = self._json(self._get(url),200)
   #print result_json
   #c = result_json.id
   #return c     
#github3.github.GitHub.teamid = teamid
#c = sess.teamid() 
#fork.create_ref('refs/heads/develop', b)

#team.add_repository(fork.name, permission='admin')



#def team(self,permission):
   #args = {'permission' : "admin"}
   #url = self._build_url('teams',team1.id,'repos',sys.argv[3],fork.name)
   #result_json = self._json(self._put(url, data=args), 201)
   #print result_json
#github3.github.GitHub.team = team
#te = sess.team("admin")

###Creating a hook 

fork.create_hook(name='web', config={"url": 'https://jenkins.iapps.apple.com/%s/github-webhook' % sys.argv[7],"content_type": "json"})












   
   