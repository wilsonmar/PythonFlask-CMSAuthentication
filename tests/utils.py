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

def get_imports(code, value):
    imports = code.find_all('from_import',  lambda node: ''.join(list(node.value.node_list.map(lambda node: str(node)))) == value).find_all('name_as_name')
    return list(imports.map(lambda node: node.value))

def get_conditional(code, values, type, nested=False):
    def flat(node):
        if node.type == 'comparison':
            return '{}:{}:{}'.format(str(node.first).replace("'", '"'), str(node.value).replace(' ', ':'), str(node.second).replace("'", '"'))
        elif node.type == 'unitary_operator':
            return '{}:{}'.format(str(node.value), str(node.target).replace("'", '"'))

    nodes = code.value if nested else code
    for value in values:
        final_node = nodes.find_all(type).find(['comparison', 'unitary_operator'], lambda node: flat(node) == value)
        if final_node is not None:
            return final_node
    return None

def get_route(code, route):
    route_function = code.find('def', name=route)
    route_function_exists = route_function is not None
    assert route_function_exists, \
        'Does the `{}` route function exist in `cms/admin/__init__.py`?'.format(route)
    return route_function

def get_methods_keyword(code, route):
    methods_keyword = get_route(code, route).find_all('call_argument', lambda node: \
        str(node.target) == 'methods')
    methods_keyword_exists = methods_keyword is not None
    assert methods_keyword_exists, \
        'Does the `{}` route have a keyword argument of `methods`?'.format(name)
    return methods_keyword

def get_request_method(code, route, parent=True):
    request_method = get_route(code, route).find('comparison', lambda node: \
        'request.method' in [str(node.first), str(node.second)])
    request_method_exists = request_method is not None
    assert request_method_exists, \
        'Do you have an `if` statement in the `{}` route that checks `request.method`?'.format(route)
    return request_method.parent if parent else request_method
