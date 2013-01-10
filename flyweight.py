#!/usr/bin/env python
import config
import os
import re
import shutil
import subprocess

class Git:
    def clone(self, source, target):
        self.call("git clone %s %s" % (source, target))

    def fetch(self, path):
        self.call("git fetch --tags")

    def checkout(self, path, revision):
        cwd = os.getcwd()
        os.chdir(path)
        self.call("git checkout %s" % revision)
        os.chdir(cwd)

    def getTags(self, path):
        cwd = os.getcwd()
        os.chdir(path)
        tags = self.parseTags(self.call("git tag")))
        os.chdir(cwd)
        return tags

    def call(self, command):
        return subprocess.check_output(command.split(" ")

    def parseTags(self, output):
        output.strip().split("\n")

class Flyweight:
    includes = [
        'md',
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

        self.workspace = os.path.join(os.getcwd(), 'workspace')
        self.source = os.path.join(self.workspace, 'source')
        self.output = os.path.join(self.workspace, 'output')

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
                print "Fetching %s from %s" % (repo['name'], repo['url'])
                self.git.fetch(repo['source'])
            # Otherwise do a fresh clone
            else:
                print "Cloning %s from %s" % (repo['name'], repo['url'])
                self.git.clone(repo['url'], repo['source'])
    
    def buildCDN(self):
        """
        The build CDN method enumerates each tag in the specified repos, creates
        new output folders, and copies all of the desired files from source to
        output
        """
        for repo in config.repos:
            for tag in self.git.getTags(repo['source']):
                if tag in self.listExistingTags(repo):
                    print "Skipping %s version %s because it already exists" %\
                        (repo['name'], tag)
                else:
                    self.git.checkout(repo['source'], tag)
                    output_dir = os.path.join(self.output, repo['name'], tag)
                    if not os.path.isdir(output_dir):
                        print "Adding %s version %s under %s" %\
                            (repo['name'], tag, output_dir)
                        self.recursiveCopy(repo['source'], output_dir)

    def updateCDN(self):
        pass

    def listExistingTags(self, repo):
        repo_path = os.path.join(self.output, repo['name'])
        if os.path.isdir(repo_path):
            return os.listdir(repo_path)
        else:
            return []

    def recursiveCopy(self, src, dst):
        names = os.listdir(src)
        os.makedirs(dst)

        for name in names:
            if os.path.basename(name)[0] == ".":
                continue
            
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)

            if os.path.isdir(srcname):
                self.recursiveCopy(srcname, dstname)
            elif extension in self.includes:
                shutil.copyfile(srcname, dstname)

    def getFileExtension(self, path):
        filename = os.path.splitext(path)[1]
        if filename:
            return filename.split(".")[1]
        return None

def main():
    flyweight = Flyweight()
    flyweight.updateRepos()
    flyweight.buildCDN()
    flyweight.updateCDN()

if __name__ == '__main__':
    main()