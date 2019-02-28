import unittest
import sys
import pytest
from mock import MagicMock
import mock
# sys.modules['spotinst_sdk2'] = MagicMock()
from ansible.modules.cloud.spotinst.spotinst_aws_elastigroup import expand_elastigroup


@pytest.fixture(autouse=True)
def spotinst_sdk2(monkeypatch):
    spotinst_sdk2 = MagicMock()
    sys.modules['spotinst_sdk2'] = spotinst_sdk2

    # monkeypatch.setattr(sys.modules, 'spotinst_sdk2', MagicMock())

    return spotinst_sdk2


@pytest.fixture(autouse=True)
def spotinst(spotinst_sdk2):
    import ansible.modules.cloud.spotinst.spotinst_aws_elastigroup as spotinst

    return spotinst



class MockModule:

    def __init__(self, input_dict):
        self.params = input_dict

class TestSpotinstAwsElastigroup():

    def test_expand_elastigroup(self, spotinst, spotinst_sdk2):
        """Format input into proper json structure"""

        input_dict = dict(
            name="test_name",
            min_size=1,
            max_size=2,
            target=3,
            product="test_product",
            image_id="test_id",
            health_check_grace_period=0,
            ebs_optimized=True,
            elastic_beanstalk=dict(
                managed_actions=dict(
                    platform_update=dict(
                        perform_at="test_perform_at",
                        time_window="test_time_window",
                        update_level="test_update_level"
                    )
                ),
                deployment_preferences=dict(
                    grace_period=0,
                    batch_size_percentage=100,
                    automatic_roll=True
                )
            )
        )
        module = MockModule(input_dict=input_dict)
        actual_eg = expand_elastigroup(module=module, is_update=False)

        assert "test_name" == actual_eg.name 

        assert 1 == actual_eg.capacity.minimum
        assert 2 == actual_eg.capacity.maximum
        assert 3 == actual_eg.capacity.target

        assert "test_product" == actual_eg.compute.product
        assert "test_id" == actual_eg.compute.launch_specification.image_id
        assert 0 == actual_eg.compute.launch_specification.health_check_grace_period
        assert True == actual_eg.compute.launch_specification.ebs_optimized

        assert "test_perform_at" == actual_eg.third_parties_integration.elastic_beanstalk.managed_actions.platform_update.perform_at
        assert "test_time_window" == actual_eg.third_parties_integration.elastic_beanstalk.managed_actions.platform_update.time_window
        assert "test_update_level" == actual_eg.third_parties_integration.elastic_beanstalk.managed_actions.platform_update.update_level

        assert 0 == actual_eg.third_parties_integration.elastic_beanstalk.deployment_preferences.grace_period
        assert 100 == actual_eg.third_parties_integration.elastic_beanstalk.deployment_preferences.batch_size_percentage
        assert True == actual_eg.third_parties_integration.elastic_beanstalk.deployment_preferences.automatic_roll
