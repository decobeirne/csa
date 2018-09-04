#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cgi
import datetime
from collections import OrderedDict
import json
import os

import bottle
from bottle import route, get, post, run, request, response, template, SimpleTemplate, static_file, url, redirect

#
# Defines
#

ROOT_DIR = os.path.abspath('../httpdocs/communitysupportedagriculture.ie/Development20180422_frameworks')
TPL_DIR = ROOT_DIR + '/templates'
IMAGES_DIR = ROOT_DIR + '/images'
STATIC_DIR = ROOT_DIR + '/static'
TMP_DIR = ROOT_DIR + '/tmp'
DATA_DIR = ROOT_DIR + '/data'

REQ_FLASH_MSGS_READ = False

LINKS = OrderedDict([
    ('About', {'link': 'about'}),
    ('Farm Profiles', {'link': 'farmprofiles'}),
    ('Farm Profiles Beta', {'link': 'farmprofiles-beta'}),
    ('Resources', {'link': 'resources'}),
    ('Contact', {'link': 'contact'}),
    ('Facebook', {'link': 'https://www.facebook.com/groups/245019725582313', 'tags': 'target="_blank"'}),
    ])
#

#
# Utility functions
#

def debug_msg(msg):  # TODO: delete
    cwd = os.getcwd()
    try:
        os.chdir(TMP_DIR)
        fd = open("debug.txt", "a")
        fd.write(msg)
        fd.write("\n")
        fd.close()
    finally:
        os.chdir(cwd)
#

def get_flash_messages():
    """
    Read the flash messages currently stored in the 'flash' cookie. These may be in the request object,
    if e.g. there was a redirect, otherwise messages from this request will be in the response object.
    """
    global REQ_FLASH_MSGS_READ
    msg = ""
    if not REQ_FLASH_MSGS_READ:
        # We haven't read the 'flash' messages from the request, i.e. in flash_message, so we will not have
        # written these into the response
        cookies = bottle.request.cookies
        request_msg = bottle.request.get_cookie("flash")
        if request_msg:
            msg = request_msg
        REQ_FLASH_MSGS_READ = True
    else:
        if bottle.response._cookies:
            morsel = bottle.response._cookies.get('flash', None)
            if morsel:
                current_msg = morsel.value
                msg = current_msg

    # It seems that if a cookie is not set in the response, the value from the request is taken. So
    # if the current flash message is taken from the request or the response, wiping it in the response
    # will be sufficient.
    bottle.response.set_cookie('flash', "", path='/')
    msgs = [x for x in msg.split('$') if x != '']
    return msgs


def flash_message(msg):
    global REQ_FLASH_MSGS_READ
    msgs = []
    if not REQ_FLASH_MSGS_READ:
        cookies = bottle.request.cookies
        request_msg = bottle.request.get_cookie("flash")
        if request_msg:
            msg = request_msg + '$' + msg
        REQ_FLASH_MSGS_READ = True
    written = False
    if bottle.response._cookies:
        morsel = bottle.response._cookies.get('flash', None)
        if morsel:
            current_msg = morsel.value
            msg = current_msg + '$' + msg
            bottle.response._cookies['flash'] = msg
            written = True
    if not written:
        bottle.response.set_cookie('flash', msg, path='/')
        bottle.response.set_cookie('foo', 'bar', path='/')


def render_template(name, **kwargs):
    """
    Render template with flash messages.
    """
    cwd = os.getcwd()
    try:
        os.chdir(TPL_DIR)
        tpl_name = name + '.tpl'
        if not os.path.isfile(tpl_name):
            return "Error"  # TODO
        tpl = SimpleTemplate(source=open(tpl_name).read())
        username = request.get_cookie('username')
        role = request.get_cookie('role')
        farmname = request.get_cookie('farmname')
        kwargs.update(
            {'page_name': name,
             'links': LINKS,
             'messages_to_flash': get_flash_messages(),  # Retrieve and wipe flash messages
             'username': username,
             'role': role,
             'farmname': farmname})
        return tpl.render(**kwargs)
    finally:
        os.chdir(cwd)

#
# Regular pages
#

@route('/')
@route('/home')
def home():
    return render_template('home')
#

@route('/about')
def about():
    return render_template('about')
#

@route('/farmprofiles')
def farmprofiles():
    return render_template('farmprofiles')
#

@route('/contact')
def contact():
    return render_template('contact')
#

@route('/resources')
def resources():
    return render_template('resources')
#

@get('/farmprofiles-beta')
def farmprofiles_beta_get():
    def fixup_url(url):
        if url.startswith('http://') or url.startswith('https://'):
            return url
        return 'http://' + url

    farm_dict = json.load(open(os.path.join(DATA_DIR, 'farms.json'), 'rb'))
    farms = farm_dict['farms']
    farm_content_dict = {}
    for farmname in farms:
        farm_content = get_farm_content(farmname)
        farm_content_dict[farmname] = farm_content
    return render_template('farmprofiles-beta', farm_content_dict=farm_content_dict, fixup_url=fixup_url)
#

#
# Admin pages
#

@get('/login')
def login_get():
    return render_template('login')
#

# TODO: NB save passwords as hash+salt in a db instead of as raw text
FARM_PERMISSIONS = {
    'declan': {'role': 'admin', 'password': 'declan'},
    'roisin': {'role': 'admin', 'password': 'roisin'},
    'seamus': {'role': 'editor', 'password': 'seamus', 'farmname': 'cloughjordan'},
    'paddy': {'role': 'editor', 'password': 'paddy', 'farmname': 'cloughjordan'},
}


def clear_session():
    bottle.response.set_cookie('farmname', '', path='/')
    bottle.response.set_cookie('username', '', path='/')
    bottle.response.set_cookie('role', '', path='/')
#

def authenticate(username, password):
    """
    Authenticate given username and password against database.
    Returns:
        (str) Type of user.
    """
    global FARM_PERMISSIONS
    if username and password:
        if username in FARM_PERMISSIONS:
            if 'password' in FARM_PERMISSIONS[username] and password == FARM_PERMISSIONS[username]['password'] and 'role' in FARM_PERMISSIONS[username]:
                role = FARM_PERMISSIONS[username]['role']
                # https://stackoverflow.com/questions/21215904/read-cookie-text-value-in-a-python-bottle-application
                bottle.response.set_cookie('farmname', 'cloughjordan', path='/')  # todo temp
                bottle.response.set_cookie('username', username, path='/')
                bottle.response.set_cookie('role', role, path='/')
                return role
    clear_session()
    return None
#

@post('/login')
def login_post():
    clear_session()
    form = cgi.FieldStorage()
    username = cgi.escape(form.getfirst('username', ''))
    password = cgi.escape(form.getfirst('password', ''))
    bottle.response.set_cookie('foo2', 'bar2', path='/')
    role = authenticate(username, password)
    bottle.response.set_cookie('foo3', 'bar3', path='/')
    if role in ['admin', 'editor']:
        auth_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        flash_message("Authenticated user <b>%s</b> on %s" % (username, auth_time))
        if role == 'admin':
            redirect('/Development20180422_frameworks/admin')
        else:
            redirect('/Development20180422_frameworks/editfarm')
    flash_message("Authentication for user <b>%s</b> failed. Please contact admin to reset your password if required." % username)
    return render_template("login")
#

@route('/logout')
def logout():
    username = request.get_cookie('username', '')
    clear_session()
    if username:
        flash_message("Signed out user <b>%s</b>" % username)
    redirect('/Development20180422_frameworks/login')
#

# Ref: http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
from functools import wraps

def farm_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = request.get_cookie('username', '')
        role = request.get_cookie('role', '')
        if username and role == 'admin':
            flash_message("Redirected. Do not have permission to edit farm profile.")
            redirect('/Development20180422_frameworks/home')
        if not username or role != 'editor':
            # TODO: check farm profile also - for now only have one farm
            redirect('/Development20180422_frameworks/login')
        return f(*args, **kwargs)
    return decorated_function
#

def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = request.get_cookie('username', '')
        role = request.get_cookie('role', '')
        if username and role == 'editor':
            flash_message("Redirected. Do not have access to admin page.")
            redirect('/Development20180422_frameworks/home')
        if not username or role != 'admin':
            redirect('/Development20180422_frameworks/login')
        return f(*args, **kwargs)
    return decorated_function
#

def get_new_farm_content():
    return OrderedDict([
        ("title", ""),
        ("images", []),
        ("description", []),
        ("info", OrderedDict([
            ("Website", ""),
            ("Email", ""),
            ("Address", []),
            ("Farmers", [])
        ])),
    ])
#

def get_farm_json_file(farmname):
    return os.path.join(DATA_DIR, '%s.json' % farmname)
#

def get_farm_content(farmname):
    json_file = get_farm_json_file(farmname)
    if os.path.isfile(json_file):
        content = json.load(open(json_file, 'rb'))
    else:
        content = get_new_farm_content()
    return content
#

def update_farm_content(farmname, content):
    json_file = get_farm_json_file(farmname)
    debug_msg("update_farm_content json_file is '%s'" % json_file)
    json.dump(content, open(json_file, 'wb'))
#

@get('/editfarm')
@farm_login_required
def editfarm():
    farmname = request.get_cookie('farmname')
    username = request.get_cookie('username')
    role = request.get_cookie('role')
    content = get_farm_content(farmname)
    instructions = json.load(open(os.path.join(DATA_DIR, 'farm-data-instructions.json'), 'rb'))
    data_layout = json.load(open(os.path.join(DATA_DIR, 'farm-data-layout.json'), 'rb'))
    return render_template('editfarm', farmname=farmname, username=username, role=role, content=content, instructions=instructions, data_layout=data_layout)
#

from HTMLParser import HTMLParser

@post('/editfarm')
@farm_login_required
def editfarm_post():
    # Retrieve data from form on the "editprofile" page.
    form = cgi.FieldStorage()
    farmname = cgi.escape(form.getfirst('farmname', ''))
    form_keys = form.keys()

    # The layout of the "editprofile" page is constructed according to farm-data-layout.json, so
    # the logic here matches the "inputs" in that form.
    layout = json.load(open(os.path.join(DATA_DIR, 'farm-data-layout.json'), 'rb'))
    nested_inputs = layout['nested-inputs']

    updated_content = {}
    for key in sorted(form_keys):
        values = form.getlist(key)

        # Some entries in the farm data contain nested data. E.g. under "info", the editor of the farm profile is 
        # allowed to add or remove key-value pairs, e.g. "Pick up location", which could be an address consisting
        # of multiple strings.
        key_tokens = key.split('$')
        main_key = key_tokens[0]

        if main_key in nested_inputs:
            # For nested data, the "input" in the form is given the name "main-key$sub-key", e.g. "info$website"
            sub_key = key_tokens[1]
            if main_key not in updated_content:
                updated_content[main_key] = {}
            updated_content[main_key][sub_key] = values
        else:
            # If this entry is not identified in farm-data-layout.json as containing nested data, then it will
            # contain a list of strings
            updated_content[main_key] = values

    update_farm_content(farmname, updated_content)
    redirect('/Development20180422_frameworks/editfarm')
#

@route('/admin')
@admin_login_required
def admin():
    global FARM_PERMISSIONS
    admins = []
    editors = {}  # Map user to farm
    farms = []
    for username in FARM_PERMISSIONS:
        data = FARM_PERMISSIONS[username]
        if data['role'] == 'admin':
            admins.append(username)
        elif data['role'] == 'editor':
            editors[username] = data['farmname']
            farms.append(data['farmname'])
    farms = list(set(farms))  # Remove duplicates
    return render_template('admin', admins=admins, editors=editors, farms=farms)
#




"""
Provide images and static files (scripts, css) to the browser using bottle.static_file.

References:
* https://stackoverflow.com/questions/6978603/how-to-load-a-javascript-or-css-file-into-a-bottlepy-template
* https://bottlepy.org/docs/dev/tutorial.html#tutorial-static-files
"""

@route('/images/<filepath:path>')
def image(filepath):
    return static_file(filepath, root=IMAGES_DIR)
#

@route('/static/<filepath:path>')
def static(filepath):
    return static_file(filepath, root=STATIC_DIR)
#

bottle.run(debug=False, server='cgi')
