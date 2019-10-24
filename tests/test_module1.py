## Imports
import pytest
import re

from pathlib import Path
from redbaron import RedBaron

from tests.utils import simplify, get_imports
#!

## Paths
admin = Path.cwd() / 'cms' / 'admin'
admin_module = admin / '__init__.py'
models = admin / 'models.py'
auth = admin / 'auth.py'
#!

## Module Functions
def get_source_code(file_path):
    with open(file_path.resolve(), 'r') as source_code:
        return RedBaron(source_code.read())
#!

## Source Code
admin_module_code = get_source_code(admin_module)
models_code = get_source_code(models)
auth_code = get_source_code(auth)
#!

## Tests
@pytest.mark.test_models_password_column_module1
def test_models_password_column_module1():
    # 1. Models - Password Column
    # password = db.Column(db.String(100), nullable=False)
    password = models_code.find('assign', lambda node: \
        node.target.value == 'password' and \
        node.value[0].value == 'db' and \
        node.value[1].value == 'Column' and \
        node.value[2].type == 'call')
    password_exists = password is not None
    assert password_exists, \
        'Are you assigning `password` a call to the `db.Column()` function?'

    first_argument = password.find('atomtrailers', lambda node: \
        node.parent.type == 'call_argument' and \
        node.value[0].value == 'db' and \
        node.value[1].value == 'String' and \
        node.value[2].type == 'call' and \
        node.value[2].value[0].value.value == '100')

    second_argument = password.find('call_argument', lambda node: \
        str(node.target) == 'nullable' and \
        node.value.value == 'False'
    )
    arguments_exist = first_argument is not None and second_argument is not None
    assert arguments_exist, \
            'Are you passing the correct arguments to the `db.Column()` function?'


@pytest.mark.test_models_check_password_module1
def test_models_check_password_module1():
    # 2. Models - Check Password
    # from werkzeug.security import check_password_hash
    # def check_password(self, value):
    #     return check_password_hash(self.password, value)
    security_import = get_imports(models_code, 'werkzeug.security')
    security_import_exits = security_import is not None
    assert security_import_exits, \
        'Do you have a `werkzeug.security` import statement?'
    check_password_hash_exists = 'check_password_hash' in security_import
    assert check_password_hash_exists, \
        'Are you importing `check_password_hash` from `werkzeug.security` in `cms/admin/models.py`?'
    def_check_password = models_code.find('def', lambda node: \
        node.name == 'check_password' and \
        node.arguments[0].target.value == 'self' and \
        node.arguments[1].target.value == 'value' and \
        node.parent.type == 'class' and \
        node.parent.name == 'User'
    )
    
    def_check_password_exists = def_check_password is not None
    assert def_check_password_exists, \
        'Have you create a function in the `User` called `check_password`? Do you have the correct parameters set?'
        
    check_password_return = def_check_password.find('return', lambda node: \
        node.value[0].value == 'check_password_hash' and \
        node.value[1].type == 'call')
    check_password_return_exists = check_password_return is not None
    assert check_password_return_exists, \
        'Are you returning a call to the `check_password_hash()` function?'
    
    first_argument = def_check_password.find('atomtrailers', lambda node: \
        node.parent.type == 'call_argument' and \
        node.value[0].value == 'self' and \
        node.value[1].value == 'password')

    second_argument = def_check_password.find('name', lambda node: \
        node.parent.type == 'call_argument' and \
        node.value == 'value')

    arguments_exist = first_argument is not None and second_argument is not None
    assert arguments_exist, \
        'Are you passing the correct arguments to the `check_password_hash()` function?'

@pytest.mark.test_database_migration_module1
def test_database_migration_module1():
    # 3. Database Migration
    # > flask db init
    # > flask db migrate
    # > flask db upgrade
    assert False

"""
@pytest.mark.test_template_login_form_module1
def test_template_login_form_module1():
    # 4. Template - Login Form
    # <input type="text" class="input" name="username">
    # <input type="password" class="input" name="password">
    # <input type="submit" class="button is-link" value="Login">
    assert False

@pytest.mark.test_auth_protected_decorator_module1
def test_auth_protected_decorator_module1():
    # 5. Auth - Protected Decorator
    # from functools import wraps
    # def protected(route_function):
    #     @wraps(route_function)
    assert False

@pytest.mark.test_auth_wrapped_function_module1
def test_auth_wrapped_function_module1():
    # 6. Auth - Wrapped Function
    # def wrapped_route_function(**kwargs):
    #     return route_function(**kwargs)
    # return wrapped_route_function
    assert False

@pytest.mark.test_auth_redirect_user_module1
def test_auth_redirect_user_module1():
    # 7. Auth - Redirect User
    # if g.user is None:
    #     return redirect(url_for('admin.login'))
    assert False

@pytest.mark.test_auth_load_user_module1
def test_auth_load_user_module1():
    # 8. Auth - Load User
    # @admin_bp.before_app_request
    # def load_user():
    #     user_id = session.get('user_id')
    #     g.user = User.query.get(user_id) if user_id is not None else None
    assert False

@pytest.mark.test_auth_login_route_module1
def test_auth_login_route_module1():
    # 9. Auth - Login Route
    # @admin_bp.route('/login', methods=('GET', 'POST'))
    # def login():
    #     return render_template('admin/login.html')
    assert False

@pytest.mark.test_auth_post_request_module1
def test_auth_post_request_module1():
    # 10. Auth - Post Request
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     error = None
    assert False

@pytest.mark.test_auth_get_user_module1
def test_auth_get_user_module1():
    # 11. Auth - Get User
    # user = User.query.filter_by(username=username).first()
    assert False

@pytest.mark.test_auth_validate_form_data_module1
def test_auth_validate_form_data_module1():
    # 12. Auth - Validate Form Data
    # if user is None:
    #     error = 'Incorrect username.'
    # elif not user.check_password(password):
    #     error = 'Incorrect password.'
    assert False

@pytest.mark.test_auth_store_user_in_session_module1
def test_auth_store_user_in_session_module1():
    # 13. Auth - Store User in Session
    # if error is None:
    #     session.clear()
    #     session['user_id'] = user.id
    #     return redirect(url_for('admin.content', type='page'))
    # flash(error)
    assert False

@pytest.mark.test_auth_logout_route_module1
def test_auth_logout_route_module1():
    # 14. Auth - Logout Route
    # @admin_bp.route('/logout')
    # def logout():
    #     session.clear()
    #     return redirect(url_for('admin.login'))
    assert False

@pytest.mark.test_admin_protect_routes_module1
def test_admin_protect_routes_module1():
    # 15. Admin - Protect Routes
    # Protect all routes with the custom decorator.
    # @auth.protected
    assert False
#!
"""
