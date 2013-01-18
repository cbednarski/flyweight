#!/usr/bin/env python
import argparse, config, os, re, shutil, subprocess


def call(command):
    return subprocess.check_output(command.split(" "))

class Repository:
    """
    """
    before_build = None
    expires = 2592000
    name = None
    resource_root = "/"
    source = None
    url = None

    def __init__(self, **entries): 
        self.__dict__.update(entries)
        if self.name is None:
            self.name = Repository.getNameFromUrl(self.url)

    def clone(self, target):
        call("git clone %s %s" % (self.url, target))

    def fetch(self):
        cwd = os.getcwd()
        os.chdir(self.source)
        call("git fetch --tags")
        os.chdir(cwd)

    def checkout(self, revision):
        cwd = os.getcwd()
        os.chdir(self.source)
        call("git clean --force")
        call("git checkout %s" % revision)
        os.chdir(cwd)

    def execBeforeBuild(self):
        cwd = os.getcwd()
        os.chdir(self.source)
        call("before_build")
        os.chdir(cwd)

    def getTags(self):
        cwd = os.getcwd()
        os.chdir(self.source)
        tags = self.parseTags(call("git tag"))
        os.chdir(cwd)
        return tags

    @staticmethod
    def getNameFromUrl(url):
        return re.search('[/\\\\]([^/\\\\]+)\.git', url).group(1).lower().replace(" ", "-").replace("_", "-")

    @staticmethod
    def parseTags(output):
        tags = []
        for tag in output.strip().split("\n"):
            tag = tag.strip()
            if re.match('^\d+\.\d+\.\d+$', tag):
                tags.append(tag)
        return tags

class Flyweight:
    includes = [
        'css', 'js', 'json',
        'png', 'gif', 'jpg', 'jpeg', 'svg', 'ico'
        'ttf', 'eot', 'woff', 'otf',
        'swf', 'flv'
    ]

    source = None
    output = None
    repos = []
    bucket_name = None
    expires = 2592000

    def __init__(self):
        self.parseConfig(config)

        self.workspace = os.path.join(os.getcwd(), 'workspace')
        self.source = os.path.join(self.workspace, 'source')
        self.output = os.path.join(self.workspace, 'output')

        if not os.path.isdir(self.source):
            os.makedirs(self.source)

        if not os.path.isdir(self.output):
            os.makedirs(self.output)

        for repo in self.repos:
            repo.source = os.path.join(self.source, repo.name)
            repo.name = repo.name.lower()

    def fetchRepos(self):
        """
        The fetch method clones all of the repos in config.repos that we don't
        have and fetches updates to the ones we have.
        """
        for repo in self.repos:
            # Fetch if it exists
            if os.path.isdir(repo.source):
                print "Fetching %s from %s" % (repo.name, repo.url)
                repo.fetch()
            # Otherwise do a fresh clone
            else:
                print "Cloning %s from %s" % (repo.name, repo.url)
                repo.clone(repo.source)
    
    def buildCDN(self):
        """
        The build CDN method enumerates each tag in the specified repos, creates
        new output folders, and copies all of the desired files from source to
        output
        """
        for repo in self.repos:
            for tag in repo.getTags():
                if tag in self.listExistingTags(repo) and not self.args.force:
                    print "Skipping %s version %s because it already exists" %\
                        (repo.name, tag)
                else:
                    print "Building %s version %s" % (repo.name, tag)
                    repo.checkout(tag)
                    if repo.before_build is not None:
                        print "Executing before_build hook for %s version %s -- command is: %s" %\
                            (repo.name, tag, repo.before_build)
                        repo.execBeforeBuild()
                    output_dir = os.path.join(self.output, repo.name, tag)
                    if not os.path.isdir(output_dir) or self.args.force:
                        print "Adding %s version %s under %s" %\
                            (repo.name, tag, output_dir)
                        self.recursiveCopy(repo.source, output_dir)

    def pushCDN(self):
        """
        The update CDN method calls s3cmd to upload files to S3
        """
        # Note: The source path should have a trailing slash or the right-most
        # directory name will appear in the CDN path
        output_dir = os.path.realpath("workspace/output")+'/'

        call("s3cmd sync -r --acl-public \
            --add-header=Cache-Control:public \
            --add-header=Expires:A%s \
            %s s3://%s/" % \
            (config.expires, output_dir, config.bucket))

    def listExistingTags(self, repo):
        repo_path = os.path.join(self.output, repo.name)
        if os.path.isdir(repo_path):
            return os.listdir(repo_path)
        else:
            return []

    def recursiveCopy(self, src, dst):
        names = os.listdir(src)
        os.makedirs(dst)

        for name in names:
            # Skip hidden files
            if os.path.basename(name)[0] == ".":
                continue
            
            extension = self.getFileExtension(name)
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)

            if os.path.isdir(srcname):
                self.recursiveCopy(srcname, dstname)
            elif extension in self.includes:
                if extension in ['js','json','css'] and len(config.yui) > 0:
                    print "Compressing %s" % dstname
                    call("java -jar %s %s -o %s" % (config.yui, srcname, dstname))
                else:
                    shutil.copyfile(srcname, dstname)

    def getFileExtension(self, path):
        filename = os.path.splitext(path)[1]
        if filename:
            return filename.split(".")[1]
        return None

    def parseConfig(self, config):
        self.bucket_name = config.bucket
        self.expires = config.expires

        for repo in config.repos:
            r = Repository(**repo)
            self.repos.append(r)

    def cli(self):
        parser = argparse.ArgumentParser()

        # Main commands
        parser.add_argument("action", choices=["build", "push", "update"], help="Build the CDN assets locally, push local assets to the CDN, or both (update).")

        # Options
        parser.add_argument("-f", "--force", action="store_true", help="Rebuild all library versions, " \
            "including those that have already been built / uploaded")
        parser.add_argument("-v", "--verbose", action="store_true", help="Spew to console")

        self.args = parser.parse_args()
        action = self.args.action

        # Execute the cli app
        if action == "build" or action == "update":
            flyweight.fetchRepos()
            flyweight.buildCDN()
        if action == "push" or action == "update":
            flyweight.pushCDN()

if __name__ == '__main__':
    flyweight = Flyweight()
    flyweight.cli()