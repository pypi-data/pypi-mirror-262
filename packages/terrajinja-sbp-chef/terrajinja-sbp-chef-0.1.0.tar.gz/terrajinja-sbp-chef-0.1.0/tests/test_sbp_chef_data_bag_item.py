import pytest
from cdktf import Testing

from src.terrajinja.sbp.chef.data_bag_item import SbpChefDataBagItem
from .helper import stack, has_resource, has_resource_path_value


class TestSbpVault:
    def test_json_formatting(self, stack):
        SbpChefDataBagItem(
            scope=stack,
            ns="sbp_chef_data_bag_item",
            data_bag_name="databag_name",
            data_bag_item="databag_item",
            content={'my_secret': 'secret'},
        )

        synthesized = Testing.synth(stack)

        has_resource(synthesized, "chef_data_bag_item")
        has_resource_path_value(synthesized, "chef_data_bag_item", "sbp_chef_data_bag_item", "data_bag_name",
                                'databag_name')
        has_resource_path_value(synthesized, "chef_data_bag_item", "sbp_chef_data_bag_item", "content_json",
                                r'${jsonencode({"my_secret" = "secret", "id" = "databag_item"})}')


if __name__ == "__main__":
    pytest.main()
