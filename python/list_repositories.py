import sys, requests

tokenId = sys.argv[1]
ownerName = sys.argv[2]
maxCounter = int(sys.argv[3])
search_strings = sys.argv[4]

ghUrl = "https://api.github.com/users/" + ownerName + "/repos"
ghHeaders = { 
    "Authorization": "Bearer " + tokenId, 
    "X-GitHub-Api-Version": "2026-03-10", 
    "Accept": "application/vnd.github+json"
}

for x in range(maxCounter):
    url = ghUrl + "?per_page=" + str(maxCounter) + "&page=" + str(x + 1)
    getRepos = requests.get(url, headers = ghHeaders).json()
    try:
        for repos in getRepos:
            reponame = repos['name']
            print(reponame)
            if any(validstr in reponame for validstr in search_strings.split(",")):                
                with open("repo_list.txt", "a") as f:
                    f.write(reponame + "\n")
    except Exception as e:
        raise RuntimeError("Unable to get repositories") from e