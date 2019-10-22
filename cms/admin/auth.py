# TASK(05): Create `auth.py`

# TASK(05)
from cms.admin import admin_bp
from cms.admin.models import User

# TASK(06)
from functools import wraps
from flask import render_template, request, redirect, url_for, flash, g, session

# TASK(07)
def protected(route_function):
    @wraps(route_function)
    # TASK(08)
    def wrapped_route_function(**kwargs):
        # TASK(09)
        if g.user is None:
            return redirect(url_for('admin.login'))
        return route_function(**kwargs)
    return wrapped_route_function

# TASK(10)
@admin_bp.before_app_request
def load_user():
    user_id = session.get('user_id')
    g.user = User.query.get(user_id) if user_id is not None else None

# TASK(11)
@admin_bp.route('/login', methods=('GET', 'POST'))
def login():
    # TASK(12)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        # TASK(13)
        user = User.query.filter_by(username=username).first()

        # TASK(14)
        if user is None:
            error = 'Incorrect username.'
        elif not user.check_password(password):
            error = 'Incorrect password.'

        # TASK(15)
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('admin.content', type='page'))

        flash(error)
    # TASK(11)
    return render_template('admin/login.html')

# TASK(16)
@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))
