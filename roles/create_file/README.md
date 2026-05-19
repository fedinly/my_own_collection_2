Role Name
=========

Role for using module "Create_file".

Requirements
------------

Python3.12

Role Variables
--------------
All variables which can be overridden are stored in defaults/main.yml file as well as in table below.

| Name | Default Value |        Description |
|------|---------------|--------------|
| `path` | '/tmp/testing.txt' | Full path for creating file |
| `content` | 'Some text' | Content that you want to see inside the file |
| `state` | new | Variables are: 'new' for create and 'absent' for delete file |

Dependencies
------------

Example Playbook
----------------

Including an example of how to use role (for instance, with variables passed in as parameters):

  - name: Create file  
  tags: Create_file  
  hosts: create_file  
  roles:  
    - create_file  

License
-------

BSD

Author Information
------------------

Fedin Leonid <fedinly@gmail.com>
