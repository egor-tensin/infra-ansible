#!/usr/bin/python

import re

from ansible.plugins.action import ActionBase
from ansible_collections.tensin.infra.plugins.module_utils import file

LOG_PATH = '/var/log/dpkg.log'


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        super().run(tmp, task_vars)

        before = self._parse_dpkg_log(task_vars, default='')

        apt_result = self._execute_module(
            module_name='ansible.builtin.apt',
            module_args=self._task.args.get('apt_args', {}),
            task_vars=task_vars,
        )

        after = self._parse_dpkg_log(task_vars)

        apt_result['packages'] = after[len(before):]
        return apt_result

    def _parse_dpkg_log(self, task_vars, default=None):
        contents = file.read_file(self, LOG_PATH, task_vars, default=default)
        lines = contents.splitlines()
        regex = re.compile(' install | upgrade | remove | purge ')
        lines = [line for line in lines if regex.search(line)]
        lines = [' '.join(line.split(' ')[2:]) for line in lines]
        return lines
