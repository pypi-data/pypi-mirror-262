from cdktf import Fn
from constructs import Construct

from imports.chef.data_bag_item import DataBagItem


class SbpChefDataBagItem(DataBagItem):
    """SBP version of chef.data_bag_item"""

    def __init__(self, scope: Construct, ns: str, data_bag_item: str, content: dict, **kwargs):
        """Generate databag content and pass to original function json encoded

        New Args:
            data_bag_item: name of the databag
            content:  content of the databag
        """
        # call the original resource
        databag_content = content.copy()
        databag_content['id'] = data_bag_item

        super().__init__(
            scope=scope,
            id_=ns,
            content_json=Fn.jsonencode(databag_content),
            **kwargs,
        )
