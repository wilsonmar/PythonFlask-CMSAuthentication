# Module 1 - Authentication

## 1.1 - Models: Password Column
[tag]: # (@pytest.mark.test_models_password_column_module1)
Project Overview
-----
In this module we'll alter the SQLAlchemy `User` model to include a `password` column. Using `Flask-Migrate`, we will add the new column to the database and populate the required fields. We will create a login HTML form and validate the form data in a new login route. The currently logged in user will be stored in a Flask `session`. The session will be cleared when the user logs out.

First Task 
----- 
Open the file called `models.py` in the `cms/admin` folder. Find the `User` model, add a column of type `string` with a size of `100`. Make sure `nullable` is `False`. Name this column `password`.

## 1.2 - Models: Check Password
[tag]: # (@pytest.mark.test_models_check_password_module1)
Eventually we are going to need to verify the username and password of a user. There are a few functions that are part of `werkzeug.security` that can help us out. Import `check_password_hash` from `werkzeug.security` below the other imports.

The best place for a password check is in the `User` model itself. Add a function called `check_password` to the `User` model below the `password` column. Since `check_password` is part of a class pass two parameters, `self` and `value`.

In the body of `check_password` return a call to the `check_password_hash` function. Pass in the new class variable `password` *Hint: self.*, and the `value`.

## 1.3 - Database Migration
[tag]: # (@pytest.mark.test_database_migration_module1)
There is currently no database for the application. Let's create one and migrate the new scheme that includes our new `password` column. Open a terminal, command propmt, or powershell and `cd` to the root folder of the project.

The `Flask-Migrate` extension should be installed. This exenstion provides several `flask db` commands.
First, to initialize and configure our schema run the `flask db init` command.
Second, to create a migration run the `flask db migrate` command.
Third, to create the database and run the migration use `flask db upgrade`.
Finally, run this projects custom command `flask add-content` to add content to the database.

## 1.4 - Template: Login Form
[tag]: # (@pytest.mark.test_template_login_form_module1)


## 1.5 - Auth: Imports
[tag]: # (@pytest.mark.test_auth_imports_module1)


## 1.6 - Auth: Protected Decorator
[tag]: # (@pytest.mark.test_auth_protected_decorator_module1)


## 1.7 - Auth: Redirect User
[tag]: # (@pytest.mark.test_auth_redirect_user_module1)


## 1.8 - Auth: Load User
[tag]: # (@pytest.mark.test_auth_load_user_module1)


## 1.9 - Auth: Login Route
[tag]: # (@pytest.mark.test_auth_login_route_module1)


## 1.10 - Auth: Post Request
[tag]: # (@pytest.mark.test_auth_post_request_module1)


## 1.11 - Auth: Get User
[tag]: # (@pytest.mark.test_auth_get_user_module1)


## 1.12 - Auth: Validate Form Data
[tag]: # (@pytest.mark.test_auth_validate_form_data_module1)


## 1.13 - Auth: Store User in Session
[tag]: # (@pytest.mark.test_auth_store_user_in_session_module1)


## 1.14 - Auth: Logout Route
[tag]: # (@pytest.mark.test_auth_logout_route_module1)


## 1.15 - Admin: Protect Routes
[tag]: # (@pytest.mark.test_admin_protect_routes_module1)
