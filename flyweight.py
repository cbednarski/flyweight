#!/usr/bin/env python
import os
import subprocess
import config

class Git:
    def clone(self, source, target):
        pass

    def fetch(self, path):
        pass

    def checkout(self, revision):
        pass

    def getTags(self, path):
        pass

class Flyweight:
    includes = [
        'css', 'js', 'json',
        'png', 'gif', 'jpg', 'jpeg', 'svg',
        'ttf', 'eot', 'woff', 'otf',
        'swf', 'flv'
    ]

    def resetWorkspace(self):
        workspace = os.path.join(os.getcwd(), 'workspace')
        source = os.path.join(workspace, 'source')
        output = os.path.join(workspace, 'output')

        if not os.path.isdir(source):
            os.makedirs(source)

        if not os.path.isdir(output):
            os.makedirs(output)

    def updateRepos(self):
        self.resetWorkspace()
        pass

    def updateCDN(self):
        pass

def main():
    flyweight = Flyweight()
    flyweight.updateRepos()

if __name__ == '__main__':
    main()