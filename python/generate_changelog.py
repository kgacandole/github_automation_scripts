import subprocess, re, sys

githubOrgName = sys.argv[1]
repoName = sys.argv[2]

def executeCli(commandArr):
    return subprocess.run(commandArr,
        capture_output=True,
        text=True
    ).stdout.strip()

def getTagDate(tagname):
    tag_date = ""
    get_tag_date = executeCli([ "git", "show", tagname, "--no-patch", "--pretty=format:\"%ai\""])
    if "Tagger" in get_tag_date:
        date_pattern = r"\d{4}-\d{2}-\d{2}"
        for get_tag in get_tag_date.split("\n"):
            extract_date = re.search(date_pattern, get_tag)
            if get_tag != "" and extract_date:
                tag_date = extract_date.group(0)
    else:
        tag_date = get_tag_date
    tag_date = tag_date.replace("\"", "").split()[0].strip()

    return tag_date

compareUrl = "https://github.com/" + githubOrgName + "/" + repoName + "/compare"
hashurl = "https://github.com/" + githubOrgName + "/" + repoName + "/commit/"

with open("CHANGELOG.md", "a") as ch:
    ch.write("# Changelog\n\n")
    ch.write("All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.\n\n")

    # Get Tags
    tags_list = executeCli([ "git", "tag", "--sort=v:refname" ]).split("\n")
    version_pattern = r"^v\d+\.\d+\.\d+$"
    filter_tags = []
    for tag in tags_list:
        if re.match(version_pattern, tag):
            filter_tags.append(tag)

    # Get Commits and Changes
    for x in range(len(filter_tags) - 1, 0, -1):
        tagname = filter_tags[x]
        tag_date = getTagDate(tagname)
        fullcompareUrl = compareUrl + "/" + filter_tags[x - 1] + "..." + tagname        
        ch.write("\n\n## [" + tagname.replace("v", "") + "](" + fullcompareUrl + ") (" + tag_date + ")\n\n")
        
        # Get Change log
        commits = executeCli(["git", "log", filter_tags[x - 1] + ".." + tagname, "--pretty=format:%s (%an)|%h|%H", "--grep=feat", "--grep=fix", "--no-merges", "--reverse" ]).split("\n")   
        fixCommits = []
        featCommits = []
        for com in commits:
            if com:
                commitLine = com.split("|")[0]
                shortHash = com.split("|")[1]
                longHash = com.split("|")[2]   
                fullHashUrl = hashurl + "/" + longHash
                changeLogCommitLine = commitLine + " ([" + shortHash + "](" + fullHashUrl + "))"
                if "fix" in com:
                    fixCommits.append(changeLogCommitLine)
                else:
                    featCommits.append(changeLogCommitLine)
        
        if len(fixCommits) > 0 and any(fixCommits):
            ch.write("\n\n### Bug Fixes\n\n")
            ch.write("* " + "\n* ".join(fixCommits))
        
        if len(featCommits) > 0 and any(featCommits):
            ch.write("\n\n### Features\n\n")
            ch.write("* " + "\n* ".join(featCommits))