# -------------------------------------------------------------------------------
# Name:        mri_automation.jobs
# Purpose:      Classes for discreet parallelizable processing jobs
#
# Author:      Bryan Cort
#
# Created:     08/10/2014
# -------------------------------------------------------------------------------




class MriJob:
    def __init__(self, lock=None):
        self.lock = lock

    def run(self):
        pass


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