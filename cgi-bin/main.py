#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cgi
import datetime
from functools import wraps
import json
import logging
import os
import sys

import bottle
from bottle import route, get, post, run, request, response, template, SimpleTemplate, static_file, url, redirect

LOGGER = logging.getLogger("csa")

ROOT_DIR = os.path.abspath('../httpdocs/communitysupportedagriculture.ie/beta1810')
DATA_DIR = ROOT_DIR + '/data'
IMAGES_DIR = ROOT_DIR + '/images'
SCRIPTS_DIR = ROOT_DIR + '/scripts'
STATIC_DIR = ROOT_DIR + '/static'
TMP_DIR = ROOT_DIR + '/tmp'

if SCRIPTS_DIR not in sys.path:
    sys.path.append(SCRIPTS_DIR)

import datautils
import sessionutils



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



#
# Regular pages
#

@route('/')
@route('/home')
def home():
    return sessionutils.render_template('home')
#

@route('/about')
def about():
    return sessionutils.render_template('about')
#

@route('/contact')
def contact():
    return sessionutils.render_template('contact')
#

@route('/resources')
def resources():
    return sessionutils.render_template('resources')
#

@get('/farms')
def farmprofiles():

    # for i in range(0,4):
        # salt = get_salt()
        # hash = get_hash("csa", salt)
        # debug_msg("%s, %s" % (hash, salt))
        # debug_msg("%s, %s" % (type(hash), type(salt)))
    

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

    permissions_dict = datautils.get_permissions_dict()
    farms = permissions_dict['farms']
    farm_content_dict = {}
    for farmname in farms:
        farm_content = datautils.get_farm_content(farmname)
        farm_content_dict[farmname] = farm_content

    return sessionutils.render_template(
        'farmprofiles',
        farm_content_dict=farm_content_dict,
        fixup_url=fixup_url,
        order_info_keys=order_info_keys,
        get_profile_image=get_profile_image)
#

#
# Login pages
#

@get('/login')
def login_get():
    # A request for e.g. '/edit/dublin' will have been redirected to '/login?next=edit/dublin'
    return sessionutils.render_template('login', next=request.query.get('next', ''))
#

@post('/login')
def login_post():
    sessionutils.clear_session()
    form = cgi.FieldStorage()
    username = cgi.escape(form.getfirst('username', ''))
    password = cgi.escape(form.getfirst('password', ''))
    next = cgi.escape(form.getfirst('next', ''))

    ok = datautils.check_password(username, password)
    if ok:
        (role, assigned_farm) = datautils.get_permissions(username)
        now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        sessionutils.flash_message("Signed in user <b>%s</b> on %s" % (username, now))
        LOGGER.info("Signed in user '%s' with role '%s' and permissions for farm '%s'" % (username, role, assigned_farm))

        # Record in session
        sessionutils.setup_session(username, role, assigned_farm)

        # Redirect
        if role == 'admin':
            # E.g. '/admin' or '/edit/dublin'
            # Admins have access to edit any farm profile, so not necessary to check.
            LOGGER.info("User '%s' signed in as admin, redirecting to '%s'" % (username, next))
            redirect('/beta1810/%s' % next)
        else:
            next_parts = next.split('/')
            # Editors are associated with a particular farm, or no farm, os necessary to check if this matches
            # the requested page
            if len(next_parts) == 2 and next_parts[0] == 'edit':
                if next_parts[1] == assigned_farm:
                    LOGGER.info("User '%s' signed in, access granted to '%s'" % (username, next))
                    redirect('/beta1810/%s' % next)
                else:
                    sessionutils.flash_message("Redirected. No access to requested page")
                    LOGGER.info("User '%s' signed in, requested access to '%s', which doesn't match user's farm '%s', so redirecting" % (username, next, assigned_farm))
                    redirect('/beta1810/home')
            else:
                LOGGER.info("User '%s' signed in, didn't request '/edit/<some farm>', so redirecting to home" % username)
                redirect('/beta1810/home')
    else:
        sessionutils.flash_message("Sign in for user <b>%s</b> failed. Please contact admin to check your permissions." % username)
        LOGGER.info("Sign in failed for user '%s'" % username)
        return sessionutils.render_template("login")
#

@route('/logout')
def logout():
    username = request.get_cookie('username', '')
    sessionutils.clear_session()
    if username:
        now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        sessionutils.flash_message("Signed out user <b>%s</b> on %s" % (username, now))
        LOGGER.info("Signed out user '%s'" % username)
    redirect('/beta1810/home')
#

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        dest = request.path[1:]  # Strip first '/' for convenience, and aesthetics
        username = request.get_cookie('username', '')
        if not username:
            LOGGER.info("User '%s' redirected to login, as not in session" % username)
            redirect('/beta1810/login?next=%s' % dest)

        role = request.get_cookie('role', '')
        farmname = 'all' if (role == 'admin') else request.get_cookie('farmname', '')
        dest_parts = dest.split('/')

        if dest_parts[0] == 'edit':
            # E.g. I.e. '/edit/dublin', either 'GET' or 'POST'
            if farmname != 'all' and farmname != dest_parts[1]:
                sessionutils.flash_message("Redirected. Do not have permission to edit farm profile %s" % dest_parts[1])
                LOGGER.info("User '%s' with farm permission '%s' denied access to '/edit/%s', redirected" % (username, farmname, dest_parts[1]))
                redirect('/beta1810/farms')

        elif dest_parts[0] == 'admin':
            # I.e. '/admin'
            if role != admin:
                sessionutils.flash_message("Redirected. Do not have admin permission")
                LOGGER.info("User '%s' with role '%s' denied access to '/admin', redirected" % (username, role))
                redirect('/beta1810/farms')

        return f(*args, **kwargs)
    return decorated_function
#

#
# Admin pages
#

@get('/edit/<farm>')
@login_required
def editfarm(farm):
    farmname = request.get_cookie('farmname')
    username = request.get_cookie('username')
    role = request.get_cookie('role')
    content = datautils.get_farm_content(farmname)
    instructions = json.load(open(os.path.join(DATA_DIR, 'farm-data-instructions.json'), 'rb'))
    data_layout = json.load(open(os.path.join(DATA_DIR, 'farm-data-layout.json'), 'rb'))

    def format_instructions(instructions):
        return '<br>'.join("<i class='fa fa-info-circle'></i> %s" % x for x in instructions)

    return sessionutils.render_template('editfarm', farmname=farmname, username=username, role=role, content=content, instructions=instructions, data_layout=data_layout, format_instructions=format_instructions)
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

    datautils.update_farm_content(farm, updated_content)
    redirect('/beta1810/edit/%s' % farm)
#

@route('/admin')
@login_required
def admin():
    return "hello"
    # global FARM_PERMISSIONS
    # admins = []
    # editors = {}  # Map user to farm
    # farms = []
    # for username in FARM_PERMISSIONS:
        # data = FARM_PERMISSIONS[username]
        # if data['role'] == 'admin':
            # admins.append(username)
        # elif data['role'] == 'editor':
            # editors[username] = data['farmname']
            # farms.append(data['farmname'])
    # farms = list(set(farms))  # Remove duplicates
    # return sessionutils.render_template('admin', admins=admins, editors=editors, farms=farms)
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

#
# Run
#

datautils.setup_logging()
bottle.run(debug=False, server='cgi')
