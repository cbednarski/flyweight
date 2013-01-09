#!/usr/bin/env python
import os
import subprocess

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
        workspace = 
        if()

    def updateRepos(self):
        pass

    def updateCDN(self):
        pass

def main():
    flyweight = Flyweight()
    flyweight.updateRepos()

if __name__ == '__main__':
    main()