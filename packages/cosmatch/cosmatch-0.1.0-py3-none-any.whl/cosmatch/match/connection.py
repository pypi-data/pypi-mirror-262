"""Module for correlation several dataframes to one frame."""

import pandas as pd
import numpy as np

from ..utils import add_postfix_to_main_columns, get_id_ra_dec_col, find_all_id_cols
from ..utils import correlate, keep_nearest_pairs

from typing import List


def connection_table_nearest(df_main: pd.DataFrame, df_sub: pd.DataFrame, max_dist: float = 0.5,
                             keep_distance: bool = True) -> pd.DataFrame:
    """
    Correlate two dataframes and keep nearest pairs to all sources in df_main.

    Args:
        df_main: Main dataframe with sources.
        df_sub: Sub dataframe with sources.
        max_dist: Maximum distance between sources in df_main and df_sub.
        keep_distance: Keep distance between sources in df_main and df_sub in the output.

    Returns:
        Correlated dataframe with columns id_main, id_sub and (optional) distance. id_main is unique.
    """
    id_main, ra_main, dec_main = get_id_ra_dec_col(df_main)
    id_sub, ra_sub, dec_sub = get_id_ra_dec_col(df_sub)
    df_cor = correlate(df_main, df_sub, max_dist, (ra_main, dec_main), (ra_sub, dec_sub), add_distance=True)
    df_cor = keep_nearest_pairs(df_cor, id_main)
    # df_cor = keep_nearest_pairs(df_cor, id_main)
    col = [id_main, id_sub]
    if keep_distance:
        col.append('distance')
    return df_cor[col]


def connection_table_after_correlation(df_cor: pd.DataFrame, query: str = "P_0<0.05 and P_i>0.9 and flag_best==1",
                                       keep_distance: bool = True, make_unique: bool = False) -> pd.DataFrame:
    """
    Keep only best sources after smart-correlation.

    Args:
        df_cor: Correlated dataframe with columns ['P_i', 'P_0', 'flag_best'].
        query: Query for filtering.
        keep_distance: Keep distance between sources in df_main and df_sub in the output.
        make_unique: Make id_main unique. If after smart-correlation there are sources with several pairs with flag_best==1,\
            keep only one pair (it may be the result of duplicates in optical catalog).
    Returns:
        Correlated dataframe with columns id_main, id_sub and (optional) distance.
    """
    df = df_cor.query(query)
    col = find_all_id_cols(df)
    if keep_distance:
        col.append('distance')
    if make_unique:
        df = df.sort_values('P_i', ascending=False).drop_duplicates(subset=['id_opt'], keep='first').reset_index(drop=True)
    return df[col].reset_index(drop=True)


def join_connection_table(df: pd.DataFrame, connection_df: pd.DataFrame, joined_id: str, outer_id: str) -> pd.DataFrame:
    """
    Join dataset of sources into connection table.

    TODO.
    """
    joined_inner = df.join(connection_df.set_index(joined_id), on=joined_id, how='inner')
    joined_outer = df[~df[joined_id].isin(joined_inner[joined_id])]
    joined_outer[outer_id] = -1
    joined = pd.concat([joined_inner, joined_outer])
    return joined


def make_frame(connection_tables: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Create frame table with id_main and all other id in df in list.

    To make the frame, all connection table should contain one same column with id of sources (name of the columns should be the same).
    """
    intersection = set(connection_tables[0].columns)
    for i in connection_tables[1:]:
        intersection = intersection.intersection(i)
    id_main = list(intersection)[0]

    ids = {item for table in connection_tables for item in table[id_main]}

    frame = pd.DataFrame({id_main: list(ids)})
    for table in connection_tables:
        id_cols = find_all_id_cols(table)
        id_sub = id_cols[0] if id_cols[0] != id_main else id_cols[1]
        frame = join_connection_table(frame, table, id_main, id_sub)
    return frame


def join_df_in_frame(frame: pd.DataFrame, dfs: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Join all df in list in frame.

    Frame should contain id columns of all df.

    Args:
        frame: Frame with id columns.
        dfs: List of dataframes. Each df should contain id column, which is presented in frame.
    """
    for df in dfs:
        id_in_df = find_all_id_cols(df)[0]
        frame = pd.merge(frame, df, on=id_in_df, how='left')
    return frame

def mark_object_in_catalog(df_main: pd.DataFrame, catalog: pd.DataFrame, distance: float=0.2, hist=False) -> pd.DataFrame:
    """
    Mark rows with sources, which are represented in the second catalog (near the objects from this catalog).

    Args:
        df_main: Dataframe with sources, where is_in attribute will be added. Attrs: ['id', 'ra', 'dec', 'name']
        catalog: Catalog with sources, near which will be marked. Attrs: ['id', 'ra', 'dec', 'name']
        distance: Distance in degrees to find pairs.
    Returns:
        df_main with new column is_in_{catalog.attrs['name']}. Attrs: ['id', 'ra', 'dec', 'name'] + ['is_in']
    Note:
        df_main will be modified in place. New column is_in_{catalog.attrs['name']} will be added.
    """
    cor = correlate(df_main, catalog, distance, add_distance=True)
    cor.distance.hist(bins=min(100, len(cor))) if hist else None
    df_main['is_in_'+catalog.attrs['name']] = df_main[df_main.attrs['id']].isin(cor[df_main.attrs['id']])

    df_main.attrs['is_in'] = [] if 'is_in' not in df_main.attrs else df_main.attrs['is_in'] + [catalog.attrs['name']]
    df_main.attrs['is_in'] = list(set(df_main.attrs['is_in']))

    return df_main
