#!/usr/bin/python

import re

from ansible.errors import AnsibleActionFail
from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        result = super().run(tmp, task_vars)

        msg = self._task.args['msg']
        allowlist = self._task.args.get('allowlist', [])
        allowlist = [re.compile(pattern) for pattern in allowlist]
        skip_no_changes = self._task.args.get('skip_no_changes', False)

        dirty_files = self._get_dirty_file_list('/etc', task_vars)
        if not dirty_files:
            if skip_no_changes:
                return result
            raise AnsibleActionFail('Nothing to commit')

        if allowlist:
            unexpected = [
                path for path in dirty_files
                if not any([pattern.fullmatch(path) for pattern in allowlist])
            ]
            if unexpected:
                raise AnsibleActionFail(f"Unexpected modifications in repository:\n{'\n'.join(unexpected)}")

        return self._commit(msg, task_vars)

    def _get_dirty_file_list(self, repo_dir, task_vars):
        status = self._get_status(repo_dir, task_vars)
        status = status.splitlines()
        status = [line[3:] for line in status]
        return status

    def _get_status(self, repo_dir, task_vars):
        cmd_result = self._execute_module(
            module_name='ansible.builtin.command',
            module_args=dict(
                argv=['git', 'status', '--porcelain'],
                chdir=repo_dir,
            ),
            task_vars=task_vars,
        )
        if cmd_result.get('failed'):
            raise AnsibleActionFail(f"Couldn't get git status for {repo_dir}", result=cmd_result)
        return cmd_result['stdout']

    def _commit(self, msg, task_vars):
        cmd_result = self._execute_module(
            module_name='ansible.builtin.command',
            module_args=dict(
                argv=['etckeeper', 'commit', msg],
            ),
            task_vars=task_vars,
        )
        if cmd_result.get('failed'):
            raise AnsibleActionFail('etckeeper commit failed', result=cmd_result)
        return cmd_result
