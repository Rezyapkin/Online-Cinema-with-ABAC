from typing import Callable, Any

import grpc
from grpc_interceptor import AsyncServerInterceptor
from grpc_auth_service.utils import Metadata
from loguru import logger


class SignatureValidationInterceptor(AsyncServerInterceptor):
    USER_AGENT: str = Metadata.USER_AGENT
    IP_ADDRESS: str = Metadata.IP_ADDRESS

    async def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        context: grpc.aio.ServicerContext,
        method_name: str,
    ) -> Any:
        expected_metadata = {self.USER_AGENT, self.IP_ADDRESS}
        actual_metadata = context.invocation_metadata()

        if expected_metadata.issubset({x.key for x in actual_metadata}):
            response_or_iterator = method(request_or_iterator, context)
            if hasattr(response_or_iterator, "__aiter__"):
                return response_or_iterator
            else:
                return await response_or_iterator
        else:
            logger.warning("Invalid request signature for method: `{}`.", method_name)
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Invalid Request Signature!")
