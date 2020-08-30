---
layout: blog-post
title: "Ensuring git commit messages contain JIRA ID"
excerpt: "Ensuring git commit messages contain JIRA ID"
disqus_id: /2020/01/12/git-prepare-commit-message-jira-id/
slug: git-prepare-commit-message-jira-id
tags:
- Git
---


Recently, we implemented a policy where every commit message includes the JIRA ID from the committer. This makes sure that every change to repo is tagged against either a user story or an issue which helps in traceability. Initially, it was difficult and users used to forget it. We had a github hook which would validate the commit message and reject the updates to the remote repo. Users would then amend the commit using
`git commit --amend` or even `git rebase -i HEAD~n` if there are multiple commits to be amended.

Fortunately, there is a provision in git itself which can validate your commit message in the local repo itself. All you to have to do is make a copy of  `.git/prepare-commit-msg.sample` to `.git/prepare-commit-msg` and then include your logic there. We used a convention that users create branch name with JIRA ID itself and this script can pickup the JIRA ID from the branch name itself. In the worst case, while working with branches such as `staging`, `master`, `release` etc, the users can provide the JIRA ID in the commit message. If there is no JIRA ID provided, the commit will be aborted with an error.

Below is the snippet I used, written in ruby

```ruby
#!/usr/bin/env ruby

# Git Prepare Commit Message Hook Script
#
# Location: <repository>/.git/hooks/prepare-commit-msg
#
# This script will automatically add the correct
# JIRA ISSUE ID to the end of each commit message
# When the branch ID starts with the JIRA ISSUE ID.
# It can be overridden if specified in the message.
#
# Example:
#
# jira-123/branch-name => 'JIRA-123 commit message'
#

# The name of the commit file is the first argument
message_filename = ARGV[0]
#puts filename: message_filename

# Read the contents of the commit file
message = File.read(message_filename)
#puts message: message

# Match a JIRA ID in the commit message that
jira_pattern = /^([A-Z]{1,32}-[0-9]{1,32})\s/

# Capture the JIRA ID if one is present in the commit message
jira_id = message[jira_pattern, 1]
#puts jira_id: jira_id

# Do nothing if the commit message has a JIRA ID
if jira_id.nil?
  # Otherwise we need to add one to the message

  # Grab the current git branch
  current_branch_name = `git rev-parse --abbrev-ref HEAD`

  exit if current_branch_name[/^(master|develop|release|hotfix)/]

  # Match the JIRA ID at the beginning of the branch name
  jira_branch_pattern = /^([a-zA-Z]{1,32}-[0-9]{1,32})[-_\/]?/

  # Capture the JIRA ID from the branch name
  jira_branch_id = current_branch_name[jira_branch_pattern, 1]
  #puts jira_branch_id: jira_branch_id

  if jira_branch_id.nil? || jira_branch_id.empty?
    # Blow up and let the user know they're missing a JIRA ID
    raise "Commit message missing JIRA ID and/or branch name does not have one"
  else
    # Append a link to the JIRA issue and the JIRA ID to the message
    jira_url = "https://jira.walmart.com/browse/#{jira_branch_id}"
    new_message = "#{jira_branch_id.upcase} - #{message}\n#{jira_url}\n"
    #puts new_message: message

    # Write the updated message back to the commit file
    File.open(message_filename, 'w') { |f| f.write(new_message) }
  end
end
```