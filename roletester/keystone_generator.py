"""
Module for ensuring role assignments in keystone.

Give it a role assignment, and it will return a user
that matches your demands. That may include making 
any missing components (i.e., domain, project, user,
role) and return back a fresh user. 

"""

import os
import types
import binascii
from Crypto.Cipher import AES
from Crypto import Random
from clients import ClientManager

"""
This is what holds the decryption keys for the hashes.
It's really important that this doesn't change during
a run, or you'll get different outputs.
    
:param key: The shared key used for 2 way encryption.
:type key: 16 character length string.
:param iv: The initialization vector for reversing a hash.
:type iv: binary number in bytes
"""
crypto_info = {
    'key': "Sixteen byte key",
    'iv': None #This gets populated on first use.
}

"""
This is the big map of users. The key is a representation
of its role assignment (domain, project, role). The value
is a credentials object.
"""
users = {}

def load_admin_creds():
    """
    Loads admin credentials from ENV variables
    
    :returns: client.ClientManager
    """
    env_vars_default = {
        'OS_USERNAME': 'admin', 
        'OS_PASSWORD': '', 
        'OS_PROJECT_NAME': 'admin', 
        'OS_TENANT_NAME': 'admin', 
        'OS_AUTH_URL': 'http://127.0.0.1:5000/v3', 
        'OS_USER_DOMAIN_NAME': 'Default', 
        'OS_PROJECT_DOMAIN_NAME': 'Default'}
    env_vars = {
        k[3:].lower(): os.getenv(k, v) 
        for (k,v) in env_vars_default.items()
    }

    # Currently, openrc doesn't quite expose everything
    env_vars['project_id'] = env_vars['project_name']

    client = ClientManager(**env_vars)
    return client
    

def _get_cypher():
    """
    Builds a cypher for encryption/decryption
    
    :returns: (Crypto.Cipher.AES, bytes)
    """
    key = crypto_info['key']
    iv = None
    if crypto_info['iv'] == None:
        iv = Random.new().read(AES.block_size)
        crypto_info['iv'] = iv
    else:
        iv = crypto_info['iv']
    return (AES.new(key, AES.MODE_CFB, iv), iv)

def find_user(domain='', project='Default', role='member'):
    """
    Finds a user that matches your auth needs, creating one if necessary.
    
    :param domain: Keystone domain. If left empty, will default to project's value.
    :type domain: string
    :param project: Keystone project. If left empty, will default to `Default`
    :type project: string
    :param role: Keystone role. If left empty, will default to member
    :type role: string
    :returns: TODO: Figure out wtf is getting returned
    """
    if domain == '' or domain == None:
        domain = project
    hash = _encode_hash(domain, project, role)
    if hash in users.keys():
        return users[hash]
    else:
        users[hash] = "BOB"
        return users[hash]


def _encode_hash(*args):
    """
    Hashes a list of *args into a single value.
    
    :param: list of strigs to pack
    :type *args: [string]
    :returns: string
    """
    text = '|'.join(args)
    (cipher, iv) = _get_cypher()
    msg = iv + cipher.encrypt(text)
    return msg.encode('hex')

def _decode_hash(hash):
    """
    Decodes a hashed string created by _encode_hash()
    
    :param hash: A hashed list
    :type hash: string
    
    :returns: string
    """
    (cipher, iv) = _get_cypher()
    return cipher.decrypt(hash.decode('hex'))[len(iv):].split('|')
    

client = load_admin_creds()
ks = client.get_keystone()
