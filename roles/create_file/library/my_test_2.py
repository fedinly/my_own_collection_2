#!/usr/bin/python

# Copyright: (c) 2026, Fedin Leonid <fedinly@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my test module.

options:
    path:
        description: Path of the file
        required: true
        type: path
    content:
        description: Content of the file
        required: true
        type: str
   
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Fedin Leonid (@fedinly)
'''

EXAMPLES = r'''
# Examples using module

'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.

'''

import errno
import os
import hashlib
import stat
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_bytes, to_native
from pathlib import Path

def get_sha256(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        # Read the file in 64KB blocks
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def create_file_if_not_exists(path, content):
    #tmp = os.path.join(Path.home(), path)
    content_to_file = str(content)
    if Path(path).exists():
        digest = get_sha256(path)
        tmp_path = os.path.join(Path.home(),os.path.basename(path))
        if Path(tmp_path).exists():
            os.remove(tmp_path)
        with open(tmp_path, 'w+') as f:
            f.write(content_to_file)
        tmp_digest = get_sha256(tmp_path)           
        if (digest != tmp_digest):
            with open(path, 'w') as f:
                f.write(content_to_file)
            return {"changed":True}
        else:
            return {"changed":False}
    else:
        with open(path, 'w+') as f:
            f.write(content_to_file)
        return {"changed":True}
    
def delete_existing_file(path):
    if os.path.exists(path):
        os.remove(path)
        return {"changed":True}
    else:
        return {"changed":False}

def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        # name=dict(type='str', required=True),
        # new=dict(type='bool', required=False, default=False)
        path=dict(type='path', required=True),
        content=dict(type='str', required=True),
        state=dict(type='str', required=False, default='new')
    )

    result = dict(
        changed=False
    )

   
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    # begin module logic
    path    = module.params['path']
    content = module.params['content']
    state   = module.params['state']
    

    if state == 'new':
        result = create_file_if_not_exists(path, content)
        # result['changed'] = True
    elif state == 'absent':
        result = delete_existing_file(path)
    else:
        module.fail_json(f'State {state} is unsupported here')
    

    module.exit_json(**result)



if __name__ == '__main__':
    main()