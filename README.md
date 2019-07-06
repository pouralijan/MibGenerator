
# MibGenerator
MibGenerator generate a snmp mib file from a config file.


- [x] Implement top level structure.
- [x] Implement module identity.
- [x] Implement import object from another mib file.
- [x] Implement auto detects objects ID.
- [x] Add support scalars.
- [ ] Add support tables.
- [ ] Add support notification.
- [ ] Add cli parameters (get config file and output path).
- [ ] Fix bugs. see([Issues](https://github.com/pouralijan/MibGenerator/issues))
 
## Config file

Config file is a ini config format file. Config file have a section (DEFAULT) and several parameter([config example](https://github.com/pouralijan/MibGenerator/blob/master/configs/sample.ini)).

- SectionName: A string of mib section name.
- ModuleIdentity: A dict of mib file identity configuration this ditc have a:
  - name:
  - last_update:
  - organization:
  - contact_info:
  - description:
  - revision:
  - parent:
- ObjectIdentifirer: A list top level structure of mib file, evry item in list is a dict, every dict have a:
  - name: Top level structure section.
  - parent: Parent name.
- Imports: A list of import object from another mib, evry item in list is a dict, every dict have a:
  - modules: A list of object.
  - from: Name of other section.
- Scalars: A list of scalar mib object, every item in list is a dict, evry dict have a:
  - count: Count of repete this object.
  - name_prefix: Scalar object prefix name.
  - type: SNMP object type.
  - permission: Read and write permission.
  - status: Object status.
  - description: Description of object.
  - parent: Object parent name.
- Tables: DOTO: Implement
