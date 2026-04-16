import pandas as pd
import xdmod_data._utilities as _utilities
import xdmod_data._validator as _validator


class _Descriptor:
    def __init__(self, http_requester):
        self.__http_requester = http_requester
        self.__cached = None

    def _get_data_frame(
        self,
        data_type,
        realm=None,
        drop_deprecated_names_column=True,
    ):
        if self.__cached is None:
            self.__cached = self._request(self.__http_requester)
        if realm is not None:
            realm_id = self._get_data_id('realms', realm)
        descriptor = self.__cached
        if data_type != 'realms':
            descriptor = descriptor[realm_id][data_type]
        data_frame = pd.DataFrame.from_dict(
            descriptor,
            orient='index',
            dtype='string',
        )
        if data_type == 'realms':
            data_frame = data_frame['label'].to_frame()
        data_frame = data_frame.rename_axis('id')
        if drop_deprecated_names_column:
            data_frame = data_frame.drop(
                columns='deprecated_names',
                errors='ignore',
            )
        return data_frame

    def _get_data_id(self, data_type, value, realm=None):
        data_type_label = data_type.rstrip('s')
        _validator._assert_str(data_type_label, value)
        if isinstance(self, _RawDescriptor):
            data_type_label = f'raw {data_type_label}'
        data_frame = self._get_data_frame(
            data_type,
            realm,
            drop_deprecated_names_column=False,
        )
        data_id = _utilities._get_id_from_data_frame(
            value,
            data_frame,
            data_type_label,
            realm,
        )
        if data_id is None:
            realm_text = (
                f' in the "{realm}" realm' if realm is not None else ''
            )
            raise KeyError(
                f'Value for `{data_type_label}` is unknown{realm_text}:'
                f' "{value}"',
            ) from None
        return data_id

    def _get_label_from_id(self, data_type, data_id, realm=None):
        if data_type == 'dimensions' and data_id == 'none':
            return None
        data_frame = self._get_data_frame(data_type, realm)
        return data_frame.loc[data_id, 'label']


class _AggregateDescriptor(_Descriptor):
    def _request(self, http_requester):
        response = http_requester._request_json(
            '/controllers/metric_explorer.php',
            {'operation': 'get_dw_descripter'},
        )
        if response['totalCount'] != 1:  # pragma: no cover
            raise RuntimeError(
                'Descriptor received with unexpected structure.',
            )
        serialized_descriptor = response['data'][0]['realms']
        result = {}
        for realm in serialized_descriptor:
            result[realm] = {'label': serialized_descriptor[realm]['category']}
            for m_or_d in ('metrics', 'dimensions'):
                m_or_d_descriptor = serialized_descriptor[realm][m_or_d]
                result[realm][m_or_d] = {}
                for id_ in m_or_d_descriptor:
                    result[realm][m_or_d][id_] = {
                        'label': m_or_d_descriptor[id_]['text'],
                        'description': m_or_d_descriptor[id_]['info'],
                    }
        return result


class _RawDescriptor(_Descriptor):
    def _request(self, http_requester):
        response = http_requester._request_json(
            '/rest/v1/warehouse/export/realms',
        )
        serialized_descriptor = response['data']
        result = {}
        for realm in serialized_descriptor:
            realm_id = realm['id']
            result[realm_id] = {'label': realm['name']}
            result[realm_id]['fields'] = {}
            fields = realm['fields']
            for field in fields:
                r = {
                    'label': field['display'],
                    'description': field['documentation'],
                }
                if 'deprecatedNames' in field:
                    r['deprecated_names'] = field['deprecatedNames']
                result[realm_id]['fields'][field['alias']] = r
        return result
