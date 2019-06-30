
scalarObjectTemplate = """{objectName} OBJECT-TYPE
    SYNTAX      {objectType}
    MAX-ACCESS  {objectPermission}
    STATUS      {objectStatus}
    DESCRIPTION
    "{objectDescription}"
    ::= {curlyBracketOpen} {parentObject} {objectID} {curlyBracketClose}
"""
