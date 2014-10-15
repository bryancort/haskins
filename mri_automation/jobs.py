# -------------------------------------------------------------------------------
# Name:        mri_automation.jobs
# Purpose:      Classes for discreet parallelizable processing jobs
#
# Author:      Bryan Cort
#
# Created:     08/10/2014
# -------------------------------------------------------------------------------


import multiprocessing as mp


class MriJob:
    def __init__(self, worker, exec_func, lock=None, blocking=False, worker_func=mp.apply_async, ):
        """

        :param worker: worker thread or pool to execute the job. Must implement apply() and apply_async()
        :param exec_func: function to be executed by worker
        :param lock: optional lock to acquire before executing the job
        :param blocking: blocking parameter for lock
        :param worker_func: function for worker to execute the job with
        """
        self.worker = worker
        self.exec_func = exec_func
        self.lock = lock
        self.blocking = blocking
        self.worker_func = worker_func

    def run(self):
        raise NotImplementedError('Method not implemented in parent')


class TransferJob(MriJob):
    def __init__(self):
        MriJob.__init__(self)

    def run(self):
        pass


class ProcessingJob(MriJob):
    def __init__(self):
        MriJob.__init__(self)

    def run(self):
        pass


class ConversionJob(MriJob):
    def __init__(self):
        MriJob.__init__(self)

    def run(self):
        pass


class MultiJob(MriJob):
    def __init__(self, ):
        MriJob.__init__(self)

    def run(self):
        pass