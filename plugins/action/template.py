#!/usr/bin/python

# As of Oct '26, I'm really sick and tired of writing the builtin.file (for
# creating directories) + builtin.template (for actual templating) combos. They
# can't even go together in a loop block! This module tires to combine the two.

import os.path
import stat

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        result = super().run(tmp, task_vars)

        dest = self._task.args["dest"]
        dir_path = os.path.dirname(dest)

        dir_args = self._task.args.copy()
        for opt in "src", "dest":
            dir_args.pop(opt, None)
        dir_args["path"] = dir_path
        dir_args["state"] = "directory"

        if "mode" in self._task.args:
            mode = self._task.args["mode"]
            # Doesn't support the symblolic form.
            if not isinstance(mode, int):
                try:
                    mode = int(mode, 8)
                except ValueError:
                    raise AnsibleActionFail(f"Mode {mode} must be an octal number")
            # +x on template file permissions:
            dir_mode = mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
            dir_args["mode"] = dir_mode

        result = self._execute_module(
            module_name="ansible.builtin.file",
            module_args=dir_args,
            task_vars=task_vars,
        )

        if result.get("failed"):
            return result

        # Example of calling another plugin can be found in Ansible's
        # lib/ansible/plugins/action/template.py
        template_action = self._shared_loader_obj.action_loader.get(
            "ansible.builtin.template",
            task=self._task,
            connection=self._connection,
            play_context=self._play_context,
            loader=self._loader,
            templar=self._templar,
            shared_loader_obj=self._shared_loader_obj,
        )
        result.update(template_action.run(task_vars=task_vars))

        return result
