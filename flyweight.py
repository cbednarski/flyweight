#!/usr/bin/env python
import config
import os
import re
import subprocess

class Git:
    def clone(self, source, target):
        command = "git clone %s %s" % (source, target)
        subprocess.call(command.split(" "))

    def fetch(self, path):
        command = "git fetch --tags"
        subprocess.call(command.split(" "))

    def checkout(self, path, revision):
        cwd = os.getcwd()
        os.chdir(path)
        command = "git checkout --tags"
        subprocess.call(command.split(" "))
        os.chdir(cwd)

    def getTags(self, path):
        cwd = os.getcwd()
        os.chdir(path)
        command = "git tag"
        subprocess.call(command.split(" "))
        os.chdir(cwd)

class Flyweight:
    includes = [
        'css', 'js', 'json',
        'png', 'gif', 'jpg', 'jpeg', 'svg',
        'ttf', 'eot', 'woff', 'otf',
        'swf', 'flv'
    ]

    source = None
    output = None
    git = None

    def __init__(self):
        self.git = Git()

        workspace = os.path.join(os.getcwd(), 'workspace')
        self.source = os.path.join(workspace, 'source')
        self.output = os.path.join(workspace, 'output')

        if not os.path.isdir(self.source):
            os.makedirs(self.source)

        if not os.path.isdir(self.output):
            os.makedirs(self.output)

        for repo in config.repos:
            repo['name'] = re.search('/([^/]+)\.git', repo['url']).group(1)
            repo['source'] = os.path.join(self.source, repo['name'])

    def updateRepos(self):
        """
        The update method clones all of the repos in config.repos that we don't
        have and updates the ones we do.
        """
        for repo in config.repos:
            # Update if it exists
            if os.path.isdir(repo['source']):
                self.git.fetch(repo['source'])
            # Otherwise do a fresh clone
            else:
                self.git.clone(repo['url'], repo['source'])
    
    def buildCDN(self):
        """
        The build CDN method enumerates each tag in the specified repos, creates
        new output folders, and copies all of the desired files from source to
        output
        """
        for repo in config.repos:
            print self.git.getTags(repo['source'])

    def updateCDN(self):
        pass

def main():
    flyweight = Flyweight()
    flyweight.updateRepos()
    flyweight.buildCDN()
    flyweight.updateCDN()

if __name__ == '__main__':
    main()