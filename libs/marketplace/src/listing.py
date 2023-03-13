import os
import importlib

from datetime import datetime
from inventory import Validator
from .packager import Package

from couchsurf import Connection

class Listing:

    """ Require:
        * author
        * date
        * version
        * description
    """

    def __init__(self, files: any = ""):
        if self.is_valid(files):
            print("[MARKETPLACE] Passed validation...")
            self.author = os.getlogin()
            self.date = datetime.now().timestamp()
            self.name = str(input("[MARKETPLACE] Name of package to list: "))

    def serialize(self) -> dict:
        obj = importlib.import_module(self.name)
        return {
            "Author": self.author,
            "Date": self.date,
            "Version": "v0.1.0",
            "Description": getattr(obj, self.name)().use.__doc__
        }

    def is_valid(self, files: any = "") -> bool:
        if os.path.isfile(files):
            files = [files]
        elif os.path.isdir(files):
            for parent, dirs, files in os.walk(files):
                files = files
        for file in files:
            # TODO: Convert Acquire.validate to bool?
            #       This fixes the issue that only _one_ of the
            #       files has to actually work -- and it tells us
            #       which file to add the code to.
            if Validator.validate(file):
                return True
        # TODO: Remains valid for now (for testing)
        return False

    def is_version(self) -> str:
        conn = Connection("marketplace")
        conn.request.get("listings")

    def pack(self):
        pass

        """
            To create a pyz package:
                * pack = Package(name = "NAME_OF_CLASS", files="FILES_TO_ADD")
                * pack.make()
        """

    def build(self) -> dict:
        print(self.serialize())

    def list(self) -> None:
        pass
