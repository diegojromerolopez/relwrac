from typing import Dict, Set


class StopCondition(object):
    @classmethod
    def depth_is_reached(cls, max_depth: int):
        def stop_condition(depth: int, _link_adj: Dict[str, Set[str]]):
            return depth >= max_depth

        return stop_condition
