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


class TestFlyweight(unittest.TestCase):
    def test_getFileExtension(self):
        fw = flyweight.Flyweight()
        self.assertEquals('md', fw.getFileExtension('readme.md'))
        self.assertEquals('png', fw.getFileExtension('my.picture.png'))
        self.assertEquals(None, fw.getFileExtension('.gitignore'))

if __name__ == '__main__':
    unittest.main()