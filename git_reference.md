## Important Git commands:

### git clone [url]:
- **Function**: This command downloads a complete copy of an existing Git repository from a remote location (usually a URL like GitHub) to your local machine.
- **Use case**: Work with a copy of the project on your local machine and make changes without affecting the original.
- **Example**: git clone https://github.com/username/project-name.git (This downloads the "project-name" repository from the user "username" on GitHub)

### git status:
- **Function**: This command displays the current state of your Git repository.
  <br>It shows you which files are:
  <br>&#160;&#160;&#160;&#160;Modified: Changed since the last commit but not yet added to the staging area.
  <br>&#160;&#160;&#160;&#160;Staged: Added to the staging area, ready to be included in the next commit.
  <br>&#160;&#160;&#160;&#160;Untracked: New files that haven't been added to Git yet.
- **Use case**: Keep track of changes and ensure you're ready to commit the right files.

### git add [file]:
- **Function**: This command adds a specific file (or multiple files) to the staging area. This tells Git that you want to include these changes in the next commit.
- **Use case**: Selectively include specific changes in a commit, rather than committing everything at once.
- **Example**: git add main.py (This adds the file "main.py" to the staging area)

### git commit -m "[commit message]":
- **Function**: This command creates a snapshot of the currently staged changes (files added with git add) and stores it permanently in the Git repository history. The -m flag allows you to provide a brief message describing the changes you made.
- **Use case**: Maintain a record of the project's history and allows you to revert to previous versions if needed. Descriptive commit messages make it easier to understand the project's evolution.
- **Example**: git commit -m "Fixed a bug in the main function" (This creates a commit with the message "Fixed a bug in the main function")

### git push [remote] [branch]:
- **Function**: This command uploads your local commits to a remote repository. You specify the remote repository name (e.g., "origin") and the branch you want to push your commits to.
- **Use case**: Share your changes with collaborators by pushing them to a central repository.
- **Example**: git push origin main (This pushes your local commits on the "main" branch to the remote repository named "origin")

### git pull [remote]:
- **Function**: This command retrieves changes from a remote repository and merges them into your local working directory. You can optionally specify a remote repository name.
- **Use case**: Stay up-to-date with the latest changes made by other collaborators. It is recommended to always pull before making any changes to the local Git repository. 
- **Example**: git pull origin (This pulls changes from the remote repository named "origin" and attempts to merge them into your current branch)

### git branch:
- **Function**: This command provides various options for managing branches in your Git repository.
<br>&#160;&#160;&#160;&#160;git branch (without arguments) lists all branches in your local repository.
<br>&#160;&#160;&#160;&#160;git branch <branch-name> creates a new branch.
<br>&#160;&#160;&#160;&#160;git checkout <branch-name> switches your working directory to a different branch.
<br>&#160;&#160;&#160;&#160;git branch -d <branch-name> deletes a branch (use with caution!).
- **Use case**: Isolate your work on new features or bug fixes without affecting the main codebase.

### git checkout [branch-name]:
- **Function**: This command has two main uses:
<br>&#160;&#160;&#160;&#160;Switching branches: Switch your working directory to a different branch. This changes the files and folders you see and allows you to work on that specific branch.
<br>&#160;&#160;&#160;&#160;Restoring working tree files: If a file has been modified but not staged (marked for inclusion in the next commit), git checkout can revert those changes and restore the file to its state in the specified branch.
- **Use case**: Switch between different development lines or revert accidental changes.

### git merge [branch]:
- **Function**: This command combines the changes from one branch into your current branch.
- **Use case**: Integrate changes from different development lines into a single branch. However, merging can sometimes lead to conflicts if the same lines of code were modified in both branches.
