"""Future module for classification of sources to different classes."""

import pandas as pd
import numpy as np
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import train_test_split

from .utils import correlate


def add_classes(data: pd.DataFrame, ignored: list, path_to_class: str = 'DS/LS/LS_class.pickle') -> pd.DataFrame:
    """Initial version of classification."""
    lis = pd.read_pickle(path_to_class)
    classes = correlate(data, lis, 0.3, ('ra_gaia', 'dec_gaia'), ('ra', 'dec'), add_distance=False)
    classes.drop(columns=['id', 'ra', 'dec'], inplace=True)

    X_train, X_test, y_train, y_test = train_test_split(classes.drop(columns=['spectype']), classes['spectype'], stratify=classes['spectype'], test_size=0.2)

    pool_train = Pool(X_train.drop(columns=ignored), y_train)
    pool_test = Pool(X_test.drop(columns=ignored), y_test)

    model = CatBoostClassifier(iterations=1000, depth=6, learning_rate=0.3,
                               loss_function='MultiClass',
                               eval_metric='TotalF1', early_stopping_rounds=50)
    model.fit(pool_train, eval_set=pool_test, verbose=False)

    predict = model.predict_proba(data.drop(columns=ignored))
    data['p_quasar'] = predict[:, 0]
    data['p_galaxy'] = predict[:, 1]
    data['p_star'] = predict[:, 2]
    return data
