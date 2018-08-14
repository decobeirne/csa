#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cgi
import datetime
from collections import OrderedDict
import json
import os

# Use cgitb.handler() under an except block
# Ref: http://cgi.tutorial.codepoint.net/debugging
# import cgitb
# cgitb.enable()

import bottle
from bottle import route, get, post, run, request, response, template, SimpleTemplate, static_file, url, redirect


ROOT_DIR = os.path.abspath('../httpdocs/communitysupportedagriculture.ie/Development20180422_frameworks')
TPL_DIR = ROOT_DIR + '/templates'
IMAGES_DIR = ROOT_DIR + '/images'
STATIC_DIR = ROOT_DIR + '/static'
TMP_DIR = ROOT_DIR + '/tmp'
DATA_DIR = ROOT_DIR + '/data'


# @route('/hi/<name>')
# def hi(name):
    # return template("Good evening {{name}}, how are you", name=name)

# @route('/i/love/<name>')
# def love(name):
    # return template("I totally love {{name}}", name=name)
#

# @route('/admin')
# def admin_func():
    # return "Login here"
#

# def get_tpl(name):
    # tpl_path = os.path.join(TPL_DIR, name)
    # if os.path.isfile(tpl_path):
        # return tpl_path
    # return None
# #

LINKS = OrderedDict([
    ('About', {'link': 'about'}),
    ('Farm Profiles', {'link': 'farmprofiles'}),
    ('Farm Profiles Beta', {'link': 'farmprofiles-beta'}),
    ('Resources', {'link': 'resources'}),
    ('Contact', {'link': 'contact'}),
    ('Facebook', {'link': 'https://www.facebook.com/groups/245019725582313', 'tags': 'target="_blank"'}),
    ])
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


REQ_FLASH_MSGS_READ = False


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
    bottle.response.set_cookie('flash', "")
    return msg.split('$')


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
        bottle.response.set_cookie('flash', msg)


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
        kwargs.update({'page_name': name, 'links': LINKS, 'messages_to_flash': get_flash_messages()})  # Retrieve and wipe flash messages
        return tpl.render(**kwargs)
    finally:
        os.chdir(cwd)


@route('/')
@route('/home')
def home():
    try:
        tpl_name = 'home.tpl'
        cwd = os.getcwd()
        os.chdir(TPL_DIR)
        if not os.path.isfile(tpl_name):
            return "Error"
        tpl = SimpleTemplate(source=open(tpl_name).read())
        return tpl.render(page_name='home', links=LINKS)
    except Exception as exc:
        return str(exc)
    finally:
        os.chdir(cwd)
#

@route('/about')
def about():
    try:
        tpl_name = 'about.tpl'
        cwd = os.getcwd()
        os.chdir(TPL_DIR)
        if not os.path.isfile(tpl_name):
            return "Error"
        tpl = SimpleTemplate(source=open(tpl_name).read())
        return tpl.render(page_name='about', links=LINKS)
    except Exception as exc:
        return str(exc)
    finally:
        os.chdir(cwd)
#

@route('/farmprofiles')
def farmprofiles():
    try:
        tpl_name = 'farmprofiles.tpl'
        cwd = os.getcwd()
        os.chdir(TPL_DIR)
        if not os.path.isfile(tpl_name):
            return "Error"
        tpl = SimpleTemplate(source=open(tpl_name).read())
        return tpl.render(page_name='farmprofiles', links=LINKS)
    except Exception as exc:
        return str(exc)
    finally:
        os.chdir(cwd)
#

@post('/farmprofiles-beta')
def farmprofiles_beta_post():
    try:

        
        cwd = os.getcwd()
        
        import cgi
        form = cgi.FieldStorage() # instantiate only once!
        name = form.getfirst('name', 'no name')

        # Avoid script injection escaping the user input
        name = cgi.escape(name)
        
        
        response.set_cookie('name', name)

        return """\
        Content-Type: text/html\n
        <html><body>
        <p>The submitted name was "%s"</p>
        </body></html>
        """ % name

            
    except Exception as exc:
        return str(exc)
    finally:
        os.chdir(cwd)
#

@get('/farmprofiles-beta')
def farmprofiles_beta_get():
    try:
            
        tpl_name = 'farmprofiles-beta.tpl'
        cwd = os.getcwd()
        os.chdir(TPL_DIR)
        
        if not os.path.isfile(tpl_name):
            return "Error"
        tpl = SimpleTemplate(source=open(tpl_name).read())
        return tpl.render(page_name='farmprofiles-beta', links=LINKS)
            
    except Exception as exc:
        return str(exc)
    finally:
        os.chdir(cwd)
#

@get('/login')
def login_get():
    #flash_message("I'm going to login")
    return render_template('login')
#

# TODO: NB save passwords as hash+salt in a db instead of as raw text
PERMISSIONS = {
    'declan': {'role': 'admin', 'password': 'declan', 'farms': 'cloughjordan'},
    # 'roisin': {'role': 'admin', 'password': 'roisin', 'farms': 'cloughjordan;dublin'},
    #'seamus': {'role': 'editor', 'password': 'seamus', 'farms': 'dublin'},
    'paddy': {'role': 'editor', 'password': 'paddy', 'farms': 'cloughjordan'},
}


def clear_session():
    bottle.response.delete_cookie('farmname')
    bottle.response.delete_cookie('username')
    bottle.response.delete_cookie('role')
#

def authenticate(username, password):
    """
    Authenticate given username and password against database.
    Returns:
        (str) Type of user.
    """
    global PERMISSIONS
    if username and password:
        if username in PERMISSIONS:
            if 'password' in PERMISSIONS[username] and password == PERMISSIONS[username]['password'] and 'role' in PERMISSIONS[username]:
                role = PERMISSIONS[username]['role']
                bottle.response.set_cookie('farmname', 'cloughjordan')  # todo temp
                bottle.response.set_cookie('username', username)
                bottle.response.set_cookie('role', role)
                return role
    clear_session()
    return None
#

@post('/login')
def login_post():
    #flash_message("login post")
    form = cgi.FieldStorage()
    username = cgi.escape(form.getfirst('username', ''))
    password = cgi.escape(form.getfirst('password', ''))
    role = authenticate(username, password)
    if role != None:
        auth_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        flash_message("Authenticated user <b>%s</b> at %s" % (username, auth_time))
        if role == 'admin':
            redirect('/Development20180422_frameworks/editfarm')  # TODO: should have admin landing page - create and delete farms
        else:
            redirect('/Development20180422_frameworks/editfarm')
    flash_message("Authentication for user '%s' failed. Please contact admin to reset." % username)
    return render_template("login")
#


@route('/logout')
def logout():
    clear_session()
    flash_message("Signed out")
    redirect('/Development20180422_frameworks/login')
#

# Ref: http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = request.get_cookie('username', None)
        role = request.get_cookie('role', None)
        debug_msg("login_required username:%s role:%s" % (username, role))
        if username is None or role not in ['admin', 'editor']:
            return render_template("login")
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

@route('/editfarm')
@login_required
def editfarm():
    debug_msg("editfarm")
    debug_msg("bottle.request.cookies: %s" % str(bottle.request.cookies.__dict__))
    debug_msg("bottle.response._cookies: %s" % str(bottle.response._cookies))
    debug_msg("\n\n")

    farmname = request.get_cookie('farmname')
    username = request.get_cookie('username')
    role = request.get_cookie('role')
    # farmname = 'cloughjordan'
    json_file = os.path.join(DATA_DIR, '%s.json' % farmname)
    if os.path.isfile(json_file):
        content = json.load(open(json_file, 'rb'))
    else:
        content = get_new_farm_content()
    instructions = json.load(open(os.path.join(DATA_DIR, 'instructions.json'), 'rb'))
    return render_template('editfarm', farmname=farmname, username=username, role=role, content=content, instructions=instructions)
#

@route('/admin')
@login_required
def admin():
    try:
        
        username = request.get_cookie('username', '')
        
        import pprint
        data = pprint.pformat(request.environ)
        
        
        cwd = os.getcwd()
        os.chdir(TPL_DIR)
        
        tpl = SimpleTemplate(source=open('admin.tpl').read())
        return tpl.render(page_name='admin', links=LINKS, user=username, data=data)
            
    except Exception as exc:
        return str(exc)
    finally:
        os.chdir(cwd)
#

@route('/contact')
def contact():
    try:
        tpl_name = 'contact.tpl'
        cwd = os.getcwd()
        os.chdir(TPL_DIR)
        if not os.path.isfile(tpl_name):
            return "Error"
        tpl = SimpleTemplate(source=open(tpl_name).read())
        return tpl.render(page_name='contact', links=LINKS)
    except Exception as exc:
        return str(exc)
    finally:
        os.chdir(cwd)
#

@route('/resources')
def resources():
    try:
        tpl_name = 'resources.tpl'
        cwd = os.getcwd()
        os.chdir(TPL_DIR)
        if not os.path.isfile(tpl_name):
            return "Error"
        tpl = SimpleTemplate(source=open(tpl_name).read())
        return tpl.render(page_name='resources', links=LINKS)
    except Exception as exc:
        return str(exc)
    finally:
        os.chdir(cwd)
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
