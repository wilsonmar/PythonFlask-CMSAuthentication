from cms.admin import admin_bp
from cms.admin.models import User
from flask import render_template, request, redirect, url_for, flash

# TASK(05)
from functools import wraps
from flask import g, session

def protected(route_function): # TASK(06)
    @wraps(route_function) # TASK(07)
    def wrapped_route_function(**kwargs): # TASK(06)
        # TASK(07)
        if g.user is None:
            return redirect(url_for('admin.login'))
        #/
        return route_function(**kwargs) # TASK(06)
    return wrapped_route_function # TASK(07)

# TASK(08)
@admin_bp.before_app_request
def load_user():
    user_id = session.get('user_id')
    g.user = User.query.get(user_id) if user_id is not None else None

# TASK(09)
@admin_bp.route('/login', methods=('GET', 'POST'))
def login():
    # TASK(10)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        # TASK(11)
        user = User.query.filter_by(username=username).first()

        # TASK(12)
        if user is None:
            error = 'Incorrect username.'
        elif not user.check_password(password):
            error = 'Incorrect password.'

        # TASK(13)
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('admin.content', type='page'))

        flash(error)
    # TASK(09)
    return render_template('admin/login.html')

# TASK(14)
@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))
