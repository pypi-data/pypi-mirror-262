#!/usr/bin/env python3
# Copyright 2021-2022 NetCracker Technology Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from collections import OrderedDict
from typing import List

from kubemarine import admission
from kubemarine.core import flow

tasks = OrderedDict({
    "delete_custom": admission.delete_custom_task,
    "add_custom": admission.add_custom_task,
    "reconfigure_psp": admission.reconfigure_psp_task,
    "restart_pods": admission.restart_pods_task
})


class PSPAction(flow.TasksAction):
    def __init__(self) -> None:
        super().__init__('manage psp', tasks, recreate_inventory=True)


def create_context(cli_arguments: List[str] = None) -> dict:

    cli_help = '''
    Script for managing psp on existing Kubernetes cluster.

    How to use:

    '''

    parser = flow.new_procedure_parser(cli_help, tasks=tasks)
    context = flow.create_context(parser, cli_arguments, procedure='manage_psp')
    return context


def main(cli_arguments: List[str] = None) -> None:
    context = create_context(cli_arguments)
    flow.ActionsFlow([PSPAction()]).run_flow(context)


if __name__ == '__main__':
    main()
