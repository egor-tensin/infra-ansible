#!/usr/bin/python

from ansible.plugins.action import ActionBase
from ansible_collections.tensin.infra.plugins.module_utils import file


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        result = super().run(tmp, task_vars)

        path = self._task.args['path']
        default = self._task.args.get('default')

        result['content'] = file.read_file(self, path, task_vars, default=default)
        return result
