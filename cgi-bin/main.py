#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cgi
import datetime
from functools import partial
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

PUBLISHED_FARMS = []

import datautils
import sessionutils


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

def farmprofile(farm):
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

    farm_content = datautils.get_farm_content(farm)

    return sessionutils.render_template(
        'farmprofile',
        farm=farm,
        farm_content=farm_content,
        fixup_url=fixup_url,
        order_info_keys=order_info_keys,
        get_profile_image=get_profile_image)
#

def __route_farms():
    global PUBLISHED_FARMS
    permissions_dict = datautils.get_permissions_dict()
    for farmname in permissions_dict['farms']:
        farm_content = datautils.get_farm_content(farmname)
        if farm_content.get('publish', ['no'])[0] == 'yes':
            PUBLISHED_FARMS.append(farmname)
            route('/%s' % farmname, 'GET', partial(farmprofile, farmname))
#

@get('/farms')
def farms():
    permissions_dict = datautils.get_permissions_dict()
    titles = {}
    coords = {}
    for farmname in permissions_dict['farms']:
        farm_content = datautils.get_farm_content(farmname)
        titles[farmname] = farm_content['title'][0]
        coords[farmname] = farm_content.get('coords', [''])[0].split(',')

    def get_farm_title(farmname):
        return titles.get(farmname, farmname.capitalize())

    def get_farm_coords(farmname):
        return coords.get(farmname, [''])

    return sessionutils.render_template(
        'farms',
        published_farms=PUBLISHED_FARMS,
        permissions_dict=permissions_dict,
        get_farm_title=get_farm_title,
        get_farm_coords=get_farm_coords)
#

#
# Login pages
#

@get('/login')
def login_get():
    # A request for e.g. '/edit/dublin' will have been redirected to '/login?nextpage=edit/dublin'
    return sessionutils.render_template('login', nextpage=request.query.get('nextpage', ''))
#

@post('/login')
def login_post():
    sessionutils.clear_session()
    form = cgi.FieldStorage()
    username = cgi.escape(form.getfirst('username', ''))
    password = cgi.escape(form.getfirst('password', ''))
    nextpage = cgi.escape(form.getfirst('nextpage', ''))

    ok = datautils.check_password(username, password)
    if ok:
        (role, assigned_farm) = datautils.get_permissions(username)
        now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        sessionutils.flash_message("Signed in user <b>%s</b> on %s" % (username, now))
        LOGGER.info("Signed in user [%s] with role [%s] and permissions for farm [%s]" % (username, role, assigned_farm))

        # Record in session
        sessionutils.setup_session(username, role, assigned_farm)

        # Redirect
        if role == 'admin':
            # E.g. '/admin' or '/edit/dublin'
            # Admins have access to edit any farm profile, so not necessary to check.
            LOGGER.info("User [%s] signed in as admin redirecting to [%s]" % (username, nextpage))
            redirect('/beta1810/%s' % nextpage)
        else:
            next_parts = nextpage.split('/')
            # Editors are associated with a particular farm, or no farm, os necessary to check if this matches
            # the requested page
            if len(next_parts) == 2 and next_parts[0] == 'edit':
                if next_parts[1] == assigned_farm:
                    LOGGER.info("User [%s] signed in and access granted to [%s]" % (username, nextpage))
                    redirect('/beta1810/%s' % nextpage)
                else:
                    sessionutils.flash_message("Redirected. No access to requested page")
                    LOGGER.info("User [%s] signed in but requested access to [%s] which doesn't match user's farm [%s] so redirecting" % (username, nextpage, assigned_farm))
                    redirect('/beta1810/home')
            else:
                LOGGER.info("User [%s] signed in but didn't request [/edit/<some farm>] so redirecting to home" % username)
                redirect('/beta1810/home')
    else:
        sessionutils.flash_message("Sign in for user <b>%s</b> failed. Please contact admin to check your permissions." % username)
        LOGGER.info("Sign in failed for user [%s]" % username)
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
            LOGGER.info("User [%s] redirected to [/login], as not in session" % username)
            redirect('/beta1810/login?nextpage=%s' % dest)

        role = request.get_cookie('role', '')
        farm_cookie = 'all' if (role == 'admin') else request.get_cookie('farmname', '')
        dest_parts = dest.split('/')

        if dest_parts[0] == 'edit':
            # E.g. I.e. '/edit/dublin', either 'GET' or 'POST'
            if farm_cookie != 'all' and farm_cookie != dest_parts[1]:
                sessionutils.flash_message("Redirected. Do not have permission to edit farm profile %s" % dest_parts[1])
                LOGGER.info("User [%s] with farm permission [%s] denied access to [/edit/%s] so redirected" % (username, farm_cookie, dest_parts[1]))
                redirect('/beta1810/farms')

        elif dest_parts[0] == 'admin':
            # I.e. '/admin'
            if role != 'admin':
                sessionutils.flash_message("Redirected. Do not have admin permission")
                LOGGER.info("User [%s] with role [%s] denied access to [/admin] so redirected" % (username, role))
                redirect('/beta1810/farms')

        return f(*args, **kwargs)
    return decorated_function
#

#
# Admin pages
#

@get('/resetpassword')
@login_required
def resetpassword():
    return sessionutils.render_template('resetpassword')
#

@post('/resetpassword')
@login_required
def resetpassword_post():
    form = cgi.FieldStorage()
    new_password = form.getlist("password")[0]
    salt = datautils.make_salt()
    hash = datautils.get_hash(new_password, salt)
    username = request.get_cookie('username')
    permissions_dict = datautils.get_permissions_dict()
    permissions_dict['hashed_passwords'][username] = hash
    permissions_dict['password_salts'][username] = salt

    datautils.update_permissions_dict(permissions_dict)
    sessionutils.flash_message("Password for user <b>%s</b> reset" % username)
    redirect('/beta1810/home')
#

@get('/edit/<farm>')
@login_required
def editfarm(farm):
    username = request.get_cookie('username')
    role = request.get_cookie('role')
    content = datautils.get_farm_content(farm)
    instructions = json.load(open(os.path.join(DATA_DIR, 'farm-data-instructions.json'), 'rb'))
    data_layout = json.load(open(os.path.join(DATA_DIR, 'farm-data-layout.json'), 'rb'))

    def format_instructions(instructions):
        return '<br>'.join("<i class='fa fa-info-circle'></i> %s" % x for x in instructions)

    return sessionutils.render_template(
        'editfarm',
        farm=farm,
        content=content,
        instructions=instructions,
        data_layout=data_layout,
        format_instructions=format_instructions)
#

@post('/edit/<farm>')
@login_required
def editfarm_post(farm):
    # Retrieve data from the submitted form
    form = cgi.FieldStorage()
    form_keys = form.keys()

    # The layout of the "editprofile" page is constructed according to farm-data-layout.json, so
    # the logic here matches the "inputs" in that form.
    layout = json.load(open(os.path.join(DATA_DIR, 'farm-data-layout.json'), 'rb'))
    checkbox_inputs = layout['checkbox-inputs']
    nested_inputs = layout['nested-inputs']
    updated_content = {}

    # Deal with images on their own before going through other items
    images = form["images"] if ("images" in form) else []
    if type(images) != list:
        images = [images]

    # First get existing images, not those from file inputs
    values = form.getlist("images$existing")

    for image in images:
        if image.filename:
            image_path = datautils.save_img(farm, image)
            rel_path = os.path.relpath(image_path, ROOT_DIR)
            values.append(rel_path)

    # Add image paths to dict
    updated_content["images"] = values

    # Set profile image, if selected
    default_image_token = 'is-default-img-'
    default_image_keys = [x for x in form_keys if x.startswith(default_image_token)]
    if default_image_keys:
        updated_content['default-image'] = default_image_keys[0][len(default_image_token):]
    LOGGER.info("form keys %s" % str(form_keys))

    # If a checkbox is unchecked, it will not be present in form.keys
    for key in checkbox_inputs:
        if key in form_keys:
            updated_content[key] = ["yes"]
        else:
            updated_content[key] = ["no"]

    for key in form_keys:
        # Some entries in the farm data contain nested data. E.g. under "info", the editor of the farm profile is 
        # allowed to add or remove key-value pairs, e.g. "Pick up location", which could be an address consisting
        # of multiple strings.
        key_tokens = key.split('$')
        main_key = key_tokens[0]

        # The form may have some inputs not used here, e.g. inputs for adding new key-value pairs
        if main_key not in layout['order']:
            continue

        # New images, "images", and "images-existing", have been dealt with above
        if main_key == "images" or main_key in checkbox_inputs:
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

    datautils.delete_removed_imgs(farm, updated_content)
    datautils.update_farm_content(farm, updated_content)
    sessionutils.flash_message("Farm profile <b>%s</b> updated" % farm)
    redirect('/beta1810/edit/%s' % farm)
#

@get('/admin')
@login_required
def admin():
    permissions_dict = datautils.get_permissions_dict()
    farms = ['None'] + permissions_dict['farms']

    def get_selected_farm(editor):
        associated = permissions_dict['permissions'].get(editor, '')
        associate = 'None' if associated == '' else associated
        return [('selected' if x == associated else '', x) for x in farms]

    return sessionutils.render_template(
        'admin',
        permissions_dict=permissions_dict,
        get_selected_farm=get_selected_farm)
#

@post('/admin')
@login_required
def admin():
    # Retrieve data from the submitted form
    form = cgi.FieldStorage()
    form_keys = form.keys()

    # Get current database
    permissions_dict = datautils.get_permissions_dict()

    # Admins
    existing_admins = form.getlist("admin$existing")
    admins_to_remove = [x for x in permissions_dict['admins'] if x not in existing_admins]
    for admin_to_remove in admins_to_remove:
        datautils.delete_user(admin_to_remove, 'admins', permissions_dict)
        LOGGER.info("Removed admin [%s]" % admin_to_remove)

    new_admins = [x for x in form.getlist("admin$new") if x != '']
    for new_admin in new_admins:
        datautils.add_user(new_admin, 'admins', permissions_dict)
        LOGGER.info("Added admin [%s]" % new_admin)

    # Editors
    existing_editors = form.getlist("editor$existing")
    editors_to_remove = [x for x in permissions_dict['editors'] if x not in existing_editors]
    for editor_to_remove in editors_to_remove:
        datautils.delete_user(editor_to_remove, 'editors', permissions_dict)
        LOGGER.info("Removed editor [%s]" % editor_to_remove)

    new_editors = [x for x in form.getlist("editor$new") if x != '']
    for new_editor in new_editors:
        datautils.add_user(new_editor, 'editors', permissions_dict)
        LOGGER.info("Added editor [%s]" % new_editor)

    # Permissions
    existing_permissions = permissions_dict['permissions'].keys()
    for editor in existing_permissions:
        if editor not in permissions_dict['editors']:
            permissions_dict['permissions'].pop(editor)
    permission_keys = [x for x in form_keys if x.startswith('permission$')]
    for permission_key in permission_keys:
        editor = permission_key.split('$')[1]
        permission = form.getlist(permission_key)[0]
        permissions_dict['permissions'][editor] = '' if permission == 'None' else permission

    # Farms
    existing_farms = form.getlist("farm$existing")
    farms_to_remove = [x for x in permissions_dict['farms'] if x not in existing_farms]
    for farm_to_remove in farms_to_remove:
        datautils.delete_farm(farm_to_remove, permissions_dict)
        LOGGER.info("Removed farm [%s]" % farm_to_remove)

    new_farms = [x for x in form.getlist("farm$new") if x != '']
    for new_farm in new_farms:
        datautils.add_farm(new_farm, permissions_dict)
        LOGGER.info("Added farm [%s]" % new_farm)

    datautils.update_permissions_dict(permissions_dict)
    redirect('/beta1810/admin')
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
__route_farms()
bottle.run(debug=False, server='cgi')
