snmpFileTemplate = """{sectionName} DEFINITIONS ::= BEGIN

{imports}

{moduleIdentity}

{topLevelStructure}

{scalars}

{tables}

{notification}

END
"""

importTemplates = """IMPORTS {modules} FROM {section};"""

moduleIdentityTemplate = """{moduleName} MODULE-IDENTITY
    LAST-UPDATED "{lastUpdate}"
    ORGANIZATION "{organization}"
    CONTACT-INFO "{contactInfo}"
    DESCRIPTION "{description}"
    REVISION     "{revision}"
    ::= {curlyBracketOpen} {parentObject} {objectID} {curlyBracketClose}
"""

objectIdentifierTemplate = """{objectName} OBJECT IDENTIFIER 
                ::= {curlyBracketOpen} {parentObject} {objectID} {curlyBracketClose}"""

scalarObjectTemplate = """{objectName} OBJECT-TYPE
    SYNTAX      {objectType}
    MAX-ACCESS  {objectPermission}
    STATUS      {objectStatus}
    DESCRIPTION
    "{objectDescription}"
    ::= {curlyBracketOpen} {parentObject} {objectID} {curlyBracketClose}
"""
