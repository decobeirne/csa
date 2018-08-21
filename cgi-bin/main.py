#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cgi
import datetime
from collections import OrderedDict
import json
import os

import bottle
from bottle import route, get, post, run, request, response, template, SimpleTemplate, static_file, url, redirect

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
        debug_msg("flash_message 1")
        debug_msg("bottle.request.cookies: %s" % str(bottle.request.cookies.__dict__))
        debug_msg("bottle.response._cookies: %s" % str(bottle.response._cookies))
        debug_msg("\n")
    
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
            debug_msg("flash_message 2")
            debug_msg("bottle.request.cookies: %s" % str(bottle.request.cookies.__dict__))
            debug_msg("bottle.response._cookies: %s" % str(bottle.response._cookies))
            debug_msg("\n")
            
    if not written:
        bottle.response.set_cookie('flash', msg, path='/')
        bottle.response.set_cookie('foo', 'bar', path='/')
        debug_msg("flash_message 3")
        debug_msg("bottle.request.cookies: %s" % str(bottle.request.cookies.__dict__))
        debug_msg("bottle.response._cookies: %s" % str(bottle.response.__dict__))
        debug_msg("bottle.response._cookies: %s" % type(bottle.response._cookies))
        debug_msg("bottle.response._cookies: %s" % str(bottle.response._cookies))
        debug_msg("\n")


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
        
        # debug_msg("username %s role %s farmname %s" % (username, role, farmname))
        
        kwargs.update(
            {'page_name': name,
             'links': LINKS,
             'messages_to_flash': get_flash_messages(),  # Retrieve and wipe flash messages
             #'messages_to_flash': ["temp"],  # Retrieve and wipe flash messages
             'username': username,
             'role': role,
             'farmname': farmname})  
        return tpl.render(**kwargs)
    finally:
        os.chdir(cwd)


@route('/')
@route('/home')
def home():
    return render_template('home')
    # try:
        # tpl_name = 'home.tpl'
        # cwd = os.getcwd()
        # os.chdir(TPL_DIR)
        # if not os.path.isfile(tpl_name):
            # return "Error"
        # tpl = SimpleTemplate(source=open(tpl_name).read())
        # return tpl.render(page_name='home', links=LINKS)
    # except Exception as exc:
        # return str(exc)
    # finally:
        # os.chdir(cwd)
#

@route('/about')
def about():
    return render_template('about')
    # try:
        # tpl_name = 'about.tpl'
        # cwd = os.getcwd()
        # os.chdir(TPL_DIR)
        # if not os.path.isfile(tpl_name):
            # return "Error"
        # tpl = SimpleTemplate(source=open(tpl_name).read())
        # return tpl.render(page_name='about', links=LINKS)
    # except Exception as exc:
        # return str(exc)
    # finally:
        # os.chdir(cwd)
#

@route('/farmprofiles')
def farmprofiles():
    return render_template('farmprofiles')
    # try:
        # tpl_name = 'farmprofiles.tpl'
        # cwd = os.getcwd()
        # os.chdir(TPL_DIR)
        # if not os.path.isfile(tpl_name):
            # return "Error"
        # tpl = SimpleTemplate(source=open(tpl_name).read())
        # return tpl.render(page_name='farmprofiles', links=LINKS)
    # except Exception as exc:
        # return str(exc)
    # finally:
        # os.chdir(cwd)
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
        
        
        bottle.response.set_cookie('name', name)

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
    debug_msg("login get")
    debug_msg("bottle.request.cookies: %s" % str(bottle.request.cookies.__dict__))
    debug_msg("bottle.response._cookies: %s" % str(bottle.response._cookies))
    debug_msg("\n")
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
    debug_msg("clear_session \n\n")
    bottle.response.set_cookie('farmname', '', path='/')
    bottle.response.set_cookie('username', '', path='/')
    bottle.response.set_cookie('role', '', path='/')
    # bottle.response.set_cookie('farmname', '')
    # bottle.response.set_cookie('username', '')
    # bottle.response.set_cookie('role', '')
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
                # Set cookie path
                # https://stackoverflow.com/questions/21215904/read-cookie-text-value-in-a-python-bottle-application
                bottle.response.set_cookie('farmname', 'cloughjordan', path='/')  # todo temp
                bottle.response.set_cookie('username', username, path='/')
                bottle.response.set_cookie('role', role, path='/')
                
                debug_msg("authenticate %s %s\n\n" % (username, password))
                return role
    clear_session()
    return None
#

@post('/login')
def login_post():
    debug_msg("login post 1")
    debug_msg("bottle.request.cookies: %s" % str(bottle.request.cookies.__dict__))
    debug_msg("bottle.response._cookies: %s" % str(bottle.response._cookies))
    debug_msg("\n")
    clear_session()
    form = cgi.FieldStorage()
    username = cgi.escape(form.getfirst('username', ''))
    password = cgi.escape(form.getfirst('password', ''))
    flash_message("Authenticating user <b>%s</b>" % (username))
    bottle.response.set_cookie('foo2', 'bar2', path='/')
    role = authenticate(username, password)
    bottle.response.set_cookie('foo3', 'bar3', path='/')
    debug_msg("login post 2")
    debug_msg("bottle.request.cookies: %s" % str(bottle.request.cookies.__dict__))
    debug_msg("bottle.response._cookies: %s" % str(bottle.response._cookies))
    debug_msg("\n")
    if role in ['admin', 'editor']:
        auth_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        #flash_message("Authenticated user <b>%s</b> on %s" % (username, auth_time))
        if role == 'admin':
            redirect('/Development20180422_frameworks/admin')
        else:
            redirect('/Development20180422_frameworks/editfarm')
    debug_msg("login post 3")
    debug_msg("bottle.request.cookies: %s" % str(bottle.request.cookies.__dict__))
    debug_msg("bottle.response._cookies: %s" % str(bottle.response._cookies))
    debug_msg("\n")
    #flash_message("Authentication for user <b>%s</b> failed. Please contact admin to reset your password." % username)
    return render_template("login")
#

@route('/logout')
def logout():
    debug_msg("logout1")
    debug_msg("bottle.request.cookies: %s" % str(bottle.request.cookies.__dict__))
    debug_msg("bottle.response._cookies: %s" % str(bottle.response._cookies))
    debug_msg("\n")
    username = request.get_cookie('username', None)
    clear_session()
    if username:
        #flash_message("Signed out user <b>%s</b>" % username)
        pass
    debug_msg("logout2")
    debug_msg("bottle.request.cookies: %s" % str(bottle.request.cookies.__dict__))
    debug_msg("bottle.response._cookies: %s" % str(bottle.response._cookies))
    debug_msg("\n")
    redirect('/Development20180422_frameworks/login')
#

# Ref: http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
from functools import wraps

def farm_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = request.get_cookie('username', None)
        role = request.get_cookie('role', None)
        
        debug_msg("farm_login_required")
        debug_msg("bottle.request.cookies: %s" % str(bottle.request.cookies.__dict__))
        debug_msg("bottle.response._cookies: %s" % str(bottle.response._cookies))
        debug_msg("\n")
        
        
        if username and role == 'admin':
            #flash_message("Redirected. Do not have permission to edit farm profile.")
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
        username = request.get_cookie('username', None)
        role = request.get_cookie('role', None)
        
        debug_msg("admin_login_required")
        debug_msg("bottle.request.cookies: %s" % str(bottle.request.cookies.__dict__))
        debug_msg("bottle.response._cookies: %s" % str(bottle.response._cookies))
        debug_msg("\n")
        
        if username and role == 'editor':
            #flash_message("Redirected. Do not have access to admin page.")
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

@route('/editfarm')
@farm_login_required
def editfarm():
    debug_msg("editfarm")
    debug_msg("bottle.request.cookies: %s" % str(bottle.request.cookies.__dict__))
    debug_msg("bottle.response._cookies: %s" % str(bottle.response._cookies))
    debug_msg("\n")
    farmname = request.get_cookie('farmname')
    username = request.get_cookie('username')
    role = request.get_cookie('role')
    json_file = os.path.join(DATA_DIR, '%s.json' % farmname)
    if os.path.isfile(json_file):
        content = json.load(open(json_file, 'rb'))
    else:
        content = get_new_farm_content()
    instructions = json.load(open(os.path.join(DATA_DIR, 'instructions.json'), 'rb'))
    return render_template('editfarm', farmname=farmname, username=username, role=role, content=content, instructions=instructions)
#

@route('/admin')
@admin_login_required
def admin():
    debug_msg("admin")
    debug_msg("bottle.request.cookies: %s" % str(bottle.request.cookies.__dict__))
    debug_msg("bottle.response._cookies: %s" % str(bottle.response._cookies))
    debug_msg("\n")
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
    # try:
        
        # username = request.get_cookie('username', '')
        
        # import pprint
        # data = pprint.pformat(request.environ)
        
        
        # cwd = os.getcwd()
        # os.chdir(TPL_DIR)
        
        # tpl = SimpleTemplate(source=open('admin.tpl').read())
        # return tpl.render(page_name='admin', links=LINKS, user=username, data=data)
            
    # except Exception as exc:
        # return str(exc)
    # finally:
        # os.chdir(cwd)
#

@route('/contact')
def contact():
    return render_template('contact')
    # try:
        # tpl_name = 'contact.tpl'
        # cwd = os.getcwd()
        # os.chdir(TPL_DIR)
        # if not os.path.isfile(tpl_name):
            # return "Error"
        # tpl = SimpleTemplate(source=open(tpl_name).read())
        # return tpl.render(page_name='contact', links=LINKS)
    # except Exception as exc:
        # return str(exc)
    # finally:
        # os.chdir(cwd)
#

@route('/resources')
def resources():
    return render_template('resources')
    # try:
        # tpl_name = 'resources.tpl'
        # cwd = os.getcwd()
        # os.chdir(TPL_DIR)
        # if not os.path.isfile(tpl_name):
            # return "Error"
        # tpl = SimpleTemplate(source=open(tpl_name).read())
        # return tpl.render(page_name='resources', links=LINKS)
    # except Exception as exc:
        # return str(exc)
    # finally:
        # os.chdir(cwd)
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
