from typing import List, Tuple, Dict
import pandas as pd
import numpy as np
import itertools

from simba.utils.checks import check_instance, check_valid_lst, check_that_column_exist
from simba.utils.errors import CountError

def spontaneous_alternations(data: pd.DataFrame,
                             shape_names: List[str]) -> Tuple[int, Dict[str, np.ndarray]]:
    """
    Detects spontaneous alternations between a set of user-defined ROIs.

    :param pd.DataFrame data: DataFrame containing shape data where each row represents a frame and each column represents a shape where 0 represents not in ROI and 1 represents inside the ROI
    :param pd.DataFrame data: List of column names in the DataFrame corresponding to shape names.
    :returns Dict[Union[str, Tuple[str], Union[int, float, List[int]]]]: Dict with the following keys and values:
            'pct_alternation': Percent alternation computed as spontaneous alternation cnt /(total number of arm entries − (number of arms - 1))} × 100
            'alternation_cnt': The sliding count of ROI entry sequences of len(shape_names) that are all unique.
            'same_arm_returns_cnt': Aggregate count of sequantial visits to the same ROI.
            'alternate_arm_returns_cnt': Aggregate count of errors which are not same-arm-return errors.
            'error_cnt': Aggregate error count (same_arm_returns_cnt + alternate_arm_returns_cnt),
            'same_arm_returns_dict': Dictionary with the keys being the name of the ROI and values are a list of frames when the same-arm-return errors where committed.
            'alternate_arm_returns_cnt': Dictionary with the keys being the name of the ROI and values are a list of frames when the alternate-arm-return errors where committed.
            'alternations_dict': Dictionary with the keys being unique ROI name tuple sequences of length len(shape_names) and values are a list of frames when the sequence was completed.

    :example:
    >>> data = np.zeros((100, 4), dtype=int)
    >>> random_indices = np.random.randint(0, 4, size=100)
    >>> for i in range(100): data[i, random_indices[i]] = 1
    >>> df = pd.DataFrame(data, columns=['left', 'top', 'right', 'bottom'])
    >>> spontanous_alternations = spontaneous_alternations(data=df, shape_names=['left', 'top', 'right', 'bottom'])
    """

    def get_sliding_alternation(data: np.ndarray) -> Tuple[Dict[int, List[int]], Dict[int, List[int]], Dict[Tuple[int], List[int]]]:
        alt_cnt, stride = 0, data.shape[1]-1
        arm_visits = np.full((data.shape[0]), -1)
        same_arm_returns, alternations, alternate_arm_returns = {}, {}, {}
        for i in range(data.shape[1]-1):  alternate_arm_returns[i], same_arm_returns[i] = [], []
        for i in list(itertools.permutations(list(range(0, data.shape[1]-1)))): alternations[i] = []
        for i in range(data.shape[0]): arm_visits[i] = np.argwhere(data[i, 1:] == 1).flatten()[0]
        for i in range(stride-1, arm_visits.shape[0]):
            current, priors = arm_visits[i], arm_visits[i-(stride-1):i]
            sequence = np.append(priors, [current])
            if np.unique(sequence).shape[0] == stride:
                alternations[tuple(sequence)].append(data[i, 0])
            else:
                if current == priors[-1]: same_arm_returns[current].append(data[i, 0])
                else: alternate_arm_returns[current].append(data[i, 0])
        return same_arm_returns, alternate_arm_returns, alternations

    check_instance(source=spontaneous_alternations.__name__, instance=data, accepted_types=(pd.DataFrame,))
    check_valid_lst(data=shape_names, source=spontaneous_alternations.__name__, valid_dtypes=(str,))
    for shape_name in shape_names: check_that_column_exist(df=data, column_name=shape_name, file_name='')
    data = data[shape_names]
    additional_vals = list(set(np.unique(data.values.flatten())) - {0, 1})
    if len(additional_vals) > 0:
        raise CountError(msg=f'When computing spontaneous alternation, ROI fields can only be 0 or 1. Found {additional_vals}', source=spontaneous_alternations.__name__)
    above_1_idx = np.argwhere(np.sum(data.values, axis=1) > 1)
    if above_1_idx.shape[0] > 0: raise CountError(msg=f'When computing spontaneous alternation, animals should only exist in <=1 ROIs in any one frame. In {above_1_idx.shape[0]} frames, the animal exist in more than one ROI.', source=spontaneous_alternations.__name__)
    shape_map = {}
    for i in range(len(shape_names)): shape_map[i] = shape_names[i]
    data = np.hstack((np.arange(0, data.shape[0]).reshape(-1, 1), data.values))
    data = data[np.sum(data, axis=1) != 0]
    data = data[np.concatenate(([0], np.where(~(data[:, 1:][1:] == data[:, 1:][:-1]).all(axis=1))[0] + 1))]
    same_arm, alternate_arm, alt = get_sliding_alternation(data=data)

    same_arm_returns, alternate_arm_returns = {}, {}
    for k, v in same_arm.items(): same_arm_returns[shape_map[k]] = v
    for k, v in alternate_arm.items(): alternate_arm_returns[shape_map[k]] = v
    alternations = {}
    for k, v in alt.items():
        new_k = []
        for i in k: new_k.append(shape_map[i])
        alternations[tuple(new_k)] = v

    same_arm_returns_cnt, alternation_cnt, alternate_arm_returns_cnt = 0, 0, 0
    for v in same_arm_returns.values():
        same_arm_returns_cnt += len(v)
    for v in alternate_arm_returns.values():
        alternate_arm_returns_cnt += len(v)
    for v in alternations.values(): alternation_cnt += len(v)
    pct_alternation = alternation_cnt / (data.shape[0] - (data.shape[1] -1))

    return {'pct_alternation': pct_alternation * 100,
           'alternation_cnt': alternation_cnt,
           'error_cnt': same_arm_returns_cnt + alternate_arm_returns_cnt,
           'same_arm_returns_cnt': same_arm_returns_cnt,
           'alternate_arm_returns_cnt': alternate_arm_returns_cnt,
           'same_arm_returns_dict': same_arm_returns,
           'alternate_arm_returns_dict': alternate_arm_returns,
           'alternations_dict': alternations}

# data = np.zeros((50, 4), dtype=int)
# random_indices = np.random.randint(0, 4, size=50)
# for i in range(50): data[i, random_indices[i]] = 1
# df = pd.DataFrame(data, columns=['left', 'top', 'right', 'bottom'])
# results = spontanous_alternation = spontaneous_alternations(data=df, shape_names=['left', 'top', 'right', 'bottom'])
