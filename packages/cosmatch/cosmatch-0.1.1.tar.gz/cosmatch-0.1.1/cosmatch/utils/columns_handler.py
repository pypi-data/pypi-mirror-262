import pandas as pd

from typing import List, Union


def add_postfix_to_main_columns(df: pd.DataFrame, postfix: Union[str, None], add_to_attrs: bool = True) -> None:
    """
    Добавляет к имени колонок id, ra, dec постфикс postfix. Также позволяет добавить атрибуты ['name', 'id', 'ra', 'dec'].
    
    Args:
        df: DataFrame, к которому добавляются постфиксы. Columns = ['id', 'ra', 'dec']
        postfix: Постфикс для добавляемых колонок. Может быть None,\
            тогда колонки не переименовываются, но атрибуты могут добавиться
        add_to_attrs: Если True, то добавляются атрибуты ['name', 'id', 'ra', 'dec'].

    Examples:
        Важно обратить внимание, что для работы функции в наборе данных должны быть строго колонки ['id', 'ra', 'dec'].

        >>> import pandas as pd
        >>> from cosmatch.utils import add_postfix_to_main_columns
        >>>
        >>> frame = pd.DataFrame({'id': [1, 2, 3, 4, 5], 
        ...                       'ra': [1, 2, 3, 4, 5], 
        ...                       'dec': [1, 2, 3, 4, 5]})
        >>> add_postfix_to_main_columns(frame, postfix='frame', add_to_attrs=True)
        >>> frame.columns
        Index(['id_frame', 'ra_frame', 'dec_frame'], dtype='object')
        >>> frame.attrs
        {'name': 'frame', 'id': 'id_frame', 'ra': 'ra_frame', 'dec': 'dec_frame'}

        В случае передачи постфикса None, то атрибуты добавляются, но колонки не переименовываются.

        >>> frame = pd.DataFrame({'id': [1, 2, 3, 4, 5],
        ...                       'ra': [1, 2, 3, 4, 5],
        ...                       'dec': [1, 2, 3, 4, 5]})
        >>> add_postfix_to_main_columns(frame, postfix=None, add_to_attrs=True)
        >>> frame.columns
        Index(['id', 'ra', 'dec'], dtype='object')
        >>> frame.attrs
        {'name': '', 'id': 'id', 'ra': 'ra', 'dec': 'dec'} 
    """
    if postfix is not None:
        df.rename(columns={'id': f'id_{postfix}', 'ra': f'ra_{postfix}',
                        'dec': f'dec_{postfix}'}, inplace=True)
        if add_to_attrs:
            df.attrs['name'] = postfix
            df.attrs['id'] = f'id_{postfix}'
            df.attrs['ra'] = f'ra_{postfix}'
            df.attrs['dec'] = f'dec_{postfix}'
    else:
        if add_to_attrs:
            df.attrs['name'] = ''
            df.attrs['id'] = 'id'
            df.attrs['ra'] = 'ra'
            df.attrs['dec'] = 'dec'

def unite_attrs_from_frame_and_target(df: pd.DataFrame, frame: pd.DataFrame, target: pd.DataFrame) -> None:
    check_attrs_structure(frame, ['name', 'id', 'ra', 'dec'])
    check_attrs_structure(target, ['name', 'id', 'ra', 'dec'])
    df.attrs['ids'] = [frame.attrs['id'], target.attrs['id']]
    df.attrs['coords'] = [frame.attrs['ra'], frame.attrs['dec'], target.attrs['ra'], target.attrs['dec']]

    df.attrs['name_frame'] = frame.attrs['name']
    df.attrs['id_frame'] = frame.attrs['id']
    df.attrs['ra_frame'] = frame.attrs['ra']
    df.attrs['dec_frame'] = frame.attrs['dec']

    df.attrs['name_target'] = target.attrs['name']
    df.attrs['id_target'] = target.attrs['id']
    df.attrs['ra_target'] = target.attrs['ra']
    df.attrs['dec_target'] = target.attrs['dec']

def check_attrs_structure(df: pd.DataFrame, keys: list[str]=['id', 'ra', 'dec']) -> None:
    """Проверяет структуру атрибутов в df."""
    for key in keys:
        if key not in df.attrs:
            raise ValueError(f'{key} not in attrs. To use correlation module you should add {key} in attrs.')
        
def get_attrs_columns(df: pd.DataFrame, keys: list[str]=['id', 'ra', 'dec']) -> list[str]:
    """Возвращает список атрибутов в df."""
    return [df.attrs[key] for key in keys]


# Legacy
def find_all_id_cols(df: pd.DataFrame) -> List[str]:
    """Возвращает все колонки, которые начинаются на id."""
    return list(filter(lambda x: 'id_' in x, df.columns))

# Legacy
def get_id_ra_dec_col(df: pd.DataFrame) -> List[str]:
    """Возвращает колонки id, ra, dec из каталога. В нем не можно быть нескольких этих колонок."""
    filtered = list(filter(lambda x: 'id_' in x, df.columns))
    if len(filtered) == 0:
        raise Exception('Id column not found')
    if len(filtered) > 1:
        raise Exception('In catalog more than one id column')
    postfix = filtered[0].replace('id_', '')
    ans = [f'id_{postfix}', f'ra_{postfix}', f'dec_{postfix}']
    for i in ans:
        if i not in df.columns:
            raise Exception(f'{i} not found')
    return [f'id_{postfix}', f'ra_{postfix}', f'dec_{postfix}']