import functools
import re

def _create_sub_applier(regex, sub, flags):
    return functools.partial(re.sub, pattern=regex, repl=sub, flags=flags)

class WVPageFactoryBase:
    def create(self):
        pass

class WVPageXMLFactory(WVPageFactoryBase):
    def __init__(self, namespace):
        self.namespace = namespace

    def create(self, node):
        title = node.find(self._namespaced_tag('title')).text
        raw_text = node.find(self._namespaced_tag('revision')) \
                       .find(self._namespaced_tag('text')).text
        if raw_text is None:
            raw_text = ''
        text = raw_text

        return WVPage(title, text)

    def _namespaced_tag(self, tag):
        return self.namespace + tag


class WVPage:
    TEMPLATES = r'\(?\{\{.+?\}\}\)?'
    FILE_BRACKETS = r'\[\[(File|Image)(.+?)\]\]'
    NESTED_BRACKETS = r'\[\[[^\[\]]+\[\[.+?\]\].+?\]\]'
    WIKI_PAGE_BRACKETS = r'\[\[(.*?)\|?([^\|\[\]]+)\]\]'
    HEADERS = r'={2,}(.+?)={2,}'
    ITALIC_INDENTS = r'^:\'\'.+?\'\''
    MULTI_SEQUENCE_QUOTES = r'\'{2,}'
    EXTERNAL_LINKS_WITH_TEXT = r'\[\S+ (.+)\]'

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.extras = {}

        flags = re.DOTALL | re.M
        self._clean_ups = [
            _create_sub_applier(WVPage.TEMPLATES, '', flags),
            _create_sub_applier(WVPage.NESTED_BRACKETS, '', flags),
            _create_sub_applier(WVPage.FILE_BRACKETS, '', flags),
            _create_sub_applier(WVPage.WIKI_PAGE_BRACKETS, '\\2', flags)
            _create_sub_applier(WVPage.HEADERS, '\\1', flags)
            _create_sub_applier(WVPage.EXTERNAL_LINKS_WITH_TEXT, '\\1', flags)
            _create_sub_applier(WVPage.ITALIC_INDENTS, '', flags),
            _create_sub_applier(WVPage.MULTI_SEQUENCE_QUOTES, '', flags)
        ]

    def json(self):
        base = {
            'title': self.title,
            'text': self.text,
        }
        base.update(self.extras)

        return base

    def remove_wikicode(self):
        cur = self.text
        for clean_up in self._clean_ups:
            cur = clean_up(cur)

        self.text = cur

    def get_extra(self, key):
        return self.extras.get(key, None)

    def set_extra(self, key, value):
        self.extras[key] = value
