import requests

githubPat = sys.argv[1]
githubOwner = sys.argv[1]

githubUri = "https://api.github.com/repos/" + githubOwner + "/"

ghHeaders = { 
    "Authorization": "Bearer " + githubPat, 
    "X-GitHub-Api-Version": "2022-11-28", 
    "Accept": "application/vnd.github+json"
}

repo_list = [] # Add list of repos
repo_vars = [ 
    "VARNAME:VALUE"
] # Add variables

for repo in repo_list:    
    fullGithubUri = githubUri + repo + "/actions/variables"    
    for vars in repo_vars:
        payload = {
            "name": vars.split(":")[0],
            "value": vars.split(":")[1]
        }
        print("Adding var, ", vars)
        result = requests.post(fullGithubUri, headers=ghHeaders, json=payload)        
        print("Successfully added vars: ", result.json())