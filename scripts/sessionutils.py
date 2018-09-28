import bottle
from collections import OrderedDict
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TPL_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, os.pardir, 'templates'))

LINKS = OrderedDict([
    ('About', {'link': 'about'}),
    ('Farm Profiles', {'link': 'farms'}),
    ('Resources', {'link': 'resources'}),
    ('Contact', {'link': 'contact'}),
    ('Facebook', {'link': 'https://www.facebook.com/groups/245019725582313', 'tags': 'target="_blank"'}),
    ])

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
    bottle.response.set_cookie('flash', "", path='/')
    msgs = ["<i class='fa fa-exclamation-circle'></i> %s" % x for x in msg.split('$') if x != '']
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
        tpl = bottle.SimpleTemplate(source=open(name + '.tpl').read(), lookup=['.'])
        username_cookie = bottle.request.get_cookie('username')
        role_cookie = bottle.request.get_cookie('role')
        farmname_cookie = bottle.request.get_cookie('farmname')
        root_rel_dir = '../' * (bottle.request.path.count('/') - 1) # E.g. '/foo' == 0 == '', '/foo/bar' == 1 == '../'
        kwargs.update(
            {'page_name': name,
             'links': LINKS,
             'messages_to_flash': get_flash_messages(),  # Retrieve and wipe flash messages
             'username_cookie': username_cookie,
             'role_cookie': role_cookie,
             'farmname_cookie': farmname_cookie,
             'root_rel_dir': root_rel_dir})
        return tpl.render(**kwargs)
    finally:
        os.chdir(cwd)

def clear_session():
    bottle.response.set_cookie('farmname', '', path='/')
    bottle.response.set_cookie('username', '', path='/')
    bottle.response.set_cookie('role', '', path='/')
#

def setup_session(username, role, farmname):
    bottle.response.set_cookie('username', username, path='/')
    bottle.response.set_cookie('role', role, path='/')
    bottle.response.set_cookie('farmname', farmname, path='/')
#



