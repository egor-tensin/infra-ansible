import base64

from ansible.errors import AnsibleActionFail
from ansible.module_utils.common.text.converters import to_text


def does_file_exist(action, path, task_vars):
    stat_result = action._execute_module(
        module_name='ansible.builtin.stat',
        module_args=dict(
            path=path,
            get_attributes=False,
            get_checksum=False,
            get_mime=False,
        ),
        task_vars=task_vars,
    )
    if stat_result.get('failed'):
        raise AnsibleActionFail(f"Couldn't stat file {path}", result=stat_result)
    return stat_result['stat']['exists']


def read_file(action, path, task_vars, default=False):
    if default is not None:
        if not does_file_exist(action, path, task_vars):
            return default
    read_result = action._execute_module(
        module_name='ansible.builtin.slurp',
        module_args=dict(src=path),
        task_vars=task_vars,
    )
    if read_result.get('failed'):
        raise AnsibleActionFail(f"Couldn't read file {path}", result=read_result)
    return base64.b64decode(to_text(read_result['content'])).decode('utf-8')
