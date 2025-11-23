#!/usr/bin/python

from ansible.errors import AnsibleActionFail
from ansible.plugins.action import ActionBase
from ansible_collections.tensin.infra.plugins.module_utils import file, git


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        result = super().run(tmp, task_vars)

        repo = self._task.args['repo']
        dest = self._task.args['dest']
        accept_hostkey = self._task.args.get('accept_hostkey', False)
        remote = self._task.args.get('remote', 'origin')
        version = self._task.args['version']

        builtin_args = {
            'repo': repo,
            'dest': dest,
            'accept_hostkey': accept_hostkey,
            'remote': remote,
            'version': version,
        }

        if not file.does_dir_exist(self, dest, task_vars):
            # If the destination directory doesn't exist, delegate to the
            # builtin module.
            return self._execute_module(
                module_name='ansible.builtin.git',
                module_args=builtin_args,
                task_vars=task_vars,
            )

        # ansible.builtin.git would just remove everything, fuck that.
        if not git.is_work_tree(self, dest, task_vars):
            raise AnsibleActionFail(f'Destination {dest} exists but is not a repository')

        # Again, ansible.builtin.git would just remove everything, fuck that.
        current_url = git.get_remote_url(self, dest, task_vars, remote=remote)
        if current_url != repo:
            raise AnsibleActionFail(f"Existing remote URL '{current_url}' doesn't match '{repo}' for {dest}")

        # ansible.builtin.git would abort if the `force` parameter is set to
        # `false`, but I don't want to depend on default values.
        dirty_files = git.get_dirty_file_list(self, dest, task_vars)
        if dirty_files:
            raise AnsibleActionFail(f'There are local changes in {dest}')

        # Fetch the remote.
        git.update_remote(self, dest, remote, task_vars, accept_hostkey=accept_hostkey)

        # If the current HEAD is not an ancestor of the requested version, fail
        # (again, unlike the builtin module).
        is_ancestor = git.is_ancestor(self, dest, remote, version, task_vars)
        if not is_ancestor:
            raise AnsibleActionFail(f'HEAD in {dest} is not an ancestor of {remote}/{version}')

        # Finally, everything looks good, delegate to the builtin module.
        return self._execute_module(
            module_name='ansible.builtin.git',
            module_args=builtin_args,
            task_vars=task_vars,
        )
