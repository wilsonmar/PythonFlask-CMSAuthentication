import re
from bs4 import BeautifulSoup
from jinja2 import Environment, PackageLoader, exceptions, meta, nodes

env = Environment(loader=PackageLoader('cms', '/admin/templates/admin'))

def template_source(name):
    try:
        return env.loader.get_source(env, name + '.html')[0]
    except exceptions.TemplateNotFound:
        return None

def parsed_content(name):
    return env.parse(template_source(name))

def template_data(name):
    html = ''
    for node in parsed_content(name).find_all(nodes.TemplateData):
        html += node.data
    return BeautifulSoup(html, 'html.parser')

def simplify(main):
    def _simplify(node):
        if not isinstance(node, nodes.Node):
            if isinstance(node, (type(None), bool)):
                buf.append(repr(node))
            else:
                buf.append(node)
            return

        for idx, field in enumerate(node.fields):
            value = getattr(node, field)
            if value == 'load' or value == 'store':
                return
            if idx:
                buf.append('.')
            if isinstance(value, list):
                for idx, item in enumerate(value):
                    if idx:
                        buf.append('.')
                    _simplify(item)
            else:
                _simplify(value)

    buf = []
    _simplify(main)
    return ''.join(buf)
