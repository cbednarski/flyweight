import unittest
import flyweight

class TestRepository(unittest.TestCase):
    def test_createFromDict(self):
        url = "git@github.com:cbednarski/flyweight.git"
        name = "flyweight-project"
        command = "ls ."
        root = "/"
        expires = 1234

        rdict = {
            "url":url,
            "name":name,
            "before_build":command,
            "resource_root":root,
            "expires":expires
        }

        repo = flyweight.Repository(**rdict)

        self.assertEquals(url, repo.url)
        self.assertEquals(name, repo.name)
        self.assertEquals(command, repo.before_build)
        self.assertEquals(root, repo.resource_root)
        self.assertEquals(expires, repo.expires)

    def test_defaults(self):
        url = "git@github.com:cbednarski/flyweight.git"

        rdict = { "url":url }
        repo = flyweight.Repository(**rdict)

        self.assertEquals("flyweight", repo.name)


    def test_parseTags(self):
        output = """
        1.0.23
        1.0.24
        1.1.0
        pie1.1.0
        1.1.0sdfds
        waka
        """
        expected = ["1.0.23","1.0.24","1.1.0"]

        self.assertEquals(expected, flyweight.Repository.parseTags(output))

    def test_getNameFromUrl(self):
        # Not sure if these are all even valid git URLs but seems like they could be.
        self.assertEquals("my-repo", flyweight.Repository.getNameFromUrl("git@github.com:cbednarski/My Repo.git"))
        self.assertEquals("my-repo", flyweight.Repository.getNameFromUrl("git://github.com/cbednarski/my_repo.git"))
        self.assertEquals("my-repo", flyweight.Repository.getNameFromUrl("https://github.com/cbednarski/My-Repo.git"))
        self.assertEquals("my-repo", flyweight.Repository.getNameFromUrl("/home/user/code/my-repo.git"))
        self.assertEquals("my-repo", flyweight.Repository.getNameFromUrl("C:\code\My Repo.git"))


class TestFlyweight(unittest.TestCase):
    def test_getFileExtension(self):
        fw = flyweight.Flyweight()
        self.assertEquals('md', fw.getFileExtension('readme.md'))
        self.assertEquals('png', fw.getFileExtension('my.picture.png'))
        self.assertEquals(None, fw.getFileExtension('.gitignore'))

if __name__ == '__main__':
    unittest.main()