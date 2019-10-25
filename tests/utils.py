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

def rq(string):
    return re.sub(r'(\'|")', '', str(string))

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

def get_form_data(code, route, values, name):
    index = list(get_request_method(code, route).find_all('atomtrailers', lambda node: \
        node.parent.type == 'assignment' and \
        node.value[0].value == 'request' and \
        node.value[1].value == 'form' and \
        node.value[2].type == 'getitem').map(lambda node: rq(node.value[2].value)))

    get = list(get_request_method(code, route).find_all('atomtrailers', lambda node: \
        node.value[0].value == 'request' and \
        node.value[1].value == 'form' and \
        node.value[2].value == 'get' and \
        node.value[3].type == 'call').map(lambda node: rq(node.value[3].value[0].value)))

    diff = list(set(index + get) - values)
    diff_exists = len(diff) == 0
    message = 'You have extra `request.form` statements. You can remove those for these varaibles {}'.format(diff)
    assert diff_exists, message
    
    assignment = get_request_method(code, route).find('assign', lambda node: \
        str(node.target) == name)
    assignment_exists = assignment is not None
    assert assignment_exists, \
        'Do you have a variable named `{}`?'.format(name)
    
    name_as_string = '"{}"'.format(name.replace('content.', ''))
    sub_name = '[{}]'.format(name_as_string)
    
    right = assignment.find('atomtrailers', lambda node: \
        node.value[0].value == 'request' and \
        node.value[1].value == 'form' and \
        node.value[2].type == 'getitem' and \
        node.value[2].find('string', lambda node: str(node.value).replace("'", '"') == name_as_string)) is not None
    
    right_get = assignment.find('atomtrailers', lambda node: \
        node.value[0].value == 'request' and \
        node.value[1].value == 'form' and \
        node.value[2].value == 'get' and \
        node.value[3].type == 'call' and \
        node.value[3].find('string', lambda node: str(node.value).replace("'", '"') == name_as_string)) is not None
    
    assert right or right_get, \
        'Are you setting the `{}` varaible to the correct form data?'.format(name)
