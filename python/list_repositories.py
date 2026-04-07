import sys, requests

tokenId = sys.argv[1]
maxCounter = int(sys.argv[2])
search_strings = sys.argv[3]
skip_strings = sys.argv[4]
ownerName = sys.argv[5]

ghUrl = "https://api.github.com/orgs/" + ownerName + "/repos"
ghHeaders = { 
    "Authorization": "Bearer " + tokenId, 
    "X-GitHub-Api-Version": "2022-11-28", 
    "Accept": "application/vnd.github+json"
}

for x in range(maxCounter):
    url = ghUrl + "?per_page=" + str(maxCounter) + "&page=" + str(x)
    getRepos = requests.get(url, headers = ghHeaders).json()
    print(getRepos)
    for repos in getRepos:
        print(repos)
        reponame = repos['name']

        if search_strings != "":        
            if any(validstr in reponame for validstr in search_strings.split(",")):
                if skip_strings != "" and not any(excemptrepo in reponame for excemptrepo in skip_strings.split(",")):
                    with open("repo_list.txt", "a") as f:
                        f.write(reponame + "\n")