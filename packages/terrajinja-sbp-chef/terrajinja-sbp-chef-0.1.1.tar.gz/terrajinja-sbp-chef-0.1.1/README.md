# terrajinja-sbp-chef

This is an extension to the vault provider for the following modules.
The original documentation can be found [here](https://registry.terraform.io/providers/dbresson/chef/latest/docs)

# SBP Specific implementations
Here is a list of supported resources and their modifications

## sbp.chef.data_bag_item
Original provider: [chef.data_bag_item](https://registry.terraform.io/providers/dbresson/chef/latest/docs/resources/data_bag_item)

This custom provider adds the following:
- allows specifying the databag item name seperate of the databag contents
- automaticly converts the databag contents in to json for the resource

| old parameter | new parameter | description |
| ------ | ------ | ------ |
| content_json | content | the data field is automaticly converted to json |
| - | data_bag_item | name of the databag item, inside the databag |

additional to the above the data structure, the key `id` is automaticly filled with the data_bag_item value
```
{ 
    "id": "{data_bag_item}", # automatically added
    "your_content": "data",
}
```

### terrajinja-cli example
the following is a code snipet you can used in a terrajinja-cli template file.
This creates a databag with the name `privoxy` and a databag item with the name `tst` and the specified content
```
terraform:
  resources:
    - task: privoxy-databag
      module: sbp.chef.data_bag_item
      parameters:
        data_bag_name: privoxy
        data_bag_item: tst
        content:
          permit_access_subnets:
            - 127.0.0.1
          whitelist: 
            - my.domain.com
```
