import os
import shlex

from ansible.errors import AnsibleActionFail
from ansible.module_utils.common.text.converters import to_text


def is_work_tree(action, repo_dir, task_vars):
    cmd_result = action._execute_module(
        module_name='ansible.builtin.command',
        module_args=dict(
            argv=['git', 'rev-parse', '--is-inside-work-tree'],
            chdir=repo_dir,
        ),
        task_vars=task_vars,
    )
    return not cmd_result.get('failed')


def get_status(action, repo_dir, task_vars):
    cmd_result = action._execute_module(
        module_name='ansible.builtin.command',
        module_args=dict(
            argv=['git', 'status', '--porcelain'],
            chdir=repo_dir,
        ),
        task_vars=task_vars,
    )
    if cmd_result.get('failed'):
        raise AnsibleActionFail(f"Couldn't get git status for {repo_dir}", result=cmd_result)
    return to_text(cmd_result['stdout'])


def get_dirty_file_list(action, repo_dir, task_vars):
    status = get_status(action, repo_dir, task_vars)
    status = status.splitlines()
    status = [line[3:] for line in status]
    return status


def get_remote_url(action, repo_dir, task_vars, remote='origin'):
    cmd_result = action._execute_module(
        module_name='ansible.builtin.command',
        module_args=dict(
            argv=['git', 'config', '--local', f'remote.{remote}.url'],
            chdir=repo_dir,
        ),
        task_vars=task_vars,
    )
    if cmd_result.get('failed'):
        raise AnsibleActionFail(f"Couldn't read the URL of remote '{remote}' in {repo_dir}", result=cmd_result)
    return cmd_result['stdout']


def update_remote(action, repo_dir, remote, task_vars, accept_hostkey=False):
    ssh = os.environ.get('GIT_SSH', 'ssh')
    ssh_opts = ''
    if accept_hostkey:
        ssh_opts += ' -o StrictHostKeyChecking=no'
    ssh_command = shlex.quote(ssh) + ssh_opts

    cmd_result = action._execute_module(
        module_name='ansible.builtin.command',
        module_args=dict(
            argv=['env', f'GIT_SSH_COMMAND={ssh_command}', 'git', 'remote', 'update', remote],
            chdir=repo_dir,
        ),
        task_vars=task_vars,
    )
    if cmd_result.get('failed'):
        raise AnsibleActionFail(f"Couldn't update remote '{remote}' for {repo_dir}", result=cmd_result)


def is_ancestor(action, repo_dir, remote, version, task_vars):
    looks_like_hash = all(((c >= '0' and c <= '9') or (c >= 'a' and c <= 'f') for c in version))

    remote_versions = [f'{remote}/{version}']
    if looks_like_hash:
        remote_versions += [version]

    for _version in remote_versions:
        cmd_result = action._execute_module(
            module_name='ansible.builtin.command',
            module_args=dict(
                argv=['git', 'merge-base', '--is-ancestor', 'HEAD', _version],
                chdir=repo_dir,
            ),
            task_vars=task_vars,
        )
        if cmd_result.get('failed'):
            if cmd_result.get('stderr'):
                continue
        else:
            return True

    raise AnsibleActionFail(f"Couldn't deduce how the HEAD of {repo_dir} relates to remote version {remote}/{version}")
