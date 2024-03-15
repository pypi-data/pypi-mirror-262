import base64
import datetime
from functools import cache
import hashlib
import os
import typing
import click
from keyrings.cryptfile.cryptfile import CryptFileKeyring
import sprinko.utils as utils
from sprinko.core.__base__ import core_mod, root_mod
import sprinko.core as core
import inspect
import json
from masscodeDriver import Snippet, Tag, AppLoader
from masscodeDriver.utils import FuzzyContext

class SprinkoDescriptor:
    def __get__(self, obj, objtype=None):
        from sprinko.core.sprinko import Sprinko
        return Sprinko

class Ko(metaclass=utils.SingletonMeta):
    __sprinko_des = SprinkoDescriptor()

    def __getattribute__(self, __name: str):
        if __name.startswith("__idcit"):
            return super().__getattribute__(__name)

        stack = inspect.stack()
        if "self" in stack[1].frame.f_locals and \
            (stack[1].frame.f_locals["self"] == self or \
            stack[1].frame.f_locals["self"].__class__ == self.__sprinko_des):        
            return super().__getattribute__(__name)

        raise RuntimeError("Invalid scope")

    def update_dict(self, data : dict, skip_read = False):
        if not skip_read and self.__idict_modified != os.path.getmtime(self.__idict_path):
            with open(self.__idict_path, "r") as f:
                self.__idict = json.loads(f.read())
            self.__idict_modified = os.path.getmtime(self.__idict_path)
        
        self.__idict.update(data)

        new_checksum2 = hashlib.sha256(json.dumps(self.__idict).encode()).hexdigest()
        with open(self.__idict_path, "w") as f:
            data = json.dumps(self.__idict)
            f.write(data)

        self.__kr.set_password("meta", "checksum2", new_checksum2)    

    def check_id_hash(self, id : str, script : str):
        if id not in self.__idict:
            return False

        hashed = hashlib.sha256(script.encode()).hexdigest()
        return self.__idict[id] == hashed
    
    def set_id_hash(self, id : str, script : str):
        hashed = hashlib.sha256(script.encode()).hexdigest()
        self.__idict[id] = hashed
        with open(self.__idict_path, "w") as f:
            data = json.dumps(self.__idict)
            f.write(data)

        checksum2 = hashlib.sha256(data.encode()).hexdigest()

        self.__kr.set_password("meta", "checksum2", checksum2)
        self.__idict_modified = os.path.getmtime(self.__idict_path)

    def __init__(self):
        sprin_dot_ko_path = os.path.join(AppLoader().dbFolderPath, "sprin.ko")
        self.__kr = CryptFileKeyring()
        self.__kr.time_cost = 8
        self.__kr.file_path = sprin_dot_ko_path
        self.__idict_path = sprin_dot_ko_path + ".json"
        self.__idict = {}
        self.__idict_modified = 0

        self.__path = sprin_dot_ko_path
        if self.inited:
            try:
                self.verify()
                with open(self.__idict_path, "r") as f:
                    self.__idict = json.loads(f.read())
                self.__idict_modified = os.path.getmtime(self.__idict_path)
            except AssertionError:
                print("MAC failed")
                exit(1)

    @cache
    def meta(self):
        return {
            "version" : self.__kr.get_password("meta", "version"),
            "modified" : self.__kr.get_password("meta", "lastmodified"),
        }

    @property
    def path(self):
        return self.__path
    
    @property
    def inited(self):
        if os.path.exists(self.path):
            return True
        
        if os.path.exists(os.path.join(core_mod, "verf")):
            return True
        
        return False
    
    def verify(self):
        self.__kr.keyring_key = self.get_pass()

        verf_code = self.__kr.get_password("meta", "verf")
        with open(os.path.join(core_mod, "verf"), "rb") as f:
            verf_code2 = f.read()
            verf_code2 = base64.urlsafe_b64encode(verf_code2).decode()
        assert verf_code == verf_code2
        
        version = self.__kr.get_password("meta", "version")
        if version != core.__version__:
            inp = input("Version mismatch, continue will reset (Type confirm)")
            if inp != "confirm":
                exit(1)
            
            self.__kr.set_password("meta", "lastmodified", str(datetime.datetime.now().timestamp()))
            self.__kr.set_password("meta", "version", core.__version__)
            self.__kr.set_password("meta", "checksum", utils.compute_mod_hash(root_mod))
        else:
            checksum = self.__kr.get_password("meta", "checksum")
            assert checksum == utils.compute_mod_hash(root_mod)

        checksum2 = self.__kr.get_password("meta", "checksum2")
        with open(self.__idict_path, "r") as f:
            checksum2_2 = hashlib.sha256(f.read().encode()).hexdigest()
        assert checksum2 == checksum2_2

    @staticmethod
    def reset():
        if os.path.exists((path:=os.path.join(core_mod, "verf"))):
            os.remove(path)
        if os.path.exists((path:=os.path.join(AppLoader().dbFolderPath, "sprin.ko"))):
            os.remove(path)
        if os.path.exists((path := os.path.join(AppLoader().dbFolderPath, "sprin.ko.json"))):
            os.remove(path)

    def setup(self, password : str, method : typing.Literal["keyring", "input", "environ"] = "input"):
        # 
        self.__kr.keyring_key = password

        # generate 64 random salt
        verf = os.urandom(64)
        with open(os.path.join(core_mod, "verf"), "wb") as f:
            f.write(verf)

        #with open(self.__idict_path, "w") as f:
        #    f.write("{}")

        self.__kr.set_password("meta", "verf", base64.urlsafe_b64encode(verf).decode())

        self.__kr.set_password("meta", "checksum", utils.compute_mod_hash(root_mod))

        #self.__kr.set_password("meta", "checksum2", '44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a')

        self.__kr.set_password("meta", "version", core.__version__)

        self.__kr.set_password("meta", "lastmodified", str(datetime.datetime.now().timestamp()))

        #
        if method == "keyring":
            utils.os_keyring.set_password("sprinko", "password", password)
        elif method == "input":
            pass
        elif method == "environ":
            print("You need to manually set SPRINKO_PASSWORD")

        # setup dict
        hashedDict = self.__setup_dict()
        self.update_dict(hashedDict, skip_read=True)
        self.__idict = hashedDict

    def __setup_dict(self):
        tagcond = FuzzyContext("sprinko", justcontains=True)
        ret = {}
        for snippet in Snippet.query(
            limit=-1, tag=Tag.query(name=tagcond)
        ):
            snippet : Snippet
            for i, frag in enumerate(snippet.content):
                ret[f"{snippet.id}[{i}]"] = hashlib.sha256(
                    frag["value"].encode()
                ).hexdigest()

        return ret


    def __get_pass_exec(self, query : str):
        ctx = {}
        exec(query, ctx)
        return ctx["get_pass"]()

    def get_pass(self, known_method : str = None):
        if known_method == "env":
            return os.environ.get("SPRINKO_PASSWORD")
        elif known_method == "keyring":
            return 
        elif known_method == "input":
            return click.prompt("Password", hide_input=True)  
        elif known_method is not None:
            return self.__setup_get_pass(known_method)
        else:
            pass

        if os.environ.get("SPRINKO_PASSWORD", None) is not None:
            return os.environ.get("SPRINKO_PASSWORD")
        
        if (method := os.environ.get("SPRINKO_METHOD", None)) is not None:
            return self.get_pass(method)
        
        if utils.os_keyring is not None \
            and (password := utils.os_keyring.get_password("sprinko", "password")) is not None:
            if "def get_pass" in password:
                return self.__get_pass_exec(password)
            return password
        
        return click.prompt("Password", hide_input=True)