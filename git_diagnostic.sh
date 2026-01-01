#!/bin/bash
echo "=== GIT REMOTE ===" > /tmp/git_diag.txt
git remote -v >> /tmp/git_diag.txt 2>&1
echo "" >> /tmp/git_diag.txt
echo "=== GIT BRANCH ===" >> /tmp/git_diag.txt
git branch -a >> /tmp/git_diag.txt 2>&1
echo "" >> /tmp/git_diag.txt
echo "=== GIT LOG ===" >> /tmp/git_diag.txt
git log --oneline -n 5 >> /tmp/git_diag.txt 2>&1
echo "" >> /tmp/git_diag.txt
echo "=== GIT STATUS ===" >> /tmp/git_diag.txt
git status >> /tmp/git_diag.txt 2>&1
cat /tmp/git_diag.txt
