import hashlib
import json
import logging
import os
import shutil
import uuid

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, os.pardir))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
IMAGES_DIR = os.path.join(ROOT_DIR, 'images')

LOGGER = logging.getLogger("csa.datautils")


def setup_logging():
    logger = logging.getLogger('csa')
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(os.path.join(SCRIPT_DIR, os.pardir, 'logs', 'csa.log'))
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def get_farm_json_file(farmname):
    return os.path.join(DATA_DIR, '%s.json' % farmname)


def get_new_farm_content(farmname):
    json_file = get_farm_json_file('new-farm-template')
    content = json.load(open(json_file, 'rb'))
    content['title'] = [farmname.capitalize()]
    return content
#

def get_farm_content(farmname):
    json_file = get_farm_json_file(farmname)
    if os.path.isfile(json_file):
        content = json.load(open(json_file, 'rb'))
    else:
        content = get_new_farm_content(farmname)
    return content


def update_farm_content(farmname, content):
    json_file = get_farm_json_file(farmname)
    LOGGER.info("Updated farm content [%s]" % json_file)
    json.dump(content, open(json_file, 'wb'), indent=4, sort_keys=True)


def get_imgs_dir(farmname):
    return os.path.join(IMAGES_DIR, 'uploads', farmname)


def save_img(farmname, image):
    imgs_dir = get_imgs_dir(farmname)
    dest_path = os.path.join(imgs_dir, os.path.basename(image.filename))
    if not os.path.isfile(dest_path):
        if not os.path.isdir(imgs_dir):
            os.makedirs(imgs_dir)
        LOGGER.info("Uploading image to [%s]" % dest_path)
        dest_file = open(dest_path, 'wb', 1000)
        while True:
            packet = image.file.read(1000)
            if not packet:
                break
            dest_file.write(packet)
        dest_file.close()
    return dest_path


def delete_removed_imgs(farmname, updated_content):
    previous_content = get_farm_content(farmname)
    imgs_to_remove = [x for x in previous_content['images'] if x not in updated_content['images']]
    for img in imgs_to_remove:
        abs_path = os.path.join(ROOT_DIR, img)
        if os.path.isfile(abs_path):
            os.remove(abs_path)
            LOGGER.info("Deleted img removed from farm profile [%s]" % abs_path)
        else:
            LOGGER.info("Removed img [%s] not on disk so did not not" % img)


def get_permissions_dict():
    return json.load(open(os.path.join(DATA_DIR, 'permissions.json'), 'rb'))


def update_permissions_dict(permissions_dict):
    LOGGER.info("Updated permissions database")
    json.dump(permissions_dict, open(os.path.join(DATA_DIR, 'permissions.json'), 'wb'), indent=4, sort_keys=True)


def _add_unique(entry, existing_list):
    existing_set = set(existing_list)
    existing_set.add(entry)
    return list(existing_set)


def delete_user(user, role, permissions_dict):
    permissions_dict[role].remove(user)
    permissions_dict['hashed_passwords'].pop(user)
    permissions_dict['password_salts'].pop(user)


def add_user(user, role, permissions_dict):
    permissions_dict[role] = _add_unique(user, permissions_dict[role])
    salt = make_salt()
    hash = get_hash("csa", salt)
    permissions_dict['hashed_passwords'][user] = hash
    permissions_dict['password_salts'][user] = salt
    if role == 'editor':
        permissions_dict['permissions'][user] = ''


def delete_farm(farm, permissions_dict):
    permissions_dict['farms'].remove(farm)
    for editor in permissions_dict['permissions']:
        if permissions_dict['permissions'][editor] == farm:
            permissions_dict['permissions'][editor] = ''
    imgs_dir = get_imgs_dir(farm)
    shutil.rmtree(imgs_dir)
    LOGGER.critical("Deleted imgs dir [%s] for farm [%s]" % (imgs_dir, farm))
    json_file = get_farm_json_file(farm)
    if os.path.isfile(json_file):
        os.remove(json_file)
        LOGGER.critical("Deleted dict [%s] for farm [%s]" % (json_file, farm))
    else:
        LOGGER.info("Dict [%s] for farm [%s] not on disk so did not delete" % (json_file, farm))


def add_farm(farm, permissions_dict):
    permissions_dict['farms'] = _add_unique(farm, permissions_dict['farms'])


def make_salt():
    return uuid.uuid4().hex


def get_hash(password, salt):
    input = password + salt
    hash = hashlib.md5(input.encode())
    return hash.hexdigest()


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
                LOGGER.debug("User [%s] hash mismatch [%s]!=[%s]" % (username, hash, permissions_dict['hashed_passwords'][username]))
        else:
            LOGGER.debug("User [%s] not in db" % username)
    return False


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
