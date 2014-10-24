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
    def __init__(self, worker, exec_func, lock=None, blocking=False, worker_func_name='apply_async',
                 *exec_func_args, **exec_func_kwargs):
        """
        Template class for various mri processing tasks

        :param worker: worker thread or pool to execute the job. Must implement apply() and apply_async()
        :param exec_func: function to be executed by worker
        :param lock: optional lock to acquire before executing the job
        :param blocking: blocking parameter for lock
        :param worker_func_name: function (name) for worker to pass exec_func, exec_func_args, and exec_func_kwargs
        :param exec_func_args: non-keyword args for exec_func
        :param exec_func_kwargs: keyword args for exec_func
        """
        self.worker = worker
        self.exec_func = exec_func
        self.lock = lock
        self.blocking = blocking
        self.worker_func = getattr(worker, worker_func_name)
        self.exec_func_args = exec_func_args
        self.exec_func_kwargs = exec_func_kwargs

    def run(self):
        raise NotImplementedError('Must implement run() when inheriting MriJob')


class TransferJob(MriJob):

    def run(self):
        pass


class ProcessingJob(MriJob):

    def run(self):
        pass


class ConversionJob(MriJob):

    def run(self):
        pass


class MultiJob(MriJob):

    def run(self):
        pass