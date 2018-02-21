import re

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
    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.extras = {}

    def json(self):
        base = {
            'title': self.title,
            'text': self.text,
        }
        base.update(self.extras)

        return base

    def remove_wikicode(self):
        tmp1 = re.sub(r'\(?\{\{.+?\}\}\)?', '', self.text)
        tmp2 = re.sub(r'\[\[(File|Image)(.+?)\]\]', '', tmp1)
        tmp3 = re.sub(r'\[\[(.*?)\|?([^\|\[\]]+)\]\]', '\\2', tmp2)
        tmp4 = re.sub(r'={2,}(.+?)={2,}', '\\1', tmp3)
        tmp5 = re.sub(r'\'{2,}', '', tmp4)
        tmp6 = re.sub(r'\[\S+ (.+)\]', '\\1', tmp5)

        self.text = tmp6

    def get_extra(self, key):
        return self.extras.get(key, None)

    def set_extra(self, key, value):
        self.extras[key] = value
