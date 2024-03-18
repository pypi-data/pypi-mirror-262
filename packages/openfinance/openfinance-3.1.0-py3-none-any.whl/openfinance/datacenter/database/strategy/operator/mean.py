import numpy as np

from openfinance.datacenter.database.strategy.operator.base import Operator

class Mean(Operator):
    name: str = "Mean"

    def run(
        self,
        data,
        **kwargs
    ):
        """
            Function to evaluate specific stocks
        """
        period = kwargs.get("period", 4)
        v = []
        if True:
            for d in data[-period:]:
                if d[1] and d[1] != None:
                    v.append(d[1])
        else:
            v = data[-period:]
        # print(kwargs, v)
        slope = np.mean(v)
        return slope