from __future__ import annotations
from holytools.web import SiteVisitor
from holytools.devtools import Unittest
import psutil

class VisitorTester(Unittest):
    @classmethod
    def setUpClass(cls):
        cls.visitor = SiteVisitor(headless=True)
        cls.beavers_url = 'https://en.wikipedia.org/wiki/Beaver'
        cls.invalid_url = 'https://asldkfjskdjdkkkkkk'
        cls.openai_docs = 'https://platform.openai.com/docs/introduction'
        cls.models_docs = 'https://platform.openai.com/docs/models'

    def test_driver(self):
        self.beaver_test()

    def test_link(self):
        link_text = self.visitor.get_text(url=self.beavers_url, with_links=True)
        self.assertIn('http', link_text)

    def test_exists(self):
        beavers_exists = self.visitor.site_exists(url=self.beavers_url)
        invalid_doesnt_exist = self.visitor.site_exists(url=self.invalid_url)
        model_docs_exist = self.visitor.site_exists(url=self.models_docs)
        self.assertTrue(beavers_exists)
        self.assertFalse(invalid_doesnt_exist)
        self.assertTrue(model_docs_exist)


    def test_crawl_js_required(self):
        if not self.is_manual_mode:
            self.skipTest(reason=f'Testing javascript requires not headless')

        visitor = SiteVisitor(headless=False)
        text_content = visitor.get_text(url=self.openai_docs)
        print(f'openai text content : {text_content}')
        self.assertTrue(len(text_content) > 200)

    def test_z_cleanup(self):
        self.visitor.quit()

        current_process = psutil.Process()
        children = current_process.children(recursive=True)
        for child in children:
            print(f'Child pid is {child.pid}')
            print(f'Child exe is {child.exe()}')
            child_exe_name = str(child.exe()).lower()
            self.assertFalse(f'chrome' in child_exe_name)
            self.assertFalse(f'google' in child_exe_name)

    # -------------------------------------------

    def beaver_test(self):
        text = self.visitor.get_text(url=self.beavers_url)
        self.assertTrue(self.contains_beavers(text=text))
        self.log(f'Beaver text: {text[:500]}')

    @staticmethod
    def contains_beavers(text: str) -> bool:
        return 'beavers' in text.lower()


if __name__ == "__main__":
    VisitorTester.execute_all()