import secrets
import json

from app import app
from app.modules.auth.model import User, SignupForm, LoginForm, \
    user_datastore

from flask import Blueprint, render_template, flash, request, redirect, \
    url_for, jsonify
from flask_security import login_user, logout_user, login_required, \
    current_user
from flask_security.utils import hash_password, verify_password


auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Signs the Current User In """

    if request.method == 'GET':
        return render_template('auth/signup.html', form=SignupForm())

    form = SignupForm(request.form)

    if not form.validate():
        flash('error Invalid Email or Password')
        return redirect(url_for('auth.signup'))

    name = form.name.data
    email = form.email.data
    password = form.password.data

    try:
        # validate that the user does not already exist
        if User.objects(email__exact=email).count() != 0:
            flash('error An Account Is Already Using That Email.')
            return redirect(url_for('auth.login'))

        # generate activation token
        activation_token = secrets.token_urlsafe(32)
        print("Activation token generated")

        # add user to the database
        user_datastore.create_user(
            email=email,
            name=name,
            password=hash_password(password),
            activation_hash=hash_password(activation_token),
            active=True
        )

        flash('User Created')
        return redirect(url_for('auth.login'))
    except Exception as e:
        print(str(e))
        flash('error An Error has Occured, Please Try Again!')
        return redirect(url_for('auth.signup'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """ Creates a session for the current user """

    if request.method == 'GET':
        return render_template('auth/login.html', form=LoginForm())

    # if not request.form:
    #     data = request.get_json()
    #     email = data['email']
    #     password = data['password']
    # else:
    form = LoginForm(request.form)
    if not form.validate():
        flash('error Invalid Email or Password.')
        return redirect(url_for('auth.login'))
    email = form.email.data
    password = form.password.data

    user = user_datastore.find_user(email=email)
    print(str(user.email))

    # user does not exist
    if user is None:
        flash('error Please Make Sure You Have Created an Account.')
        return redirect(url_for('auth.signup'))

    # user provided invalid password
    if not verify_password(password, user.password):
        flash('error Invalid Email or Password.')
        return redirect(url_for('auth.login'))

    # user has not authenticated their account
    if not user.is_authenticated():
        flash('error Please Authenticate Your Account.')
        return redirect(url_for('auth.login'))

    login_user(user)

    flash('success Logged in Successfully, {}'.format(user.name))
    return redirect(request.args.get('next') or url_for('classes.home'))


@auth.route('/profile/<user_id>', methods=['GET'])
@login_required
def view_profile(user_id):
    """ Get information and statistics to view user's profile """
    return render_template('auth/profile.html')


@auth.route('/invite/<email>', methods=['GET'])
@login_required
def invite_user(email):
    try:
        user = current_user._get_current_object()

        mail = SendGrid(app)

        mail.send_email(
            from_email=app.config['SENDGRID_DEFAULT_FROM'],
            to_email=email,
            subject='Come Join myplanner',
            html=invite_html(user.email, email)
        )

        flash('success Invitation Sent.')
    except Exception as e:
        flash('error Could not Create Invitation. {}'.format(e))

    return redirect(request.args.get('next') or url_for('classes.home'))


@auth.route('/getUser')
@login_required
def get_user():
    usr = current_user._get_current_object()
    return json.dumps({'name': usr.name, 'email': usr.email, 'id': str(usr.id)})


@auth.route('/logout')
@login_required
def logout():
    """ Deletes the session for the current user """

    logout_user()
    flash('success Successfully Logged Out')
    return redirect(url_for('auth.login'))


@auth.route('/delete', methods=['POST'])
def delete_user():
    form = LoginForm(request.form)
    if not form.validate():
        flash('error Could Not Delete User')
        return redirect(url_for('auth.login'))

    email = form.email.data
    password = form.password.data

    try:
        user = User.objects.get(email=email)
    except Exception as e:
        return jsonify({'error': 'user not found'})

    if not verify_password(password, user.password):
        return jsonify({'error': 'invalid password'})

    classes = user.classes
    for class in classes:
        class.members.remove(user)

    events = user.event
    for event in events:
        event.members.remove(user)
        event.admins.remove(user)

    user.delete()

    return jsonify({'success': True})
