#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cgi
from collections import OrderedDict
import json
import os
import time
import uuid

# Use cgitb.handler() under an except block
# Ref: http://cgi.tutorial.codepoint.net/debugging
import cgitb
cgitb.enable()

import bottle
from bottle import route, get, post, run, request, response, template, SimpleTemplate, static_file, url, redirect
from beaker.middleware import SessionMiddleware

SESSION_OPTS = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
APP = SessionMiddleware(bottle.app(), SESSION_OPTS)

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

@route('/testbeaker')
def test():
    try:
        # import inspect
        # foo = str(dir(inspect))
        # from inspect import signature as func_signature
        # import funcsigs
        # from beaker.middleware import SessionMiddleware
        
        s = bottle.request.environ.get('beaker.session')
        s['test'] = s.get('test', 0) + 1
        s.save()
        return 'Test counter: %d' % s['test']
    except Exception as exc:
        return str(exc)


@post('/farmprofiles-beta')
def farmprofiles_beta_post():
    try:

        
        cwd = os.getcwd()
        
        import cgi
        form = cgi.FieldStorage() # instantiate only once!
        name = form.getfirst('name', 'no name')

        # Avoid script injection escaping the user input
        name = cgi.escape(name)
        
        
        bottle.request.set_cookie('name', name)

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
        tpl = SimpleTemplate(source=open(tpl_name).read()) # TODO pass in links nad id(for flash messages)
        return tpl.render(page_name='farmprofiles-beta', links=LINKS)
            
    except Exception as exc:
        return str(exc)
    finally:
        os.chdir(cwd)
#

"""
Utilities
"""
def get_new_farm_content():
    return OrderedDict([
        ("title", ""),
        ("image", ""),
        ("desc", []),
        ("info", OrderedDict([
            ("Website", ""),
            ("Email", ""),
            ("Address", []),
            ("Farmers", [])
        ])),
    ])
#

"""
Session
"""
def get_session():
    return bottle.request.environ.get('beaker.session')


def write_to_session(key, value):
    s = get_session()
    s[key] = value
    s.save()
    return value


def read_from_session(key, type="str"):
    s = get_session()
    if type == "int":
        return s.get(key, 0)
    return s.get(key, "")


"""
Rendering
"""
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
    s = get_session()
    flash_messages_str = s.get("flash-messages", "")
    s['flash-messages'] = ""
    s.save()
    debug_msg("going to render messages: " + flash_messages_str)
    return flash_messages_str.split("$")
#

def flash_message(msg):
    s = get_session()
    flash_messages_str = read_from_session("flash-messages")
    if flash_messages_str:
        flash_messages_str += '$' + msg
    else:
        flash_messages_str = msg
    debug_msg("flash msgs are: " + flash_messages_str)
    write_to_session("flash-messages", flash_messages_str)
#

def flash_debug(msg):  # TODO delete
    return flash_message(msg)
#

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
        
        s = bottle.request.environ.get('beaker.session')
        s['test'] = s.get('test', 0) + 1
        s.save()
        counter = s['test']
        
        
        kwargs.update({'page_name': name, 'links': LINKS, 'flash_messages': get_flash_messages(), 'counter': counter})
        return tpl.render(**kwargs)
    finally:
        os.chdir(cwd)
    
    
#


"""
Very simple authentication
"""
def get_id():
    id = read_from_session("id")
    if not id:
        id = str(uuid.uuid4())
        write_to_session("id", id)
        flash_message("new id:" + id)
    else:
        flash_message("old id:" + id)
    return id
#

def write_login(id, username, login_time):
    """
    """
    cwd = os.getcwd()
    try:
        os.chdir(TMP_DIR)
        expiry_time = login_time + (60 * 60 * 24)
        filename = 'login_%s.txt' % username
        fd = open(filename, 'w')  # Overwrite for this username
        fd.write('username=%s&id=%s&expiry=%s' % (username, id, expiry_time))
        flash_debug('wrote auth info to %s' % filename)
        fd.close()
    finally:
        os.chdir(cwd)
#

def delete_login(username):
    cwd = os.getcwd()
    try:
        os.chdir(TMP_DIR)
        filename = 'login_%s.txt' % username
        if os.path.isfile(filename):
            os.remove(filename)
    finally:
        os.chdir(cwd)
#

def check_user():
    username = read_from_session("username")
    id = get_id()
    filename = 'login_%s.txt' % username
    cwd = os.getcwd()
    try:
        os.chdir(TMP_DIR)
        if os.path.isfile(filename):
            vals = open(filename, 'r').read().split('&')
            if vals[1].startswith('id=') and vals[1][3:] == id:
                if vals[2].startswith('expiry='):
                    expiry_time = int(vals[2][7:])
                    current_time = int(time.time())
                    if current_time < expiry_time:
                        debug_msg("Logged in as <b>%s</b>" % username)
                        flash_message("Logged in as <b>%s</b>" % username)
                        return True
                    else:
                        debug_msg("Session has expired")
                        flash_message("Session has expired")
    except Exception as exc:
        debug_msg("exp checking user: %s" % exc)
        flash_debug("exp checking user: %s" % exc)
        return False
    finally:
        os.chdir(cwd)
    if username:
        debug_msg("Authentication for <b>%s</b> %s failed" % (username, id))  # TODO
        flash_debug("Authentication for <b>%s</b> %s failed" % (username, id))  # TODO
    return False
#

def authenticate(username, password):
    """
    Authenticate given username and password against database.
    Returns:
        (str) Type of user.
    """
    db = {
        "admin": {"pw": "admin", "role": "admin"},
        "cloughjordan": {"pw": "cloughjordan", "role": "editor", "farm": "cloughjordan"},
        "declan": {"pw": "declan", "role": "editor", "farm": "dublin"}
    }
    if username and password:
        if username in db and password == db[username]["pw"]:
            role = db[username].get("role", "editor")
            farms = []
            if role == "admin":
                for name in db:
                    if "farm" in db[name]:
                        farms.append(db[name]["farm"])
            else:
                if "farm" in db[username]:
                    farms.append(db[username]["farm"])
            id = str(uuid.uuid4())
            
            s = get_session()
            s['username'] = username
            s['role'] = role
            s['farms'] = "+".join(farms)
            s['id'] = id
            s.save()

            write_login(id, username, int(time.time()))
            return db[username]
    return None
#

def signout():
    s = get_session()
    username = s.get("username", "")
    if username:
        flash_message("Signed out %s" % username)
    s['username'] = ""
    s['role'] = ""
    s['farms'] = ""


# Ref: http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not check_user():
            debug_msg("check failed so redirecting")
            flash_message("check failed so redirecting")
            redirect('/Development20180422_frameworks/login')
        debug_msg("check was ok")
        flash_message("check was ok")
        return f(*args, **kwargs)
    return decorated_function
#

"""
TODO: hopefully dont need these

Redirect results in a new Python process being spawned, thus disabling the simple message
flash functionality put in place. To avoid this, functions to render are content are split
out into separate functions, and these called directly instead of redirecting.
"""

def render_login():
    """
    Render login page, useful when login fails, etc.
    
    Avoids another request to server, which allows flash message to be displayed.
    """
    return render_template('login')
    # try:
        # tpl_name = 'login.tpl'
        # cwd = os.getcwd()
        # os.chdir(TPL_DIR)
        
        # if not os.path.isfile(tpl_name):
            # return "Error"
        # tpl = SimpleTemplate(source=open(tpl_name).read())
        # return tpl.render(page_name='login', links=LINKS)
    # except Exception as exc:
        # return str(exc)
    # finally:
        # os.chdir(cwd)

def render_editfarm(farmname):
    cwd = os.getcwd()
    try:
        os.chdir(DATA_DIR)
        json_file = os.path.join(DATA_DIR, '%s.json' % farmname)
        if os.path.isfile(json_file):
            content = json.load(open(json_file, 'rb'))
        else:
            content = get_new_farm_content()
        instructions = json.load(open(os.path.join(DATA_DIR, 'instructions.json'), 'rb'))
        return render_template('editfarm', {'content': content, 'instructions': instructions})
    except Exception as exc:
        return str(exc)
    finally:
        os.chdir(cwd)

    # try:
        # cwd = os.getcwd()
        # os.chdir(TPL_DIR)
        # data_dir = os.path.join(os.pardir, 'data')
        
        # json_file = os.path.join(data_dir, '%s.json' % farmname)
        # if os.path.isfile(json_file):
            # content = json.load(open(json_file, 'rb'))
        # else:
            # content = get_new_farm_content()
        
        # instructions = json.load(open(os.path.join(data_dir, 'instructions.json'), 'rb'))
        
        # tpl = SimpleTemplate(source=open('editfarm.tpl').read())
        # return tpl.render(page_name='editfarm', links=LINKS, content=content, instructions=instructions)
    # except Exception as exc:
        # return str(exc)
    # finally:
        # os.chdir(cwd)
#

def render_admin():
    # debug_msg("farms cookie is: '%s'" % bottle.request.get_cookie('farms', ''))
    # debug_msg("role cookie is: '%s'" % bottle.request.get_cookie('profile', ''))
    # debug_msg("username cookie is: '%s'" % bottle.request.get_cookie('username', ''))
    # debug_msg("id cookie is: '%s'" % bottle.request.get_cookie('id', ''))
    # debug_msg("msgs cookie is: '%s'" % bottle.request.get_cookie('msgs', ''))
    
    # debug_msg("farms cookie is: '%s'" % read_from_session("farms"))
    # debug_msg("role cookie is: '%s'" % read_from_session("role"))
    # debug_msg("username cookie is: '%s'" % read_from_session("username"))
    # debug_msg("id cookie is: '%s'" % read_from_session("id"))
    # debug_msg("flash-messages cookie is: '%s'" % read_from_session("flash-messages"))
    
    farms = read_from_session('farms').split('+')
    return render_template('admin', farms=farms)
    # try:
        # cwd = os.getcwd()
        # os.chdir(TPL_DIR)
        
        # username = bottle.request.get_cookie('username', '')
        # role = bottle.request.get_cookie('role', '')
        # farms = bottle.request.get_cookie('farms', '')
        # farms = farms.split("+")
        
        # tpl = SimpleTemplate(source=open('admin.tpl').read())
        # return tpl.render(page_name='admin', links=LINKS, farms=farms)
    # except Exception as exc:
        # return str(exc)
    # finally:
        # os.chdir(cwd)
#


"""
Private
"""

@get('/login')
def login_get():
    return render_login()
#

@post('/login')
def login_post():
    form = cgi.FieldStorage()
    username = cgi.escape(form.getfirst('username', ''))
    password = cgi.escape(form.getfirst('password', ''))
    credentials = authenticate(username, password)
    if credentials:
        if credentials["role"] == "editor":
            flash_message("Logged in as editor for %s" % credentials["farm"])
        else:
            flash_message("Logged in as admin")
        return render_admin()
    flash_message("Incorrect username or password")
    return render_login()
#

@route('/logout')
def logout():
    signout()
    return render_login()
#

@route('/editfarm/<farmname>')
@login_required
def editfarm(farmname):
    return render_editfarm(farmname)
#

@route('/admin')
@login_required
def admin():
    debug_msg("ok to go to admin")
    flash_message("ok to go to admin")
    farms = read_from_session('farms').split('+')
    return render_template('admin', farms=farms)
    # return render_admin()
#

"""
Public
"""

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

bottle.run(app=APP, debug=False, server='cgi')
