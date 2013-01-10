import unittest
import flyweight

class TestGit(unittest.TestCase):
    pass


class TestFlyweight(unittest.TestCase):
    def test_getFileExtension(self):
        fw = flyweight.Flyweight()
        self.assertEquals('md', fw.getFileExtension('readme.md'))
        self.assertEquals('png', fw.getFileExtension('my.picture.png'))
        self.assertEquals(None, fw.getFileExtension('.gitignore'))

if __name__ == '__main__':
    unittest.main()