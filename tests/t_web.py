from __future__ import annotations
from hollarek.web import SiteVisitor
from hollarek.devtools import Unittest

class VisitorTester(Unittest):
    @classmethod
    def setUpClass(cls):
        cls.visitor = SiteVisitor()
        cls.beavers_url = 'https://en.wikipedia.org/wiki/Beaver'
        cls.invalid_url = 'https://asldkfjskdjdkkkkkk'

    def test_static_beavers_ok(self):
        self.beaver_test(use_driver=False)

    def test_driver_beakers_ok(self):
        self.beaver_test(use_driver=True)

    def beaver_test(self, use_driver : bool):
        text = self.visitor.get_text(url=self.beavers_url, use_driver=use_driver)
        self.assertTrue(self.contains_beavers(text=text))

    @staticmethod
    def contains_beavers(text : str) -> bool:
        return 'beavers' in text.lower()

    def test_exists(self):
        beavers_exists = self.visitor.site_exists(url=self.beavers_url)
        invalid_doesnt_exist = self.visitor.site_exists(url=self.invalid_url)
        self.assertTrue(beavers_exists)
        self.assertFalse(invalid_doesnt_exist)


if __name__ == "__main__":
    VisitorTester.execute_all()