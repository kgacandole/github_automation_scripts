import sys, requests

githubPat = sys.argv[1]
repoName = sys.argv[2]
repoOwner = sys.argv[3]
wfName = sys.argv[4]

ghHeaders = { 
    "Authorization": "Bearer " + githubPat, 
    "X-GitHub-Api-Version": "2022-11-28", 
    "Accept": "application/vnd.github+json"
}

pageCounter = 1
save_build = [] # List workflow IDs to be skipped

repoUrl = "https://api.github.com/repos/" + repoOwner "/" + repoName + "/actions/runs?page=" + str(pageCounter)
getListofRuns = requests.get(repoUrl, headers = ghHeaders).json()
print("Found total of ", getListofRuns['total_count'], " workflow runs.")

while getListofRuns['workflow_runs'] != []:
    print("Querying page " + str(pageCounter))
    for runs in getListofRuns['workflow_runs']:
        runId = str(runs['id'])
        if(runId in save_build):
            print("Skipping ", runId)
        else:
            wfPath = runs['path']

            if wfName in wfPath:
                 try:
                     deleteUrl = "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/actions/runs/" + runId
                     deleteRun = requests.delete(deleteUrl, headers = ghHeaders)
                     print("Deleted ", runId, " : ", deleteRun)
                 except Exception as e:
                     print("Error deleting ", runId, " : ", e)
 
    pageCounter = pageCounter + 1
    getListofRuns = requests.get(repoUrl, headers = ghHeaders).json()
