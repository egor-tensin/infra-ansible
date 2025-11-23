#!/usr/bin/python

import base64
import re

from ansible.errors import AnsibleActionFail
from ansible.module_utils.common.text.converters import to_text
from ansible.plugins.action import ActionBase

LOG_PATH = '/var/log/dpkg.log'


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super().run(tmp, task_vars)

        if self._check_dpkg_log(task_vars):
            before = self._parse_dpkg_log(task_vars)
        else:
            before = []

        apt_result = self._execute_module(
            module_name='ansible.builtin.apt',
            module_args=self._task.args.get('apt_args', {}),
            task_vars=task_vars,
        )

        after = self._parse_dpkg_log(task_vars)

        apt_result['packages'] = after[len(before):]
        return apt_result

    def _check_dpkg_log(self, task_vars):
        return self._is_file_readable(LOG_PATH, task_vars)

    def _parse_dpkg_log(self, task_vars):
        contents = self._read_file(LOG_PATH, task_vars)
        lines = contents.splitlines()
        regex = re.compile(' install | upgrade | remove | purge ')
        lines = [line for line in lines if regex.search(line)]
        lines = [' '.join(line.split(' ')[2:]) for line in lines]
        return lines

    def _is_file_readable(self, path, task_vars):
        stat_result = self._execute_module(
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
        return stat_result['stat']['readable']

    def _read_file(self, path, task_vars):
        read_result = self._execute_module(
            module_name='ansible.builtin.slurp',
            module_args=dict(src=path),
            task_vars=task_vars,
        )
        if read_result.get('failed'):
            raise AnsibleActionFail(f"Couldn't read file {path}", result=read_result)
        return base64.b64decode(to_text(read_result['content'])).decode('utf-8')
