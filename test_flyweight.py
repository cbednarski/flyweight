import unittest
import flyweight

class TestGit(unittest.TestCase):
    def test_parseTags(self):
        git = flyweight.Git()

        output = """
        1.0.23
        1.0.24
        1.1.0
        pie1.1.0
        1.1.0sdfds
        picture
        master
        waka
        """
        expected = ["1.0.23","1.0.24","1.1.0"]

        self.assertEquals(expected, git.parseTags(output))

    def test_getNameFromUrl(self):
        git = flyweight.Git()
        # Not sure if these are all even valid git URLs but seems like they could be.
        self.assertEquals("my-repo", git.getNameFromUrl("git@github.com:cbednarski/My Repo.git"))
        self.assertEquals("my-repo", git.getNameFromUrl("git://github.com/cbednarski/my_repo.git"))
        self.assertEquals("my-repo", git.getNameFromUrl("https://github.com/cbednarski/My-Repo.git"))
        self.assertEquals("my-repo", git.getNameFromUrl("/home/user/code/my-repo.git"))
        self.assertEquals("my-repo", git.getNameFromUrl("C:\code\My Repo.git"))


class TestFlyweight(unittest.TestCase):
    def test_getFileExtension(self):
        fw = flyweight.Flyweight()
        self.assertEquals('md', fw.getFileExtension('readme.md'))
        self.assertEquals('png', fw.getFileExtension('my.picture.png'))
        self.assertEquals(None, fw.getFileExtension('.gitignore'))

if __name__ == '__main__':
    unittest.main()