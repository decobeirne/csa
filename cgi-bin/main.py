#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cgi
from collections import OrderedDict
import json
import os

# Use cgitb.handler() under an except block
# Ref: http://cgi.tutorial.codepoint.net/debugging
# import cgitb
# cgitb.enable()

import bottle
from bottle import route, get, post, run, request, response, template, SimpleTemplate, static_file, url, redirect


ROOT_DIR = '../httpdocs/communitysupportedagriculture.ie/Development20180422_frameworks'
TPL_DIR = ROOT_DIR + '/templates'
IMAGES_DIR = ROOT_DIR + '/images'
STATIC_DIR = ROOT_DIR + '/static'
TMP_DIR = ROOT_DIR + '/tmp'

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

def render_login():
    """
    Render login page, useful when login fails, etc.
    
    Avoids another request to server, which allows flash message to be displayed.
    """
    try:
        #flash_message("deco flash2")
        tpl_name = 'login.tpl'
        cwd = os.getcwd()
        os.chdir(TPL_DIR)
        
        if not os.path.isfile(tpl_name):
            return "Error"
        tpl = SimpleTemplate(source=open(tpl_name).read())
        return tpl.render(page_name='login', links=LINKS)
    except Exception as exc:
        return str(exc)
    finally:
        os.chdir(cwd)

@get('/login')
def login_get():
    return render_login()
#

def authenticate(username, password):
    """
    Authenticate given username and password against database.
    Returns:
        (str) Type of user.
    """
    if username and password:
        if username == 'deco' and password == 'password':
            return 'admin'
    # flash_message("Incorrect username or password")
    return None
#

@post('/login')
def login_post():
    form = cgi.FieldStorage()
    username = cgi.escape(form.getfirst('username', ''))
    password = cgi.escape(form.getfirst('password', ''))
    role = authenticate(username, password)
    if role == 'admin':  # todo
        bottle.response.set_cookie('farmname', 'cloughjordan')  # todo temp
        bottle.response.set_cookie('username', username)
        bottle.response.set_cookie('role', role)
        # flash_message("login admin")
        redirect('/Development20180422_frameworks/editfarm')
    elif role == 'editor':
        bottle.response.set_cookie('farmname', 'cloughjordan')
        bottle.response.set_cookie('username', username)
        bottle.response.set_cookie('role', role)
        # flash_message("login editor")
        redirect('/Development20180422_frameworks/editfarm')
    # flash_message("login fail")
    return render_login()
#


@route('/logout')
def logout():
    bottle.response.delete_cookie('username')
    bottle.response.delete_cookie('role')
    import sys
    # flash_message(sys.version)
    return render_login()
    # redirect('/Development20180422_frameworks/login')
    # return "hello"
#




# Ref: http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = request.get_cookie('username', None)
        if not username:
            return render_login()
        return f(*args, **kwargs)
    return decorated_function
#


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

@route('/editfarm')
@login_required
def editfarm():
    try:
        cwd = os.getcwd()
        os.chdir(TPL_DIR)
        data_dir = os.path.join(os.pardir, 'data')
        
        farmname = request.get_cookie('farmname')
        json_file = os.path.join(data_dir, '%s.json' % farmname)
        if os.path.isfile(json_file):
            content = json.load(open(json_file, 'rb'))
        else:
            content = get_new_farm_content()
        
        instructions = json.load(open(os.path.join(data_dir, 'instructions.json'), 'rb'))
        
        # return str(instructions)
        
        # instructions = {}
        # f0 = os.path.join(DATA_DIR, 'cloughjordan.json')
        # instructions[f0] = os.path.isfile(f0)
        
        # f0 = os.path.join(os.pardir, 'data', 'cloughjordan.json')
        # instructions[f0] = os.path.isfile(f0)
        
        # f0 = os.path.join(os.pardir, 'data')
        # instructions[f0] = os.path.isdir(f0)
        
        # f0 = DATA_DIR
        # instructions[f0] = os.path.isdir(f0)
        
        
        
        tpl = SimpleTemplate(source=open('editfarm.tpl').read())
        return tpl.render(page_name='editfarm', links=LINKS, content=content, instructions=instructions)
        
    except Exception as exc:
        return str(exc)
    finally:
        os.chdir(cwd)
    
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
