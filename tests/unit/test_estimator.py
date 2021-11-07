import json
import os.path

import pytest

from windml.app import _estimate

TEST_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def event_01():
    with open(os.path.join(TEST_ROOT, 'events/event.test.01.json')) as jf:
        data = json.load(jf)
    return data


class TestEstimator:
    def test_estimator_case_having_all_features(self, event_01):
        r = _estimate(body=event_01)
        assert r.status_code == 200

    def test_estimator_case_missing_feature(self, event_01):
        event_01 = event_01.copy()
        for x in list(event_01.keys())[:3]:
            event_01.pop(x)
        r = _estimate(body=event_01)
        assert r.status_code == 400

    def test_estimator_case_extra_feature(self, event_01):
        event_01 = event_01.copy()
        event_01['EXTRA'] = 0.1
        r = _estimate(body=event_01)
        assert r.status_code == 200

    def test_estimator_bad_data_type(self, event_01):
        event_01 = event_01.copy()
        for x in list(event_01.keys())[:3]:
            event_01[x] = '?'
        r = _estimate(body=event_01)
        assert r.status_code == 501

    @pytest.mark.skip(reason="Not yet implemented")
    def test_model_performance(self):
        # TODO test on a small benchmark dataset and make sure the mse loss is within reasonable e range
        raise NotImplementedError()

