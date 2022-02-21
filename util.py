from joblib import Parallel, delayed
import os
from tqdm import tqdm
import joblib
import subprocess
import contextlib
from typing import Tuple, Iterable, Set, List, Callable


@contextlib.contextmanager
def tqdm_joblib(tqdm_object):
    """Context manager to patch joblib to report into tqdm progress bar given as argument"""

    # credits:
    # https://stackoverflow.com/questions/24983493/tracking-progress-of-joblib-parallel-execution
    class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def __call__(self, *args, **kwargs):
            tqdm_object.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    old_batch_callback = joblib.parallel.BatchCompletionCallBack
    joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback
    try:
        yield tqdm_object
    finally:
        joblib.parallel.BatchCompletionCallBack = old_batch_callback
        tqdm_object.close()


def paral(function: Callable,
          iters: List[Iterable],
          num_cores=-1,
          progress_bar=True):
    """ compute function parallel with arguments in iters.
    function(iters[0][0],iters[0][1],...)"""

    with tqdm_joblib(
            tqdm(desc=function.__name__,
                 unit="jobs",
                 dynamic_ncols=True,
                 total=len(iters[0]),
                 disable=not progress_bar), ) as progress_bar:
        return Parallel(n_jobs=num_cores, batch_size=1)(delayed(function)(*its)
                                                        for its in zip(*iters))


def prep_dir(dir_name: str):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


def log(message: str):
    print(str(dt.now()) + "\t| " + message)
