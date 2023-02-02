from typing import Callable, Any

import grpc
from grpc_interceptor import AsyncServerInterceptor
from loguru import logger

from middleware.signature_middleware import SignatureValidationInterceptor


class LoggerInterceptor(AsyncServerInterceptor):
    async def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        context: grpc.aio.ServicerContext,
        method_name: str,
    ) -> Any:
        [request_ip] = [x for x in context.invocation_metadata() if x.key == SignatureValidationInterceptor.IP_ADDRESS]

        response_or_iterator = method(request_or_iterator, context)
        if hasattr(response_or_iterator, "__aiter__"):
            return response_or_iterator
        else:
            logger.info("Received request for: `{}` from: `{}`.", method_name, request_ip.value)
            result = await response_or_iterator
            logger.debug(
                "Successfully processed response for method: `{}` with code: `{}`; details: `{}`; from: `{}`.",
                method_name,
                context.code,
                context.details,
                request_ip.value,
            )
            return result
