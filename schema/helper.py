import json

structures = [
    {
        "name": "Listed company",
        "subtypeOf": [
            {
                "name": "Company"
            }
        ]
    },
    {
        "name": "Local Government",
        "subtypeOf": [
            {
                "name": "Government Agency"
            }
        ]
    },
    {
        "name": "Sole trader",
        "subtypeOf": [
            {
                "name": "Company"
            }
        ]
    },
    {
        "name": "Unincorporated body",
        "subtypeOf": None
    },
    {
        "name": "Community Interest Company",
        "subtypeOf": [
            {
                "name": "Company"
            }
        ]
    },
    {
        "name": "Mutual",
        "subtypeOf": [
            {
                "name": "Company"
            }
        ]
    },
    {
        "name": "Trust",
        "subtypeOf": None
    },
    {
        "name": "Partnership",
        "subtypeOf": [
            {
                "name": "Company"
            }
        ]
    },
    {
        "name": "Limited Company",
        "subtypeOf": [
            {
                "name": "Company"
            }
        ]
    },
    {
        "name": "Company",
        "subtypeOf": None
    },
    {
        "name": "Public service",
        "subtypeOf": [
            {
                "name": "Government Agency"
            }
        ]
    },
    {
        "name": "Government Agency",
        "subtypeOf": None
    },
    {
        "name": "Charity",
        "subtypeOf": None
    }
]



new_struct = []

for structure in structures:
    if structure['subtypeOf']:
        code = structure['subtypeOf'][0]['name'].lower().replace(" ","_") + "/" + structure['name'].lower().replace(" ","_")
        parent = structure['subtypeOf'][0]['name'].lower().replace(" ","_")
    else:
        code = structure['name'].lower().replace(" ","_")
        parent = None

    new_struct.append({"code": code, "title": { "en": structure['name'] }, "parent":parent})

print(json.dumps(new_struct,indent=4))