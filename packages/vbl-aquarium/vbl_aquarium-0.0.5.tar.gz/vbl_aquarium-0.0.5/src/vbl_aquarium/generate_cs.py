from vbl_aquarium import *
from vbl_aquarium.models_urchin import *

import typing
import inspect
import models_unity

p2c_types = {
    'str': 'string',
}

def get_classes(module):
    # Get a list of all attributes in the module
    attributes = dir(module)
    # Filter out classes
    classes = [getattr(module, attr) for attr in attributes if isinstance(getattr(module, attr), type)]
    return classes


unity_class_names = [x.__name__ for x in get_classes(models_unity)]

def generate_csharp_struct(class_name: str, fields: List[str], enums = None, has_unity_classes = False):
    #build using statements
    usings = ''
    # if enums is not None:
    #     usings += 'using System;\nusing UnityEngine;'
    # else:
    if has_unity_classes:
        usings += 'using UnityEngine;' 

    # build field declartions
    field_declarations = "\n".join(f"    public {field};" for field in fields)

    # build enum str
    enum_str = ""
    if enums is not None:
        enum_array = "\n".join(f"    {v[0]} = {v[1]}," for v in enums[1])
        enum_str = f"""
\n\npublic enum {enums[0]}
{{
{enum_array}
}}
"""
         
    # build the full class file string
    return f"""
{usings}
    
public struct {class_name}
{{
{field_declarations}
}}{enum_str}
"""

def pydantic_to_csharp(pydantic_class, class_json):
    class_name = pydantic_class.__name__

    fields = []

    enums = None # when enums are active this should be a tuple (ClassName, [(Option1, Value1), (Option2, Value2)])

    has_unity_classes = False

    for name, data in pydantic_class.model_fields.items():
        field_data = ''

        # first, catch enums
        if 'enum' in str(data.annotation):
            # get the name of the enum
            enum_name = data.annotation.__name__
            # pull the defs
            enum_data = class_json["$defs"][enum_name]['enum'] 
            data_list = []
            for i, v in enumerate(enum_data):
                data_list.append((v, i))
            enums = (enum_name, data_list)
            field_data = f'{enum_name} {name}'

        # finally, deal with arrays
        elif typing.get_origin(data.annotation) == list:
            arg_class = typing.get_args(data.annotation)
            type_name = arg_class[0].__name__

            # convert str -> string properly
            if type_name in p2c_types.keys():
                type_name = p2c_types[type_name]

            if hasattr(arg_class[0], "__name__"):
                field_data = f'{type_name}[] {name}'
            else:
                print(arg_class[0])

        # next, deal with base classes
        elif hasattr(data.annotation, "__name__"):

            # convert str -> string properly
            type_name = data.annotation.__name__
            if type_name in p2c_types.keys():
                type_name = p2c_types[type_name]

            field_data = f'{type_name} {name}'

        else:
            raise Exception("need to write a new parser for a missing type")
        
        if not has_unity_classes:
            for uc in unity_class_names:
                if uc in field_data:
                    has_unity_classes = True
                    break

        fields.append(field_data)

    return generate_csharp_struct(class_name, fields, enums, has_unity_classes)