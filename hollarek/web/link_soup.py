from __future__ import annotations

from bs4 import BeautifulSoup, NavigableString, CData, Tag


class LinkSoup(BeautifulSoup):
    def _all_strings(self, types=(NavigableString, CData)):
        for descendant in self.descendants:

            if isinstance(descendant, Tag) and descendant.name == 'a':
                link_text = descendant.text.strip()
                link_text = link_text.replace('\n', ' ')
                yield str(f"<({link_text})[{descendant.get('href')}]> ")
            if isinstance(descendant, NavigableString) and descendant.parent.name == 'a':
                continue
            if types is None and not isinstance(descendant, NavigableString):
                continue
            if types and type(descendant) in types:
                continue

            yield descendant
