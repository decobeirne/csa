#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cgi
from collections import OrderedDict
import datetime
from functools import wraps
import json
import os

import bottle
from bottle import route, get, post, run, request, response, template, SimpleTemplate, static_file, url, redirect

#
# Defines
#

ROOT_DIR = os.path.abspath('../httpdocs/communitysupportedagriculture.ie/beta1810')
TPL_DIR = ROOT_DIR + '/templates'
IMAGES_DIR = ROOT_DIR + '/images'
STATIC_DIR = ROOT_DIR + '/static'
TMP_DIR = ROOT_DIR + '/tmp'
DATA_DIR = ROOT_DIR + '/data'

REQ_FLASH_MSGS_READ = False

LINKS = OrderedDict([
    ('About', {'link': 'about'}),
    ('Farm Profiles', {'link': 'farms'}),
    ('Resources', {'link': 'resources'}),
    ('Contact', {'link': 'contact'}),
    ('Facebook', {'link': 'https://www.facebook.com/groups/245019725582313', 'tags': 'target="_blank"'}),
    ])
#

#
# Utility functions
#

def debug_msg(msg):  # TODO: delete / replace with logging
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
        tpl = SimpleTemplate(source=open(name + '.tpl').read())
        username = request.get_cookie('username')
        role = request.get_cookie('role')
        farmname = request.get_cookie('farmname')
        root_rel_dir = '../' * (request.path.count('/') - 1) # E.g. '/foo' == 0 == '', '/foo/bar' == 1 == '../'
        kwargs.update(
            {'page_name': name,
             'links': LINKS,
             'messages_to_flash': get_flash_messages(),  # Retrieve and wipe flash messages
             'username': username,
             'role': role,
             'farmname': farmname,
             'root_rel_dir': root_rel_dir})
        return tpl.render(**kwargs)
    finally:
        os.chdir(cwd)

#
# Data functions
#

def get_new_farm_content():
    json_file = get_farm_json_file('new-farm')
    return json.load(open(json_file, 'rb'))
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

@route('/contact')
def contact():
    return render_template('contact')
#

@route('/resources')
def resources():
    return render_template('resources')
#

@get('/farms')
def farmprofiles():
    data_layout = json.load(open(os.path.join(DATA_DIR, 'farm-data-layout.json'), 'rb'))

    def fixup_url(url):
        if url.startswith('http://') or url.startswith('https://'):
            return url
        return 'http://' + url

    def order_info_keys(keys):
        keys = sorted(keys)
        required_keys = []
        for key in data_layout['required-nested-inputs']:
            if key in keys:
                keys.remove(key)
                required_keys.append(key)
        required_keys = reversed(sorted(required_keys))
        for key in required_keys:
            keys.insert(0, key)
        return keys

    def get_profile_image(content):
        default = content.get('default-image', '')
        images = content.get('images', [])
        return "" if not images else (default if (default in images) else images[0])

    permissions_dict = json.load(open(os.path.join(DATA_DIR, 'permissions.json'), 'rb'))
    farms = permissions_dict['farms']
    farm_content_dict = {}
    for farmname in farms:
        farm_content = get_farm_content(farmname)
        farm_content_dict[farmname] = farm_content

    return render_template(
        'farmprofiles',
        farm_content_dict=farm_content_dict,
        fixup_url=fixup_url,
        order_info_keys=order_info_keys,
        get_profile_image=get_profile_image)
#

#
# Admin pages
#
# TODO: NB save passwords as hash+salt in a db instead of as raw text
FARM_PERMISSIONS = {
    # 'declan': {'role': 'admin', 'password': 'declan'},
    # 'roisin': {'role': 'admin', 'password': 'roisin'},
    # 'seamus': {'role': 'editor', 'password': 'seamus', 'farmname': 'cloughjordan'},
    'Pat': {'role': 'editor', 'password': 'Pat', 'farmname': 'cloughjordan'},
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
                # See link for relevance of setting path
                # https://stackoverflow.com/questions/21215904/read-cookie-text-value-in-a-python-bottle-application
                role = FARM_PERMISSIONS[username]['role']
                farmname = FARM_PERMISSIONS[username]['farmname']
                bottle.response.set_cookie('username', username, path='/')
                bottle.response.set_cookie('role', role, path='/')
                bottle.response.set_cookie('farmname', farmname, path='/')
                return (username, role, farmname)
    clear_session()
    return None
#

@get('/login')
def login_get():
    # A request for e.g. '/edit/dublin' will have been redirected to '/login?next=edit/dublin'
    return render_template('login', next=request.query.get('next', ''))
#

@post('/login')
def login_post():
    clear_session()
    form = cgi.FieldStorage()
    username = cgi.escape(form.getfirst('username', ''))
    password = cgi.escape(form.getfirst('password', ''))
    next = cgi.escape(form.getfirst('next', ''))
    auth_res = authenticate(username, password)

    auto_ok = False
    if auth_res is not None:
        (auth_username, auth_role, auth_farmname) = auth_res
        if auth_role == 'admin' or auth_role == 'editor':
            auth_ok = True

    if auth_ok:
        auth_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        flash_message("Authenticated user <b>%s</b> on %s" % (username, auth_time))  # TODO: should log all this
        if auth_role == 'admin':
            # E.g. '/admin' or '/edit/dublin'
            redirect('/beta1810/%s' % next)
        else:
            next_parts = next.split('/')
            if len(next_parts) == 2 and next_parts[0] == 'edit':
                if next_parts[1] == auth_farmname:
                    redirect('/beta1810/%s' % next)
                else:
                    flash_message("Redirected. Do not have access permission")
                    redirect('/beta1810/home')
            else:
                redirect('/beta1810/home')
    else:
        flash_message("Authentication for user <b>%s</b> failed. Please contact admin to reset your password if required." % username)
        return render_template("login")
#

@route('/logout')
def logout():
    username = request.get_cookie('username', '')
    clear_session()
    if username:
        flash_message("Signed out user <b>%s</b>" % username)
    redirect('/beta1810/home')
#

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        dest = request.path[1:]  # Strip first '/' for convenience, and aesthetics
        username = request.get_cookie('username', '')
        if not username:
            redirect('/beta1810/login?next=%s' % dest)

        role = request.get_cookie('role', '')
        farmname = 'all' if (role == 'admin') else request.get_cookie('farmname', '')
        dest_parts = dest.split('/')

        if dest_parts[0] == 'edit':
            # E.g. I.e. '/edit/dublin', either 'GET' or 'POST'
            if farmname != 'all' and farmname != dest_parts[1]:
                flash_message("Redirected. Do not have permission to edit farm profile %s" % dest_parts[1])
                redirect('/beta1810/farms')

        elif dest_parts[0] == 'admin':
            # I.e. '/admin'
            if role != admin:
                flash_message("Redirected. Do not have admin permission")
                redirect('/beta1810/farms')

        return f(*args, **kwargs)
    return decorated_function
#

@get('/edit/<farm>')
@login_required
def editfarm(farm):
    farmname = request.get_cookie('farmname')
    username = request.get_cookie('username')
    role = request.get_cookie('role')
    content = get_farm_content(farmname)
    instructions = json.load(open(os.path.join(DATA_DIR, 'farm-data-instructions.json'), 'rb'))
    data_layout = json.load(open(os.path.join(DATA_DIR, 'farm-data-layout.json'), 'rb'))

    def format_instructions(instructions):
        return '<br>'.join("<i class='fa fa-info-circle'></i> %s" % x for x in instructions)

    return render_template('editfarm', farmname=farmname, username=username, role=role, content=content, instructions=instructions, data_layout=data_layout, format_instructions=format_instructions)
#

@post('/edit/<farm>')
@login_required
def editfarm_post(farm):
    # Retrieve data from form on the "editprofile" page.
    form = cgi.FieldStorage()
    form_keys = form.keys()

    # The layout of the "editprofile" page is constructed according to farm-data-layout.json, so
    # the logic here matches the "inputs" in that form.
    layout = json.load(open(os.path.join(DATA_DIR, 'farm-data-layout.json'), 'rb'))
    nested_inputs = layout['nested-inputs']
    updated_content = {}

    # Deal with images on their own before going through other items
    images = form["images"] if ("images" in form) else []
    if type(images) != list:
        debug_msg("Warning: editfarm_post, IMAGES not a list")
        images = [images]

    # First get existing images, not those from file inputs
    values = form.getlist("images$existing")

    for image in images:
        if image.filename:
            # Write image to file
            dest = os.path.join(IMAGES_DIR, 'uploads', farm, os.path.basename(image.filename))
            if not os.path.isfile(dest):
                dest_dir = os.path.dirname(dest)
                if not os.path.isdir(dest_dir):
                    os.makedirs(dest_dir)
                debug_msg("Uploading to %s" % dest)
                dest_file = open(dest, 'wb', 1000)
                while True:
                    packet = image.file.read(1000)
                    if not packet:
                        break
                    dest_file.write(packet)
                dest_file.close()

            # Add path
            rel_dest = os.path.relpath(dest, ROOT_DIR)
            values.append(rel_dest)

    # Add image paths to dict
    updated_content["images"] = values

    # Set profile image, if selected
    default_image_token = 'is-default-img-'
    default_image_keys = [x for x in form_keys if x.startswith(default_image_token)]
    if default_image_keys:
        updated_content['default-image'] = default_image_keys[0][len(default_image_token):]

    for key in sorted(form_keys):
        # Some entries in the farm data contain nested data. E.g. under "info", the editor of the farm profile is 
        # allowed to add or remove key-value pairs, e.g. "Pick up location", which could be an address consisting
        # of multiple strings.
        key_tokens = key.split('$')
        main_key = key_tokens[0]

        # The form may have some inputs not used here, e.g. inputs for adding new key-value pairs
        if main_key not in layout['order']:
            continue

        # New images, "images", and "images-existing", have been dealt with above
        if main_key == "images":
            continue

        values = form.getlist(key)

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

    update_farm_content(farm, updated_content)
    redirect('/beta1810/edit/%s' % farm)
#

@route('/admin')
@login_required
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

#
# Provide images and static files (scripts, css) to the browser using bottle.static_file.
#
# References:
# * https://stackoverflow.com/questions/6978603/how-to-load-a-javascript-or-css-file-into-a-bottlepy-template
# * https://bottlepy.org/docs/dev/tutorial.html#tutorial-static-files
#

@route('/images/<filepath:path>')
def image(filepath):
    return static_file(filepath, root=IMAGES_DIR)
#

@route('/static/<filepath:path>')
def static(filepath):
    return static_file(filepath, root=STATIC_DIR)
#

bottle.run(debug=False, server='cgi')
