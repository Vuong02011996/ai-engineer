# Generate ssh key to access Gitlab
[1] [Generate ssh key](https://help.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
```
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
Enter
Enter
Enter
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
Add to Setting account -> SSH

# remote again to push with SSH.
git remote set-url origin git@github.com:Vuong02011996/tools_ubuntu.git
```
# Basic command
`clone project`: git clone ... 

`remove folder in gitlab`: 

+ git rm -r darknet_config_weight
+ git rm -r tracking_threading_backup.py

`check branch of project`: git branch

`show all branch` : 
+ git branch -a
+ git branch -r

`Push changed code`:
 + git add -A or git add *.py
 + git commit -m"command"
 + git push -u origin master

# Create new branch from master
+ git fetch --all
+ git checkout master
+ git pull
+ git checkout -b dev_v0.1(re nhanh moi)
+ git push origin dev_v0.1
# Merge change from master in dev branch
+ git checkout master
+ git pull
+ git checkout dev_v0.1(dev branch)
+ git rebase master

# Merge change from dev branch to master with many commit before
```buildoutcfg
From master branch
git rebase origin/dev_branch
git branch -> (no branchs, rebase from master)
```

**Using loop in process in follow**
+ Step 1: Keep going git rebase --continue

+ Step 2: fix CONFLICTS then git add .

+ Back to step 1, now if it says no changes .. then run git rebase --skip then go back to step 1

+ If you just want to quit rebase run git rebase --abort

+ Once all changes are done run git commit -m "rebase complete" and you are done.

# Error
+ git clone 

    Cloning into 'traffic_sign'...
    git@gitlab.com: Permission denied (publickey).
    fatal: Could not read from remote repository.
    
    eval "$(ssh-agent -s)"
    
    ssh-add ~/.ssh/id_rsa
+ git push 
`Error`: hint: Updates were rejected because the tip of your current branch is behind
Using git pull -> fix conflict -> git add -> git commit -> git push again.

+ Lỗi push file lớn hơn 100Mb
https://stackoverflow.com/questions/33330771/git-lfs-this-exceeds-githubs-file-size-limit-of-100-00-mb
