import hashlib
import json
import logging
import os
import uuid

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, os.pardir, 'data'))

LOGGER = logging.getLogger("csa.datautils")


def setup_logging():
    logger = logging.getLogger('csa')
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(os.path.join(SCRIPT_DIR, os.pardir, 'logs', 'csa.log'))
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
#

def get_farm_json_file(farmname):
    return os.path.join(DATA_DIR, '%s.json' % farmname)
#

def get_new_farm_content():
    json_file = get_farm_json_file('new-farm')
    return json.load(open(json_file, 'rb'))
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
    LOGGER.info("Updated farm content %s" % json_file)
    json.dump(content, open(json_file, 'wb'))
#

def get_permissions_dict():
    return json.load(open(os.path.join(DATA_DIR, 'permissions.json'), 'rb'))
#

def update_permissions_dict(permissions_dict):
    LOGGER.info("Updated permissions database")
    json.dump(permissions_dict, open(os.path.join(DATA_DIR, 'permissions.json'), 'wb'))
#

def delete_user(user, role, permissions_dict):
    permissions_dict[role].remove(user)
    permissions_dict['hashed_passwords'].pop(user)
    permissions_dict['password_salts'].pop(user)
#

def _add_unique(entry, existing_list):
    existing_set = set(existing_list)
    existing_set.add(entry)
    return list(existing_set)
#

def add_user(user, role, permissions_dict):
    permissions_dict[role] = _add_unique(user, permissions_dict[role])
    salt = make_salt()
    hash = get_hash("csa", salt)
    permissions_dict['hashed_passwords'][user] = hash
    permissions_dict['password_salts'][user] = salt
#

def make_salt():
    return uuid.uuid4().hex
#

def get_hash(password, salt):
    input = password + salt
    hash = hashlib.md5(input.encode())
    return hash.hexdigest()
#

def check_password(username, password):
    """
    Compare the password entered by the user against the hashed password stored in the database.
    Returns:
        (bool) Whether the password is ok.
    """
    if username and password:
        permissions_dict = get_permissions_dict()
        if ((username in permissions_dict['admins'] or username in permissions_dict['editors']) and
            username in permissions_dict['password_salts'] and
            username in permissions_dict['hashed_passwords']):
            salt = permissions_dict['password_salts'][username]
            hash = get_hash(password, salt)
            if hash == permissions_dict['hashed_passwords'][username]:
                return True
            else:
                LOGGER.debug("User '%s' hash mismatch '%s'!='%s'" % (username, hash, permissions_dict['hashed_passwords'][username]))
        else:
            LOGGER.debug("User '%s' not in db" % username)
    return False
#

def get_permissions(username):
    """
    Get user role and farm for which they have permission to edit. If role is admin, farm is "all".
    Otherwise the user may have no permissions currently, so farm is "".
    Returns:
        (tuple[str, str]) Role and farm for this user.
    """
    permissions_dict = get_permissions_dict()
    role = 'admin' if username in permissions_dict['admins'] else 'editor' if username in permissions_dict['editors'] else ''
    farm = 'all' if role == 'admin' else permissions_dict['permissions'].get(username, '')
    return (role, farm)
#