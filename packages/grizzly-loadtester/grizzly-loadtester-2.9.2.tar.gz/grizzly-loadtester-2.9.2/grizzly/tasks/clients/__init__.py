"""@anchor pydoc:grizzly.tasks.clients Clients
Client tasks is functionality that is executed by locust and is registred to an URL scheme.
These tasks is used to make a request to another host than the scenario is actually load testing.

## Statistics

Executions of all client tasks will be visible with request type `CLNT`.

## Arguments

* `endpoint` _str_ - describes the request

If `endpoint` is a template variable which includes the scheme, the scheme for the request must be specified so the
correct `grizzly.tasks.client` implementation is used. The additional scheme will be removed when the request is
performed.
"""
from __future__ import annotations

import logging
import traceback
from abc import abstractmethod
from contextlib import contextmanager
from copy import copy
from datetime import datetime
from json import dumps as jsondumps
from os import environ
from pathlib import Path
from time import perf_counter as time
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Generator, List, Optional, Type, cast, final
from urllib.parse import unquote, urlparse

from grizzly.tasks import GrizzlyMetaRequestTask, grizzlytask, template
from grizzly.testdata.utils import resolve_variable
from grizzly.types import GrizzlyResponse, RequestDirection, RequestType
from grizzly.utils import merge_dicts, normalize
from grizzly_extras.arguments import parse_arguments, split_value
from grizzly_extras.transformer import TransformerContentType

if TYPE_CHECKING:  # pragma: no cover
    from grizzly.context import GrizzlyContext, GrizzlyContextScenario
    from grizzly.scenarios import GrizzlyScenario


# see https://github.com/python/mypy/issues/5374
@template('endpoint', 'destination', 'source', 'name', 'variable_template')
class ClientTask(GrizzlyMetaRequestTask):
    __scenario__: ClassVar[GrizzlyContextScenario]
    _scenario: GrizzlyContextScenario
    _schemes: List[str]
    _scheme: str
    _short_name: str
    _direction_arrow: ClassVar[Dict[RequestDirection, str]] = {
        RequestDirection.FROM: '<-',
        RequestDirection.TO: '->',
    }
    _context: ClassVar[Dict[str, Any]] = {}

    host: str
    grizzly: GrizzlyContext
    direction: RequestDirection
    endpoint: str
    name: Optional[str]
    payload_variable: Optional[str]
    metadata_variable: Optional[str]
    source: Optional[str]
    destination: Optional[str]
    _text: Optional[str]

    log_dir: Path

    def __init__(  # noqa: PLR0915
        self,
        direction: RequestDirection,
        endpoint: str,
        name: Optional[str] = None,
        /,
        payload_variable: Optional[str] = None,
        metadata_variable: Optional[str] = None,
        source: Optional[str] = None,
        destination: Optional[str] = None,
        text: Optional[str] = None,
    ) -> None:
        super().__init__()

        if text is not None:
            self.text = text
        else:
            self._text = None

        endpoint = cast(str, resolve_variable(self.grizzly, endpoint, only_grizzly=True))
        try:
            parsed = urlparse(endpoint)
            proto_sep = endpoint.index('://') + 3
            # if `proto_sep` is followed by the start of a jinja template, we should remove the specified protocol, since it will
            # be part of the rendered template
            if proto_sep != endpoint.rindex('://') + 3 or (endpoint[proto_sep:proto_sep + 2] == '{{' and '}}' in endpoint):
                endpoint = endpoint[proto_sep:]
        except ValueError:
            pass

        if parsed.scheme not in self._schemes:
            message = f'{self.__class__.__name__}: "{parsed.scheme}" is not supported, must be one of {", ".join(self._schemes)}'
            raise AttributeError(message)

        self._scheme = parsed.scheme

        content_type: TransformerContentType = TransformerContentType.UNDEFINED

        if '|' in endpoint:
            value, value_arguments = split_value(endpoint)
            arguments = parse_arguments(value_arguments, unquote=True)

            if 'content_type' in arguments:
                content_type = TransformerContentType.from_string(unquote(arguments['content_type']))
                del arguments['content_type']

            endpoint = value

        self.content_type = content_type
        self.direction = direction
        self.endpoint = endpoint
        self.name = name
        self.payload_variable = payload_variable
        self.metadata_variable = metadata_variable
        self.source = source
        self.destination = destination
        self.host = endpoint

        if self.payload_variable is not None and self.direction != RequestDirection.FROM:
            message = f'{self.__class__.__name__}: variable argument is not applicable for direction {self.direction.name}'
            raise AssertionError(message)

        if self.source is not None and self.direction != RequestDirection.TO:
            message = f'{self.__class__.__name__}: source argument is not applicable for direction {self.direction.name}'
            raise AssertionError(message)

        if self.payload_variable is not None and self.payload_variable not in self.grizzly.state.variables:
            message = f'{self.__class__.__name__}: variable {self.payload_variable} has not been initialized'
            raise AssertionError(message)

        if self.metadata_variable is not None and self.metadata_variable not in self.grizzly.state.variables:
            message = f'{self.__class__.__name__}: variable {self.metadata_variable} has not been initialized'
            raise AssertionError(message)

        if self.payload_variable is None and self.metadata_variable is not None:
            message = f'{self.__class__.__name__}: payload variable is not set, but metadata variable is set'
            raise AssertionError(message)

        if self.source is None and self.direction == RequestDirection.TO:
            message = f'{self.__class__.__name__}: source must be set for direction {self.direction.name}'
            raise AssertionError(message)

        self._short_name = self.__class__.__name__.replace('ClientTask', '')

        context_root = environ.get('GRIZZLY_CONTEXT_ROOT', None)
        assert context_root is not None, 'environment variable GRIZZLY_CONTEXT_ROOT is not set!'

        self.log_dir = Path(context_root) / 'logs'
        log_dir = environ.get('GRIZZLY_LOG_DIR', None)
        if log_dir is not None:
            self.log_dir /= log_dir

        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._scenario = copy(self.__scenario__)
        self._scenario._tasks = self.__scenario__._tasks
        self.__class__._context = merge_dicts(self.__class__._context, self._context)

    def on_start(self, parent: GrizzlyScenario) -> None:
        pass

    def on_stop(self, parent: GrizzlyScenario) -> None:
        pass

    # SOW: see https://github.com/python/mypy/issues/5936#issuecomment-1429175144
    def text_fget(self) -> Optional[str]:
        return self._text

    def text_fset(self, _: str) -> None:
        message = f'{self.__class__.__name__} has not implemented support for step text'
        raise NotImplementedError(message)  # pragma: no cover

    text = property(text_fget, text_fset)
    # EOW

    @property
    def variable_template(self) -> Optional[str]:
        if self.payload_variable is None or ('{{' in self.payload_variable and '}}' in self.payload_variable):
            return self.payload_variable

        template = f'{{{{ {self.payload_variable} }}}}'

        if self.metadata_variable is not None:
            template = f'{template} {{{{ {self.metadata_variable} }}}}'

        return template

    @final
    def __call__(self) -> grizzlytask:
        @grizzlytask
        def task(parent: GrizzlyScenario) -> GrizzlyResponse:
            return self.execute(parent)

        @task.on_start
        def on_start(parent: GrizzlyScenario) -> None:
            self.__class__._context = merge_dicts(parent.user._context, self._context)
            return self.on_start(parent)

        @task.on_stop
        def on_stop(parent: GrizzlyScenario) -> None:
            self.__class__._context = merge_dicts(parent.user._context, self._context)
            return self.on_stop(parent)

        return task

    def execute(self, parent: GrizzlyScenario) -> GrizzlyResponse:
        """Execute correct method depending on the direction on the request. When wrapped in another task, the @grizzlytask decorated method above will not be called."""
        self.__class__._context = merge_dicts(parent.user._context, self.__class__._context)

        if self.direction == RequestDirection.FROM:
            return self.get(parent)

        return self.put(parent)

    @abstractmethod
    def get(self, parent: GrizzlyScenario) -> GrizzlyResponse:  # pragma: no cover
        message = f'{self.__class__.__name__} has not implemented GET'
        raise NotImplementedError(message)

    @abstractmethod
    def put(self, parent: GrizzlyScenario) -> GrizzlyResponse:  # pragma: no cover
        message = f'{self.__class__.__name__} has not implemented PUT'
        raise NotImplementedError(message)

    @contextmanager
    def action(self, parent: GrizzlyScenario, action: Optional[str] = None, *, suppress: bool = False) -> Generator[Dict[str, Any], None, None]:
        exception: Optional[Exception] = None
        response_length = 0
        start_time = time()
        meta: Dict[str, Any] = {}

        try:
            # get metadata back from actual implementation
            yield meta
        except Exception as e:
            parent.logger.exception('%s:', self.__class__.__name__)
            exception = e
        finally:
            if self.name is None:
                action = action or meta.get('action', self.payload_variable)
                name = f'{parent.user._scenario.identifier} {self._short_name}{meta.get("direction", self._direction_arrow[self.direction])}{action}'
            else:
                rendered_name = parent.render(self.name)
                name = f'{parent.user._scenario.identifier} {rendered_name}'

            response_time = int((time() - start_time) * 1000)
            response_length = meta.get('response_length') or 0

            if exception is None:
                exception = meta.get('exception')

            if not suppress or exception is not None:
                parent.user.environment.events.request.fire(
                    request_type=RequestType.CLIENT_TASK(),
                    name=name,
                    response_time=response_time,
                    response_length=response_length,
                    context=parent.user._context,
                    exception=exception,
                )

            if exception is not None or parent.user._scenario.context.get('log_all_requests', False):
                log_name = normalize(name)
                log_date = datetime.now()
                log_file = self.log_dir / f'{log_name}.{log_date.strftime("%Y%m%dT%H%M%S%f")}.log'

                meta.get('request', {}).update({'time': response_time})

                request_log: Dict[str, Any] = {
                    'stacktrace': None,
                    'response': meta.get('response'),
                    'request': meta.get('request'),
                }

                if exception is not None:
                    request_log.update({'stacktrace': traceback.format_exception(
                        type(exception),
                        value=exception,
                        tb=exception.__traceback__,
                    )})

                log_file.write_text(jsondumps(request_log, indent=2))

            if exception is not None and parent.user._scenario.failure_exception is not None:
                parent.logger.error('%s raising %s', self.__class__.__name__, parent.user._scenario.failure_exception)
                raise parent.user._scenario.failure_exception
            elif exception is not None:
                parent.logger.warning('%s ignoring %s', self.__class__.__name__, exception)


class client:
    available: ClassVar[Dict[str, Type[ClientTask]]] = {}
    schemes: List[str]

    def __init__(self, scheme: str, *additional_schemes: str) -> None:
        schemes = [scheme]
        if len(additional_schemes) > 0:
            schemes += list(additional_schemes)
        self.schemes = schemes

    def __call__(self, impl: Type[ClientTask]) -> Type[ClientTask]:
        available = {scheme: impl for scheme in self.schemes}
        impl._schemes = self.schemes
        client.available.update(available)

        return impl


logger = logging.getLogger(__name__)

from .blobstorage import BlobStorageClientTask
from .http import HttpClientTask
from .messagequeue import MessageQueueClientTask
from .servicebus import ServiceBusClientTask

__all__ = [
    'HttpClientTask',
    'BlobStorageClientTask',
    'MessageQueueClientTask',
    'ServiceBusClientTask',
    'logger',
]
