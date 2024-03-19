from __future__ import annotations

from collections import UserDict
from typing import Literal


class DefaultDescriptor:
    def __init__(self, factory):
        self.factory = factory

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance: Saga, owner: type[Saga]):
        if instance is None:
            return owner
        value = self.factory()
        setattr(instance, self.name, value)
        return value


class State(UserDict):
    pass


class Step:
    def action(self, state: State):
        pass

    def compensate(self, state: State):
        pass


class Saga:
    state: State = DefaultDescriptor(State)
    steps: list[Step] = DefaultDescriptor(list)
    status: Literal["success", "rollback", "error"]
    _execute_exc: Exception
    _rollback_exc: Exception
    _current_index: int
    _error_index: int

    def run(self):
        try:
            self._execute()
        except Exception as exc1:
            self._execute_exc = exc1
            try:
                self._rollback()
                self.status = "rollback"
            except Exception as exc2:
                self._rollback_exc = exc2
                self._error_index = self._current_index
                self.status = "error"
                self.on_error()
                raise exc2
            self.on_failure()
            raise exc1
        else:
            self.status = "success"
            self.on_success()

    def _execute(self):
        self._current_index = 0
        for idx, step in enumerate(self.steps):
            self._current_index = idx
            step.action(self.state)

    def _rollback(self):
        for idx in range(self._current_index - 1, -1, -1):
            self._current_index = idx
            self.steps[idx].compensate(self.state)

    def on_success(self):
        pass

    def on_failure(self):
        pass

    def on_error(self):
        pass

    @property
    def is_success(self):
        return self.status == "success"

    @property
    def is_rollback(self):
        return self.status == "rollback"

    @property
    def is_error(self):
        return self.status == "error"
