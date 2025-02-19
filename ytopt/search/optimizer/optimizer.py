from sys import float_info

import numpy as np
from numpy import inf
from skopt import Optimizer as SkOptimizer

from ytopt.search import util

logger = util.conf_logger('ytopt.search.hps.optimizer.optimizer')

class Optimizer:
    SEED = 12345
    KAPPA = 1.96

    def __init__(self, num_workers: int, space, learner, acq_func, liar_strategy, **kwargs):
        assert learner in ["RF", "ET", "GBRT", "GP", "DUMMY"], f"Unknown scikit-optimize base_estimator: {learner}"
        assert liar_strategy in "cl_min cl_mean cl_max".split()


        self.space = space
        self.learner = learner
        self.acq_func = acq_func
        self.liar_strategy = liar_strategy

        n_init = inf if learner=='DUMMY' else num_workers

        self._optimizer = SkOptimizer(
            dimensions=self.space.dimensions,
            base_estimator=self.learner,
            acq_optimizer='sampling',
            acq_func=self.acq_func,
            acq_func_kwargs={'kappa':self.KAPPA},
            random_state=self.SEED,
            n_initial_points=n_init
        )

        self.evals = {}
        self.counter = 0
        logger.info("Using skopt.Optimizer with %s base_estimator" % self.learner)

    def _get_lie(self):
        if self.liar_strategy == "cl_min":
            return min(self._optimizer.yi) if self._optimizer.yi else 0.0
        elif self.liar_strategy == "cl_mean":
            return np.mean(self._optimizer.yi) if self._optimizer.yi else 0.0
        else:
            return  max(self._optimizer.yi) if self._optimizer.yi else 0.0

    def _xy_from_dict(self):
        XX = list(self.evals.keys())
        YY = [self.evals[x] for x in XX]
        return XX, YY

    def to_dict(self, x: list) -> dict:
        return self.space.to_dict(x)

    def _ask(self):
        x = self._optimizer.ask()
        y = self._get_lie()
        key = tuple(x)
        if key not in self.evals:
            self.counter += 1
            self._optimizer.tell(x,y)
            self.evals[key] = y
            logger.debug(f'_ask: {x} lie: {y}')
        else:
            logger.debug(f'Duplicate _ask: {x} lie: {y}')
        return self.to_dict(x)

    def ask(self, n_points=None, batch_size=20):
        if n_points is None:
            return self._ask()
        else:
            batch = []
            for _ in range(n_points):
                batch.append(self._ask())
                if len(batch) == batch_size:
                    yield batch
                    batch = []
            if batch:
                yield batch

    def ask_initial(self, n_points):
        XX = self._optimizer.ask(n_points=n_points)
        for x in XX:
            y = self._get_lie()
            key = tuple(x)
            if key not in self.evals:
                self.counter += 1
                self._optimizer.tell(x,y)
                self.evals[key] = y
        return [self.to_dict(x) for x in XX]

    def tell(self, xy_data):
        assert isinstance(xy_data, list), f"where type(xy_data)=={type(xy_data)}"
        maxval = max(self._optimizer.yi) if self._optimizer.yi else 0.0
        for x,y in xy_data:
            key = tuple(x.values()) # * tuple(x[k] for k in self.space)
            assert key in self.evals, f"where key=={key} and self.evals=={self.evals}"
            logger.debug(f'tell: {x} --> {key}: evaluated objective: {y}')
            self.evals[key] = (y if y < float_info.max else maxval)

        self._optimizer.Xi = []
        self._optimizer.yi = []
        XX, YY = self._xy_from_dict()
        assert len(XX) == len(YY) == self.counter, (
            f"where len(XX)=={len(XX)},"
            f"len(YY)=={len(YY)}, self.counter=={self.counter}")
        self._optimizer.tell(XX, YY)
        assert len(self._optimizer.Xi) == len(self._optimizer.yi) == self.counter, (
            f"where len(self._optimizer.Xi)=={len(self._optimizer.Xi)}, "
            f"len(self._optimizer.yi)=={len(self._optimizer.yi)},"
            f"self.counter=={self.counter}")
