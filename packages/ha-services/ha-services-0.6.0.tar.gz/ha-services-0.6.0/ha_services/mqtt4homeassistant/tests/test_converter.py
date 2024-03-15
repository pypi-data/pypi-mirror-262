from unittest import TestCase

from ha_services.mqtt4homeassistant.converter import values2mqtt_payload
from ha_services.mqtt4homeassistant.data_classes import HaMqttPayload, HaValue, HaValues


class ConverterTestCase(TestCase):
    def test_basic(self):
        values = HaValues(
            device_name='egg boiler',
            values=[
                HaValue(
                    name='Power',
                    value=450,
                    device_class='energy',
                    state_class='measurement',
                    unit='W',
                )
            ],
            prefix='homeassistant',
            component='sensor',
        )
        self.assertEqual(
            values2mqtt_payload(values=values, name_prefix='Test'),
            HaMqttPayload(
                configs=[
                    {
                        'data': {
                            'device': {
                                'identifiers': ['test_eggboiler_power'],
                                'name': 'egg boiler',
                            },
                            'device_class': 'energy',
                            'enabled_by_default': True,
                            'name': 'Power',
                            'origin': {
                                'name': 'ha-services',
                                'support_url': 'https://pypi.org/project/ha_services/',
                                'sw_version': '0.6.0',
                            },
                            'state_class': 'measurement',
                            'state_topic': 'homeassistant/sensor/test_eggboiler/state',
                            'unique_id': 'test_eggboiler_power',
                            'unit_of_measurement': 'W',
                            'value_template': '{{ value_json.test_eggboiler_power }}',
                        },
                        'topic': 'homeassistant/sensor/test_eggboiler_power/config',
                    }
                ],
                state={
                    'data': {
                        'test_eggboiler_power': 450,
                    },
                    'topic': 'homeassistant/sensor/test_eggboiler/state',
                },
            ),
        )

    def test_check_prefix(self):
        with self.assertRaises(AssertionError) as err:
            values2mqtt_payload(values=None, name_prefix='1foobar')
        self.assertIn('Invalid: name_prefix', str(err.exception))
