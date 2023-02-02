from typing import Callable, Any, AsyncIterable, AsyncGenerator

import grpc
from grpc_interceptor import AsyncServerInterceptor
from grpc_interceptor.exceptions import GrpcException
from loguru import logger


# noinspection PyUnusedLocal
class ExceptionToStatusMiddleware(AsyncServerInterceptor):
    def __init__(self, status_on_unknown_exception: grpc.StatusCode | None = None):
        if status_on_unknown_exception == grpc.StatusCode.OK:
            raise ValueError("The status code for unknown exceptions cannot be OK")

        self._status_on_unknown_exception = status_on_unknown_exception

    async def _generate_responses(
        self,
        request_or_iterator: Any,
        context: grpc.ServicerContext,
        method_name: str,
        response_iterator: AsyncIterable,
    ) -> AsyncGenerator[Any, None]:
        """Yield all the responses, but check for errors along the way."""
        try:
            async for r in response_iterator:
                yield r
        except Exception as ex:
            await self.handle_exception(ex, request_or_iterator, context, method_name)

    async def handle_exception(
        self,
        ex: Exception,
        request_or_iterator: Any,
        context: grpc.ServicerContext,
        method_name: str,
    ) -> None:
        """Override this if extending ExceptionToStatusInterceptor.

        This will get called when an exception is raised while handling the RPC.

        Args:
            ex: The exception that was raised.
            request_or_iterator: The RPC request, as a protobuf message if it is a
                unary request, or an iterator of protobuf messages if it is a streaming
                request.
            context: The servicer context. You probably want to call context.abort(...)
            method_name: The name of the RPC being called.

        Raises:
            This method must raise and cannot return, as in general there's no
            meaningful RPC response to return if an exception has occurred. You can
            raise the original exception, ex, or something else.
        """
        if isinstance(ex, GrpcException):
            logger.debug(
                "Failed response for method: `{}` with code: `{}`; details: `{}`.",
                method_name,
                ex.status_code,
                ex.details,
            )
            await context.abort(ex.status_code, ex.details)
        else:
            logger.exception(ex)
            if self._status_on_unknown_exception is not None:
                await context.abort(self._status_on_unknown_exception, repr(ex))
        raise ex

    async def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        context: grpc.ServicerContext,
        method_name: str,
    ) -> Any:
        try:
            response_or_iterator = method(request_or_iterator, context)
            if not hasattr(response_or_iterator, "__aiter__"):
                return await response_or_iterator
        except Exception as ex:
            await self.handle_exception(ex, request_or_iterator, context, method_name)

        return self._generate_responses(request_or_iterator, context, method_name, response_or_iterator)
