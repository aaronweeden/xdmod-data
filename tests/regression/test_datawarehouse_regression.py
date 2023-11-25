import numpy
import os
from os.path import expanduser
import pandas
from pathlib import Path
import pytest
from xdmod_data.warehouse import DataWarehouse

XDMOD_URL = 'https://xdmod.access-ci.org'
TOKEN_PATH = '~/.xdmod-data-token'
DATA_DIR = os.path.dirname(__file__) + '/data'


with open(Path(expanduser(TOKEN_PATH)), 'r') as token_file:
    token = token_file.read().replace('\n', '').strip()
os.environ['XDMOD_API_TOKEN'] = token


@pytest.fixture(scope='module')
def valid_dw():
    with DataWarehouse(XDMOD_URL) as dw:
        yield dw


def __assert_dfs_equal(
    data_file,
    actual,
    dtype='object',
    index_col='id',
):
    expected = pandas.read_csv(
        DATA_DIR + '/' + data_file,
        dtype=dtype,
        index_col=index_col,
        keep_default_na=False,
        na_values=[''],
    ).fillna(numpy.nan)
    expected.columns = expected.columns.astype('string')
    assert expected.equals(actual)


def test_get_raw_data(valid_dw):
    data = valid_dw.get_raw_data(
        duration=('2023-05-01', '2023-05-02'),
        realm='SUPREMM',
        fields=(
            'CPU User',
            'Nodes',
            'Wall Time',
            'Wait Time',
            'Requested Wall Time',
            'Total memory used',
            'Mount point "home" data written',
            'Mount point "scratch" data written',
        ),
        filters={
            'Resource': [
                'STAMPEDE2 TACC',
                'Bridges 2 RM',
            ],
        },
    ).iloc[::1000]
    data.index = data.index.astype('string')
    __assert_dfs_equal(
        'machine-learning-notebook-example-every-1000.csv',
        data,
        dtype='string',
        index_col=0,
    )


def __assert_descriptor_dfs_equal(data_file, actual):
    __assert_dfs_equal(data_file, actual, 'string')


def test_get_realms(valid_dw):
    __assert_descriptor_dfs_equal(
        'realms.csv',
        valid_dw.get_realms(),
    )
    __assert_descriptor_dfs_equal(
        'realms.csv',
        valid_dw.describe_realms(),
    )


def test_get_metrics(valid_dw):
    __assert_descriptor_dfs_equal(
        'jobs-metrics.csv',
        valid_dw.get_metrics('Jobs'),
    )
    __assert_descriptor_dfs_equal(
        'jobs-metrics.csv',
        valid_dw.describe_metrics('Jobs'),
    )


def test_get_dimensions(valid_dw):
    __assert_descriptor_dfs_equal(
        'jobs-dimensions.csv',
        valid_dw.get_dimensions('Jobs'),
    )
    __assert_descriptor_dfs_equal(
        'jobs-dimensions.csv',
        valid_dw.describe_dimensions('Jobs'),
    )


def test_get_filter_values(valid_dw):
    __assert_descriptor_dfs_equal(
        'jobs-fieldofscience-filter-values.csv',
        valid_dw.get_filter_values('Jobs', 'Field of Science'),
    )
