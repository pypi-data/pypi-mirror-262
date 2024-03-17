"""Modul for loading data from Vizier."""

from astroquery.vizier import Vizier
import astropy.coordinates as coord
import astropy.units as u

import pandas as pd
import numpy as np
import os

import requests  # type: ignore
import urllib
import json

from abc import ABC, abstractmethod

from ..utils import local_package_path

from typing import Union


class Retriever(ABC):
    """Abstract class for finding near pairs of object from Vizier.

    To implement this class, you need to define the following methods: __init__

    In this method you should:
        - set the path to the catalog from vizier
        - set the columns to load from catalog
        - set the description of columns (optional)
    """

    def __init__(self) -> None:
        """Initialize the class. You should implement this method in your class."""
        self.path: str  # name of catalog in Vizier
        self.columns: Union[dict[str, str], list[str]]  # list of columns in catalog or dict of {column_in_catalog: more_clear_name}
        self.about_columns: Union[dict[str, str], None] = None  # description of columns

    def load_data(self, sourses: pd.DataFrame, columns: list[str] = ['*'], radius_arcsec: float = 10,
                  verbose: bool = False, window: int = 100) -> pd.DataFrame:
        """
        Load data from Vizier.

        Args:
            sourses: catalog of objects with coordinates [ra, dec]
            columns: list of columns to load from catalog. To get available columns, use available_columns().\
                  To load all columns, use ['*']
            radius_arcsec: radius of search in arcsec.
            verbose: if True, print progress.
            window: number of sources to load at once.
        Returns:
            Dataframe with loaded data.
        Note:
            This method generate temporary files for loading data. It also save data.
        """
        if columns == ['*']:
            columns = self.available_columns()
        columns = self._rename_columns(columns)

        if not os.path.exists('tmp_load_data'):
            os.mkdir('tmp_load_data')
        for num in range(len(sourses) // window + 1):
            coords = coord.SkyCoord(ra=list(sourses.ra.values[num * window:(num + 1) * window]),
                                    dec=list(sourses.dec.values[num * window:(num + 1) * window]), unit=(u.deg, u.deg))
            radius = radius_arcsec * u.arcsec

            if verbose:
                print(f"{num} start...", end=' ')
            panstarrs = Vizier(columns=columns, catalog=self.path).query_region(coords, radius=radius)
            if verbose:
                print(f"get...", end=' ')

            for i, result in enumerate(panstarrs):
                neighbors = result[columns]
                neighbors = pd.DataFrame(np.array(neighbors), columns=columns)
                neighbors.to_csv(f'tmp_load_data/{num}.csv', index=False)

            if verbose:
                print(f"{num*window} object finished!", end='\n')

        print('Data collected successfully. Start to merge.')

        df = pd.concat([pd.read_csv(f'tmp_load_data/{num}.csv') for num in range(len(sourses) // window + 1)])

        df.columns = self._unrename_columns(df.columns)
        df.to_csv(f'merged_{len(df)}.csv', index=False)
        print(f'Data merged successfully. It saved as merged_{len(df)}.csv')

        return df

    def available_columns(self) -> list[str]:
        """Get available columns to load."""
        if isinstance(self.columns, dict):
            return list(self.columns.values())
        else:
            return self.columns

    def _rename_columns(self, columns: list[str]) -> list[str]:
        """Rename columns to vizier columns."""
        if isinstance(self.columns, dict):
            dict_ = {val: key for key, val in self.columns.items()}
            for col in columns:
                if col not in dict_:
                    raise KeyError(f'{col} should be in columns. Available columns: {self.available_columns()}')
            return [dict_[col] for col in columns]
        else:
            for col in columns:
                if col not in self.columns:
                    raise KeyError(f'{col} should be in columns. Available columns: {self.available_columns()}')
            return columns

    def _unrename_columns(self, columns: list[str]) -> list[str]:
        """Reverse method for renaming vizier columns to clear columns."""
        if isinstance(self.columns, dict):
            return [self.columns[col] for col in columns]
        else:
            return columns

    def about(self) -> str:
        """Get description of columns. If you haven't implemented self.about_columns, it will return 'About was not implemented yet."""
        if self.about_columns is None:
            return "About was not implemented yet."
        return str(self.about_columns)


class PS1(Retriever):
    """Class for loading PanSTARRS DR1."""

    def __init__(self) -> None:
        """Init."""
        self.path = 'II/349/ps1'
        self.columns = {"objID": 'id', 'RAJ2000': 'ra', 'DEJ2000': 'dec',
                        'rmag': 'rPsfMag', 'e_rmag': 'rPsfMagErr', 'rKmag': 'rKronMag', 'e_rKmag': 'rKronMagErr',
                        'ymag': 'yPsfMag', 'e_ymag': 'yPsfMagErr', 'yKmag': 'yKronMag', 'e_yKmag': 'yKronMagErr',
                        'zmag': 'zPsfMag', 'e_zmag': 'zPsfMagErr', 'zKmag': 'zKronMag', 'e_zKmag': 'zKronMagErr',
                        'imag': 'iPsfMag', 'e_imag': 'iPsfMagErr', 'iKmag': 'iKronMag', 'e_iKmag': 'iKronMagErr',
                        'gmag': 'gPsfMag', 'e_gmag': 'gPsfMagErr', 'gKmag': 'gKronMag', 'e_gKmag': 'gKronMagErr', }
        self.about_columns = {'id': "Id of the object",
                              'RAJ2000': "Right ascension",
                              'DEJ2000': "Declination",
                              'gPsfMag': "Mean PSF magnitude from g filter",
                              'gPsfMagErr': "Uncertainty in g magnitude from g filter",
                              'gKronMag': "Mean Kron magnitude from g filter detections",
                              'gKronMagErr': "Uncertainty in Kron magnitude from g filter",
                              'rPsfMag': "Mean PSF magnitude from r filter",
                              'rPsfMagErr': "Uncertainty in r magnitude from r filter",
                              'rKronMag': "Mean Kron magnitude from r filter",
                              'rKronMagErr': "Uncertainty in Kron magnitude from r filter",
                              'iPsfMag': "Mean PSF magnitude from i filter",
                              'iPsfMagErr': "Uncertainty in i magnitude from i filter",
                              'iKronMag': "Mean Kron magnitude from i filter",
                              'iKronMagErr': "Uncertainty in Kron magnitude from i filter",
                              'zPsfMag': "Mean PSF magnitude from z filter",
                              'zPsfMagErr': "Uncertainty in i magnitude from z filter",
                              'zKmag': "Mean Kron magnitude from z filter",
                              'zKronMagErr': "Uncertainty in Kron magnitude from z filter",
                              'yPsfMag': "Mean PSF magnitude from y filter",
                              'yPsfMagErr': "Uncertainty in y magnitude from y filter",
                              'yKronMag': "Mean Kron magnitude from y filter",
                              'yKronMagErr': "Uncertainty in Kron magnitude from y filter"}


class Gaia(Retriever):
    """Class for loading GAIA DR3."""

    def __init__(self) -> None:
        """Init."""
        self.path = 'I/355/gaiadr3'
        self.columns = {'Source': 'id', 'RA_ICRS': 'ra', 'DE_ICRS': 'dec',
                        'Plx': 'paralax', 'e_Plx': 'paralaxErr',
                        'Gmag': 'gMag', 'e_Gmag': 'gMagErr',
                        'BPmag': 'bpMag', 'e_BPmag': 'bpMagErr',
                        'RPmag': 'rpMag', 'e_RPmag': 'rpMagErr', }


class CatalogLoader:
    """Class for loading catalogs from yandex disk."""

    def __init__(self, file_name: str) -> None:
        """Init."""
        self.folder_link = 'https://disk.yandex.ru/d/dxNUCwXCW5_mHg'
        self.path_to_save = local_package_path(f'downloaded_catalogues/{file_name.replace("/","_")}')
        self.file_name = file_name
        self.columns: Union[dict, None] = None
        self.str_about: Union[str, None] = None

    def _load_file(self) -> pd.DataFrame:
        """Download file."""
        url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download' + '?public_key='\
              + urllib.parse.quote(self.folder_link) + '&path=/' + urllib.parse.quote(self.file_name)

        r = requests.get(url)  # запрос ссылки на скачивание
        h = json.loads(r.text)['href']  # 'парсинг' ссылки на скачивание
        return pd.read_pickle(h)

    def remove(self) -> None:
        """Delete file from local environment."""
        if os.path.exists(self.path_to_save):
            print(f'File {self.path_to_save} already exists. Removing...')
            os.remove(self.path_to_save)

    def load(self, force: bool = False) -> pd.DataFrame:
        """Download file if in local environment it does not exist."""
        if os.path.exists(self.path_to_save) and not force:
            print(f'File {self.path_to_save} already exists. Loading...')
            return pd.read_pickle(self.path_to_save)

        print(f'File {self.path_to_save} does not exist. Downloading...')
        df = self._load_file()
        df.to_pickle(self.path_to_save)

        return df

    def about(self) -> str:
        """Get description of columns. If you haven't implemented self.about_columns, it will return 'About was not implemented yet."""
        if self.str_about is None:
            return "About was not implemented yet."
        return self.str_about


class CSC2(CatalogLoader):
    """Class for download CSC2 as support catalogue to teach model of correlation."""

    def __init__(self) -> None:
        """Init."""
        super().__init__('CSC2.pkl')


class DESI(CatalogLoader):
    """Class for download DESI LIS, in which DESI classes are stored. Needed for teach model of classification."""

    def __init__(self) -> None:
        """Init."""
        super().__init__('DESI_classes.pkl')


# Переодически бывают ошибки в скачивании данных. Надо пробовать несколько раз


def clear_downloaded_files() -> None:
    """Delete all files in local folder."""
    for file in os.listdir(local_package_path('downloaded_catalogues')):
        if file.endswith('.pkl'):
            os.remove(local_package_path(f'downloaded_catalogues/{file}'))


def download_vizier_catalog(catalog_keyword: str, columns: list[str] = ['**']) -> pd.DataFrame:
    """Download whole catalog from Vizier with specified columns."""
    data = Vizier(columns=columns,
                  catalog=catalog_keyword,
                  row_limit=-1).get_catalogs(catalog=catalog_keyword)[0]
    data = data.to_pandas()
    return data
