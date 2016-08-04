import os
import types
import binascii
from Crypto.Cipher import AES
from Crypto import Random
from clients import ClientManager


class KeystoneManager(object):
    """
    Class for ensuring role assignments in keystone.

    Give it a role assignment, and it will return a user
    that matches your demands. That may include making 
    any missing components (i.e., domain, project, user,
    role) and return back a fresh user. 
    """
    
    def __init__(self):
        """
        This is what holds the decryption keys for the hashes.
        It's really important that this doesn't change during
        a run, or you'll get different outputs.
    
        :param key: The shared key used for 2 way encryption.
        :type key: 16 character length string.
        :param iv: The initialization vector for reversing a hash.
        :type iv: binary number in bytes
        """
        self.__crypto_info = {
            'key': "Sixteen byte key",
            'iv': None #This gets populated on first use.
        }
        
        """
        This is the big map of users. The key is a representation
        of its role assignment (domain, project, role). The value
        is a credentials object.
        """
        self.__users = {}

        """
        These credentials are so that we can create anything we 
        need to in keystone. They must be admin level credentials.
        """
        self.admin_client_manager = self.load_admin_client_manager()
        
    def load_admin_client_manager(self):
        """
        Loads admin credentials from ENV variables
        
        :returns: client.ClientManager
        """
        env_vars_default = {
            'OS_USERNAME': 'admin', 
            'OS_PASSWORD': '', 
            'OS_PROJECT_NAME': 'admin', 
            'OS_AUTH_URL': 'http://127.0.0.1:5000/v3', 
            'OS_USER_DOMAIN_NAME': 'Default', 
            'OS_PROJECT_DOMAIN_NAME': 'Default'}
        env_vars = {
            k[3:].lower(): os.getenv(k, v) 
            for (k,v) in env_vars_default.items()
        }

        return ClientManager(**env_vars)


    def _get_cypher(self):
        """
        Builds a cypher for encryption/decryption
        
        :returns: (Crypto.Cipher.AES, bytes)
        """
        key = self.__crypto_info['key']
        iv = None
        if self.__crypto_info['iv'] == None:
            iv = Random.new().read(AES.block_size)
            self.__crypto_info['iv'] = iv
        else:
            iv = self.__crypto_info['iv']
        return (AES.new(key, AES.MODE_CFB, iv), iv)

    def find_user_credentials(self, domain='', project='Default', role='member'):
        """
        Finds a user that matches your auth needs, creating one if necessary.
        
        :param domain: Keystone domain. Defaults to project's value.
        :type domain: string
        :param project: Keystone project. Default to `Default`
        :type project: string
        :param role: Keystone role. If left empty, will default to member
        :type role: string
        :returns: clients.ClientManager
        """
        if domain == '' or domain == None:
            domain = project
        hash = self._encode_hash(domain, project, role)
        if hash in self.__users.keys():
            return self.__users[hash]
        else:
            self.__users[hash] = self.admin_client_manager
            #TODO: Make this return real users
            return self.__users[hash]
            

    def _encode_hash(self, *args):
        """
        Hashes a list of *args into a single value.
        
        :param: list of strigs to pack
        :type *args: [string]
        :returns: string
        """
        text = '|'.join(args)
        (cipher, iv) = self._get_cypher()
        msg = iv + cipher.encrypt(text)
        return msg.encode('hex')


    def _decode_hash(self, hash):
        """
        Decodes a hashed string created by _encode_hash().
        
        Not really used, but handy to have in case something goes sideways.
        
        :param hash: A hashed list
        :type hash: string
        :returns: string
        """
        (cipher, iv) = self._get_cypher()
        return cipher.decrypt(hash.decode('hex'))[len(iv):].split('|')
        
    def _entity_exists(self, keystone_type, name):
        """
        Checks to see if keystone has a matching record.
        
        :param keystone_type: Keystone resource "project" || "domain" || "role"
        :type keystone_type: string
        :param name: matching name, like `member` for a role
        :type name: string
        :returns: boolean
        """
        ks = self.admin_client_manager.get_keystone()
        return name in [x.name for x in getattr(ks, keystone_type).list()]
        
    def get_keystone_resource(self, keystone_resource_type, name, domain_name=None, project_name=None):
        """
        Gets (or creates and returns) a keystone domain by name.
        
        :param name: Keystone domain name
        :type name: string
        :returns: keystoneclient.v3.domains.Domain
        """

        def build_args(xs, ys, all={}):
            """
            Compiles a struct of args passed into keystone clients
            
            Each keystone type takes the parent types as options
            to create(). Thus user has one more options than project,
            and project one more than domain.
            
            :param xs: keystone entities to be searched.
            :type xs: ['domain', 'project', 'user]
            :param ys: the args from this function. Order is key.
            :type ys: [string]
            :returns: dict
            """
            if xs == []:
                return all
            else:
                all[xs[-1]] = ys
                return build_args_list(xs[:-1], ys[:-1], all)
                
        desc = "testing %s" % keystone_resource_type
        xs = ['domain', 'project', 'user']
        ys = [name, desc, domain_name, project_name]
        all_args = build_args(xs, ys)
        
        ks = self.admin_client_manager.get_keystone()
        

        """
        keystone clients are all plural, like `domains` and `users`.
        """
        resources = getattr(ks, "%ss" % keystone_resource_type)

        entity_exists = lambda name: name in [x.name for x in resources.list()]

        if entity_exists(name) == False:
            my_args = all_args[keystone_resource_type]
            return resources.create(*my_args)
        else:
            return [resources.get(x.id) 
                for x in resources.list() 
                if x.name == name][0]

