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


class ModuleIdentity(object):
    id = itertools.count(1)

    def __init__(self, name: str, last_update: str, organization: str,
                 contact_info: str, description: str, revision: str,
                 parent: str):
        self.id = next(self.id)
        self.name = name
        self.last_update = last_update
        self.organization = organization
        self.contact_info = contact_info
        self.description = description
        self.revision = revision
        self.parent = parent

    def __str__(self):
        return MibGeneratorTemplate.moduleIdentityTemplate.format(
            moduleName=self.name, lastUpdate=self.last_update,
            organization=self.organization, contactInfo=self.contact_info,
            description=self.description, revision=self.revision,
            parentObject=self.parent, objectID=self.id,
            curlyBracketOpen="{",
            curlyBracketClose="}")


class ObjectIdentitier(object):
    id = itertools.count(1)

    def __init__(self, name: str, parent: str):
        self.id = next(self.id)
        self.name = name
        self.parent = parent

    def __str__(self):
        return MibGeneratorTemplate.objectIdentifierTemplate.format(
            objectName=self.name,
            parentObject=self.parent,
            objectID=self.id,
            curlyBracketOpen="{",
            curlyBracketClose="}")


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

    def get_section_name(self):
        return eval(self.config.get("DEFAULT", "SectionName"))

    def get_module_identity(self):
        module_identity = eval(self.config.get("DEFAULT", "ModuleIdentity"))
        return ModuleIdentity(module_identity["name"],
                              module_identity["last_update"],
                              module_identity["organization"],
                              module_identity["contact_info"],
                              module_identity["description"],
                              module_identity["revision"],
                              module_identity["parent"],
                              )

    def get_imports(self) -> list:
        import_object_list = []
        imports = eval(self.config.get("DEFAULT", "Imports"))
        for import_ in imports:
            import_object = Imports(import_["modules"], import_["from"])
            import_object_list.append(import_object)

        return import_object_list

    def get_object_identifier(self) -> list:
        object_identifier_list = []
        object_identifier = eval(
            self.config.get("DEFAULT", "ObjectIdentifirer"))

        for object_ in object_identifier:
            o = ObjectIdentitier(object_["name"], object_["parent"])
            object_identifier_list.append(o)
        return object_identifier_list

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
    def __init__(self, file_path: str):
        self.file_path = file_path
        config = ConfigReader("../configs/sample.ini")
        self.section_name = config.get_section_name()
        self.imports = config.get_imports()
        self.module_identity = config.get_module_identity()
        self.object_identifier = config.get_object_identifier()
        self.scalars = config.get_scalars()
        self.tables = config.get_tables()

    def save(self):
        file_name = open(self.file_path, "w+")
        file_name.write(str(self))
        file_name.close()

    def __str__(self):
        return MibGeneratorTemplate.snmpFileTemplate.format(
            sectionName=self.section_name,
            imports="\n".join([str(import_) for import_ in self.imports]),
            moduleIdentity=str(self.module_identity),
            topLevelStructure="\n".join(
                [str(object_) for object_ in self.object_identifier]),
            scalars="\n".join([str(scalars) for scalars in self.scalars]),
            tables="# TODO: Fix tables",
            notification="# TODO: Fix notification",
        )


if __name__ == "__main__":
    mg = MibGenerator("./test.txt")
    mg.save()


