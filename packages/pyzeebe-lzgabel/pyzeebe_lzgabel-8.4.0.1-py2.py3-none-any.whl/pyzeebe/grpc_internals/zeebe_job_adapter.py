import asyncio
import json
import logging
from typing import AsyncGenerator, Dict, List, Optional

import grpc
from zeebe_grpc.gateway_pb2 import (
    ActivateJobsRequest,
    CompleteJobRequest,
    CompleteJobResponse,
    FailJobRequest,
    FailJobResponse,
    ThrowErrorRequest,
    ThrowErrorResponse,
    StreamActivatedJobsRequest,
)

from pyzeebe.errors import (
    ActivateJobsRequestInvalidError,
    JobAlreadyDeactivatedError,
    JobNotFoundError,
)
from pyzeebe.grpc_internals.grpc_utils import is_error_status
from pyzeebe.grpc_internals.zeebe_adapter_base import ZeebeAdapterBase
from pyzeebe.job.job import Job

logger = logging.getLogger(__name__)


class ZeebeJobAdapter(ZeebeAdapterBase):
    async def activate_jobs(
        self,
        task_type: str,
        worker: str,
        timeout: int,
        max_jobs_to_activate: int,
        variables_to_fetch: List[str],
        request_timeout: int,
        tenant_ids: Optional[List[str]] = None,
    ) -> AsyncGenerator[Job, None]:
        try:
            async for response in self._gateway_stub.ActivateJobs(
                ActivateJobsRequest(
                    type=task_type,
                    worker=worker,
                    timeout=timeout,
                    maxJobsToActivate=max_jobs_to_activate,
                    fetchVariable=variables_to_fetch,
                    requestTimeout=request_timeout,
                    tenantIds=tenant_ids,
                )
            ):
                for raw_job in response.jobs:
                    job = self._create_job_from_raw_job(raw_job)
                    logger.debug("Got job: %s from zeebe", job)
                    yield job
        except grpc.aio.AioRpcError as grpc_error:
            if is_error_status(grpc_error, grpc.StatusCode.INVALID_ARGUMENT):
                raise ActivateJobsRequestInvalidError(task_type, worker, timeout, max_jobs_to_activate) from grpc_error
            await self._handle_grpc_error(grpc_error)

    async def openStream(
        self,
        task_type: str,
        worker: str,
        timeout: int,
        variables_to_fetch: List[str],
        queue: asyncio.Queue,
        tenant_ids: Optional[List[str]] = None,
    ):
        try:
            stream = self._gateway_stub.StreamActivatedJobs(
                StreamActivatedJobsRequest(
                    type=task_type,
                    worker=worker,
                    timeout=timeout,
                    fetchVariable=variables_to_fetch,
                    tenantIds=tenant_ids
                )
            )

            async for job in stream:
                raw_job = self._create_job_from_raw_job(job, True)
                await queue.put(raw_job)
        except grpc.aio.AioRpcError as grpc_error:
            if is_error_status(grpc_error, grpc.StatusCode.INVALID_ARGUMENT):
                raise ActivateJobsRequestInvalidError(task_type, worker, timeout) from grpc_error
            await self._handle_grpc_error(grpc_error)

    def _create_job_from_raw_job(self, response, stream_job: Optional[bool] = False) -> Job:
        return Job(
            key=response.key,
            type=response.type,
            process_instance_key=response.processInstanceKey,
            bpmn_process_id=response.bpmnProcessId,
            process_definition_version=response.processDefinitionVersion,
            process_definition_key=response.processDefinitionKey,
            element_id=response.elementId,
            element_instance_key=response.elementInstanceKey,
            custom_headers=json.loads(response.customHeaders),
            worker=response.worker,
            retries=response.retries,
            deadline=response.deadline,
            variables=json.loads(response.variables),
            tenant_id=response.tenantId,
            zeebe_adapter=self,
            stream_job=stream_job,
        )

    async def complete_job(self, job_key: int, variables: Dict) -> CompleteJobResponse:
        try:
            return await self._gateway_stub.CompleteJob(
                CompleteJobRequest(jobKey=job_key, variables=json.dumps(variables))
            )
        except grpc.aio.AioRpcError as grpc_error:
            if is_error_status(grpc_error, grpc.StatusCode.NOT_FOUND):
                raise JobNotFoundError(job_key=job_key) from grpc_error
            elif is_error_status(grpc_error, grpc.StatusCode.FAILED_PRECONDITION):
                raise JobAlreadyDeactivatedError(job_key=job_key) from grpc_error
            await self._handle_grpc_error(grpc_error)

    async def fail_job(
            self, job_key: int, retries: int, message: str, retry_back_off_ms: int, variables: Dict
    ) -> FailJobResponse:
        try:
            return await self._gateway_stub.FailJob(
                FailJobRequest(
                    jobKey=job_key,
                    retries=retries,
                    errorMessage=message,
                    retryBackOff=retry_back_off_ms,
                    variables=json.dumps(variables),
                )
            )
        except grpc.aio.AioRpcError as grpc_error:
            if is_error_status(grpc_error, grpc.StatusCode.NOT_FOUND):
                raise JobNotFoundError(job_key=job_key) from grpc_error
            elif is_error_status(grpc_error, grpc.StatusCode.FAILED_PRECONDITION):
                raise JobAlreadyDeactivatedError(job_key=job_key) from grpc_error
            await self._handle_grpc_error(grpc_error)

    async def throw_error(
            self, job_key: int, message: str, variables: Dict, error_code: str = ""
    ) -> ThrowErrorResponse:
        try:
            return await self._gateway_stub.ThrowError(
                ThrowErrorRequest(
                    jobKey=job_key,
                    errorMessage=message,
                    errorCode=error_code,
                    variables=json.dumps(variables),
                )
            )
        except grpc.aio.AioRpcError as grpc_error:
            if is_error_status(grpc_error, grpc.StatusCode.NOT_FOUND):
                raise JobNotFoundError(job_key=job_key) from grpc_error
            elif is_error_status(grpc_error, grpc.StatusCode.FAILED_PRECONDITION):
                raise JobAlreadyDeactivatedError(job_key=job_key) from grpc_error
            await self._handle_grpc_error(grpc_error)
