"""
    QuaO Project quao_cuda_quantum_device.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
import time
from ...data.device.circuit_running_option import CircuitRunningOption
from ...enum.status.job_status import JobStatus
from ...model.device.quao_device import QuaoDevice
from ...config.logging_config import logger


class QuaoCudaQuantumDevice(QuaoDevice):
    def _create_job(self, circuit, options: CircuitRunningOption):
        logger.debug('[Quao CUDA Quantum] Create job with {0} shots'.format(options.shots))

        start_time = time.time()

        job = self.device.sample(circuit, shots_count=options.shots)

        self.execution_time = time.time() - start_time

        return job

    def _produce_histogram_data(self, job_result) -> dict | None:
        logger.debug('[Quao CUDA Quantum] Produce histogram')

        return None

    def _get_provider_job_id(self, job) -> str:
        logger.debug('[Quao CUDA Quantum] Get provider job id')

        import uuid
        return str(uuid.uuid4())

    def _get_job_status(self, job) -> str:
        logger.debug('[Quao CUDA Quantum] Get job status')

        return JobStatus.DONE.value

    def _get_job_result(self, job):
        logger.debug('[Quao CUDA Quantum] Get job result')

        return job
