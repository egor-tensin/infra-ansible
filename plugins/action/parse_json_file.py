#!/usr/bin/python

import json

from ansible.errors import AnsibleActionFail
from ansible.plugins.action import ActionBase
from ansible_collections.tensin.infra.plugins.module_utils import file


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        result = super().run(tmp, task_vars)

        path = self._task.args['path']
        default = self._task.args.get('default')
        if default is not None:
            default = json.dumps(default)

        content = file.read_file(self, path, task_vars, default=default)

        try:
            content = json.loads(content)
        except json.JSONDecodeError as e:
            raise AnsibleActionFail(f'Failed to parse JSON at {path}') from e

        result['content'] = content
        return result
