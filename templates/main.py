#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from collections import OrderedDict

import cgi

# Use cgitb.handler() under an except block
# Ref: http://cgi.tutorial.codepoint.net/debugging
import cgitb
cgitb.enable()

import bottle
from bottle import route, get, post, run, request, response, template, SimpleTemplate, static_file, url, redirect

ROOT_DIR = '../httpdocs/communitysupportedagriculture.ie/Development20180422_frameworks'
TPL_DIR = ROOT_DIR + '/templates'
IMAGES_DIR = ROOT_DIR + '/images'
STATIC_DIR = ROOT_DIR + '/static'


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

@get('/login')
def login_get():
    try:
            
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
#

# Ref: https://stackoverflow.com/questions/36269485/how-do-i-pass-through-the-next-url-with-flask-and-flask-login
@post('/login')
def login_post():
    
    
    form = cgi.FieldStorage()
    username = cgi.escape(form.getfirst('username', ''))
    password = cgi.escape(form.getfirst('password', ''))
    if username and password:
        if username == 'deco' and password == 'password':  # Todo
            
            response.set_cookie('username', username)
            
            return redirect('/Development20180422_frameworks/admin')
    
    try:
            
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
    
    
#


@route('/logout')
def logout():
    return "hello"
    # request.delete_cookie('username')
    # redirect('/Development20180422_frameworks/home')
#






# Ref: http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        username = request.get_cookie('username', None)
        if not username:
            # redirect(url('login', next=request.url))
            redirect('/Development20180422_frameworks/login')
        return f(*args, **kwargs)
    return decorated_function



@route('/admin')
@login_required
def admin():
    try:
        
        username = request.get_cookie('username', '')
        
        import pprint
        data = pprint.pformat(request.environ)
        
        
        tpl_name = 'admin.tpl'
        cwd = os.getcwd()
        os.chdir(TPL_DIR)
        
        if not os.path.isfile(tpl_name):
            return "Error"
        tpl = SimpleTemplate(source=open(tpl_name).read())
        return tpl.render(page_name='admin', links=LINKS, user=username, data=data)
            
    except Exception as exc:
        return str(exc)
    finally:
        os.chdir(cwd)
#

# @route('/farmprofiles-beta', method=['GET', 'POST'], name='farmprofiles-beta')
# @route('farmprofiles-beta/<foo>', method=['GET', 'POST'], name='farmprofiles-beta')
# # @route('/farmprofiles-beta')
# def farmprofiles_beta(foo=None):
    # try:
        # if request.method == 'POST':
        
            # import cgi
            # form = cgi.FieldStorage() # instantiate only once!
            # name = form.getfirst('name', 'empty')

            # # Avoid script injection escaping the user input
            # name = cgi.escape(name)

            # return """\
            # Content-Type: text/html\n
            # <html><body>
            # <p>The submitted name was "%s"</p>
            # </body></html>
            # """ % name
        
        # else:
            
            # tpl_name = 'farmprofiles-beta.tpl'
            # cwd = os.getcwd()
            # os.chdir(TPL_DIR)
            
            # if not os.path.isfile(tpl_name):
                # return "Error"
            # tpl = SimpleTemplate(source=open(tpl_name).read())
            # return tpl.render(page_name='farmprofiles-beta', links=LINKS)
            
    # except Exception as exc:
        # return str(exc)
    # finally:
        # os.chdir(cwd)
# #

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
