import models_unity
import models_generic
import models_urchin
import models_logging
import models_pinpoint

from generate_cs import *

import json
import os

def get_classes(module):
    # Get a list of all attributes in the module
    attributes = dir(module)
    # Filter out classes
    classes = [getattr(module, attr) for attr in attributes if isinstance(getattr(module, attr), type)]
    return classes

def get_classes_nunity(module):
    return [c for c in get_classes(module) if c not in unity_classes]

unity_classes = get_classes(models_unity)
unity_class_names = [x.__name__ for x in get_classes(models_unity)]

module_list = [models_generic, models_urchin, models_logging, models_pinpoint]
folder_prefix = ['generic', 'urchin', 'logging', 'pinpoint']


cdir = os.path.dirname(os.path.abspath(__file__))

for i, (module, cfolder) in enumerate(zip(module_list, folder_prefix)):
    classes = get_classes_nunity(module)
    
    for cclass in classes:
        
        if not cclass.__name__ in unity_class_names:

            path = f"{cdir}/../../models/schemas/{cfolder}"
            if not os.path.exists(path):
                    os.makedirs(path)

            with open(f"{path}/{cclass.__name__}.json", "w") as f:
                f.write(json.dumps(cclass.model_json_schema()))

            path = f"{cdir}/../../models/csharp/{cfolder}"
            if not os.path.exists(path):
                    os.makedirs(path)

            with open(f'{path}/{cclass.__name__}.cs', 'w') as f:
                f.write(pydantic_to_csharp(cclass, cclass.model_json_schema()))