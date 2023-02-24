import pandas
import pytest
import xdmod.datawarehouse as xdw


class TestDataWarehouse:
    __INVALID_STR = 'asdlkfjsdlkfisdjkfjd'
    __VALID_DATE = '2020-01-01'
    __VALID_DIMENSION = 'allocation'
    __VALID_REALM = 'Jobs'
    __VALID_XDMOD_URL = 'https://xdmod-dev.ccr.xdmod.org'

    @pytest.fixture
    def valid_dw(self):
        yield xdw.DataWarehouse(self.__VALID_XDMOD_URL)

    def test_get_aggregate_data_KeyError_duration(self, valid_dw):
        with valid_dw:
            with pytest.raises(KeyError, match='Invalid value for `duration`'):
                valid_dw.get_aggregate_data(duration=self.__INVALID_STR)

    def test_get_aggregate_data_KeyError_realm(self, valid_dw):
        with valid_dw:
            with pytest.raises(KeyError, match='Invalid realm'):
                valid_dw.get_aggregate_data(realm=self.__INVALID_STR)

    def test_get_aggregate_data_KeyError_metric(self, valid_dw):
        with valid_dw:
            with pytest.raises(KeyError, match='not found in metrics'):
                valid_dw.get_aggregate_data(metric=self.__INVALID_STR)

    def test_get_aggregate_data_KeyError_dimension(self, valid_dw):
        with valid_dw:
            with pytest.raises(KeyError, match='not found in dimensions'):
                valid_dw.get_aggregate_data(dimension=self.__INVALID_STR)

    def test_get_aggregate_data_KeyError_filter_key(self, valid_dw):
        with valid_dw:
            with pytest.raises(KeyError, match='not found in dimensions'):
                valid_dw.get_aggregate_data(
                    filters={self.__INVALID_STR: self.__INVALID_STR})

    def test_get_aggregate_data_KeyError_filter_value(self, valid_dw):
        with valid_dw:
            with pytest.raises(KeyError, match='Filter value'):
                valid_dw.get_aggregate_data(
                    filters={self.__VALID_DIMENSION: self.__INVALID_STR})

    def test_get_aggregate_data_KeyError_aggregation_unit(self, valid_dw):
        with valid_dw:
            with pytest.raises(
                    KeyError, match='Invalid value for `aggregation_unit`'):
                valid_dw.get_aggregate_data(
                    aggregation_unit=self.__INVALID_STR)

    def test_get_aggregate_data_RuntimeError_outside_context(self, valid_dw):
        with pytest.raises(
                RuntimeError, match='outside of the runtime context'):
            valid_dw.get_aggregate_data()

    def test_get_aggregate_data_RuntimeError_start_date_malformed(
            self, valid_dw):
        with valid_dw:
            with pytest.raises(
                    RuntimeError,
                    match='start_date param is not in the correct format'):
                valid_dw.get_aggregate_data(
                    duration=(self.__INVALID_STR, self.__VALID_DATE))

    def test_get_aggregate_data_RuntimeError_end_date_malformed(
            self, valid_dw):
        with valid_dw:
            with pytest.raises(
                    RuntimeError,
                    match='end_date param is not in the correct format'):
                valid_dw.get_aggregate_data(
                    duration=(self.__VALID_DATE, self.__INVALID_STR))

    def test_get_aggregate_data_TypeError_duration(self, valid_dw):
        with valid_dw:
            with pytest.raises(TypeError, match='duration'):
                valid_dw.get_aggregate_data(duration=1)

    def test_get_aggregate_data_TypeError_realm(self, valid_dw):
        with valid_dw:
            with pytest.raises(TypeError, match='realm'):
                valid_dw.get_aggregate_data(realm=1)

    def test_get_aggregate_data_TypeError_metric(self, valid_dw):
        with valid_dw:
            with pytest.raises(TypeError, match='metric'):
                valid_dw.get_aggregate_data(metric=1)

    def test_get_aggregate_data_TypeError_dimension(self, valid_dw):
        with valid_dw:
            with pytest.raises(TypeError, match='dimension'):
                valid_dw.get_aggregate_data(dimension=1)

    def test_get_aggregate_data_TypeError_filters(self, valid_dw):
        with valid_dw:
            with pytest.raises(TypeError, match='filters'):
                valid_dw.get_aggregate_data(filters=1)

    def test_get_aggregate_data_TypeError_filter_key(self, valid_dw):
        with valid_dw:
            with pytest.raises(TypeError, match='filters'):
                valid_dw.get_aggregate_data(filters={2: self.__INVALID_STR})

    def test_get_aggregate_data_TypeError_filter_value(self, valid_dw):
        with valid_dw:
            with pytest.raises(TypeError, match='filters'):
                valid_dw.get_aggregate_data(
                    filters={self.__VALID_DIMENSION: 2})

    def test_get_aggregate_data_TypeError_timeseries(self, valid_dw):
        with valid_dw:
            with pytest.raises(TypeError, match='timeseries'):
                valid_dw.get_aggregate_data(timeseries=1)

    def test_get_aggregate_data_TypeError_aggregation_unit(self, valid_dw):
        with valid_dw:
            with pytest.raises(TypeError, match='aggregation_unit'):
                valid_dw.get_aggregate_data(aggregation_unit=1)

    def test_get_aggregate_data_ValueError_duration(self, valid_dw):
        with valid_dw:
            with pytest.raises(ValueError, match='duration'):
                valid_dw.get_aggregate_data(duration=('1', '2', '3'))

    def test_get_realms_return_type(self, valid_dw):
        with valid_dw:
            assert isinstance(
                valid_dw.get_realms(), pandas.core.frame.DataFrame)

    def test_get_realms_RuntimeError_outside_context(self, valid_dw):
        with pytest.raises(
                RuntimeError, match='outside of the runtime context'):
            valid_dw.get_realms()

    def test_get_metrics_return_type(self, valid_dw):
        with valid_dw:
            assert isinstance(
                valid_dw.get_metrics(self.__VALID_REALM),
                pandas.core.frame.DataFrame)

    def test_get_metrics_KeyError(self, valid_dw):
        with valid_dw:
            with pytest.raises(KeyError, match='Invalid realm'):
                valid_dw.get_metrics(self.__INVALID_STR)

    def test_get_metrics_RuntimeError_outside_context(self, valid_dw):
        with pytest.raises(
                RuntimeError, match='outside of the runtime context'):
            valid_dw.get_metrics(self.__VALID_REALM)

    def test_get_metrics_TypeError(self, valid_dw):
        with valid_dw:
            with pytest.raises(TypeError, match='realm'):
                valid_dw.get_metrics(2)

    def test_get_dimensions_return_type(self, valid_dw):
        with valid_dw:
            assert isinstance(
                valid_dw.get_dimensions(self.__VALID_REALM),
                pandas.core.frame.DataFrame)

    def test_get_dimensions_KeyError(self, valid_dw):
        with valid_dw:
            with pytest.raises(KeyError, match='Invalid realm'):
                valid_dw.get_dimensions(self.__INVALID_STR)

    def test_get_dimensions_RuntimeError_outside_context(self, valid_dw):
        with pytest.raises(RuntimeError, match='runtime context'):
            valid_dw.get_dimensions(self.__VALID_REALM)

    def test_get_dimensions_TypeError(self, valid_dw):
        with valid_dw:
            with pytest.raises(TypeError, match='realm'):
                valid_dw.get_dimensions(2)

    def test_get_valid_values_KeyError(self, valid_dw):
        with valid_dw:
            with pytest.raises(
                    KeyError,
                    match='Parameter \'' + self.__INVALID_STR
                    + '\' does not have a list of valid values.'):
                valid_dw.get_valid_values(self.__INVALID_STR)

    def test_get_valid_values_TypeError(self, valid_dw):
        with valid_dw:
            with pytest.raises(
                    TypeError, match='`parameter` must be a string.'):
                valid_dw.get_valid_values(2)
