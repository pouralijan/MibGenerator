#!/usr/bin/env python3

import configparser
import itertools

import MibGeneratorTemplate

__author__ = "Hassan Pouralijan"
__copyright__ = "Copyright 2019"
__credits__ = ["Hassan Pouralijan"]
__license__ = "GPL3"
__version__ = "0.0.1"
__maintainer__ = "Hassan Pouralijan"
__email__ = "pouralijan@gmail.com"
__status__ = "Production"


class SnmpObject(object):

    def __init__(self, name: str, object_type: str, permission: str,
                 status: str, parent: str, description: str):
        self.name = "{}_{}".format(name, str(self.id))
        self.type = object_type
        self.permission = permission
        self.status = status
        self.parent = parent
        self.description = description


class ScalarObject(SnmpObject):
    id = itertools.count(1)

    def __init__(self, name: str, object_type: str, permission: str,
                 status: str, parent: str, description: str):
        self.id = next(self.id)
        super(ScalarObject, self).__init__(name, object_type, permission,
                                           status, parent, description)

    def __str__(self):
        return MibGeneratorTemplate.scalarObjectTemplate.format(
            objectName=self.name,
            objectType=self.type,
            objectPermission=self.permission,
            objectStatus=self.status,
            parentObject=self.parent,
            objectDescription=self.description,
            objectID=self.id,
            curlyBracketOpen="{",
            curlyBracketClose="}")


class Imports(object):
    def __init__(self, modules: list, section: str):
        self.modules = modules
        self.chunked_module = [modules[x:x+2]
                               for x in range(0, len(modules), 2)]
        self.separated_module = []
        for chunk in self.chunked_module:
            self.separated_module.append(",".join(chunk))
        self.section = section

    def __str__(self):
        return MibGeneratorTemplate.importTemplates.format(
            modules="\n\t".join(self.separated_module),
            section=self.section)


class ConfigReader(object):
    def __init__(self, configfile: str):
        self.config = configparser.ConfigParser()
        self.config.read(configfile)

    def get_imports(self) -> list:
        import_object_list = []
        imports = eval(self.config.get("DEFAULT", "Imports"))
        for import_ in imports:
            import_object = Imports(import_["modules"], import_["from"])
            import_object_list.append(import_object)

        return import_object_list

    def get_scalars(self) -> list:
        scalars_object_list = []
        scalars = eval(self.config.get("DEFAULT", "Scalars"))
        for scalar in scalars:
            if "count" in scalar:
                for i in range(int(scalar["count"])):
                    scalar_object = ScalarObject(
                        scalar["name_prefix"],
                        scalar["type"], scalar["permission"],
                        scalar["status"], scalar["parent"],
                        scalar["description"])
                    scalars_object_list.append(scalar_object)
        return scalars_object_list

    def get_tables(self) -> list:
        tables = eval(self.config.get("DEFAULT", "Tables"))
        # TODO(Hassan Pouralijan): Fill a list of TableObject and return it.
        return None


class MibGenerator(object):
    def __init__(self):
        config = ConfigReader("../configs/sample.ini")
        self.imports_section = config.get_imports()
        self.scalars = config.get_scalars()
        self.tables = config.get_tables()
        self.generate_imports_section()
        self.generate_scalars()
        self.generate_tables()

    def generate_imports_section(self):
        if self.imports_section:
            for import_ in self.imports_section:
                print(import_)

    def generate_scalars(self):
        if self.scalars:
            for scalar_object in self.scalars:
                print(scalar_object)

    def generate_tables(self):
        if self.tables:
            for table in self.tables:
                print(table)


if __name__ == "__main__":
    MibGenerator()
