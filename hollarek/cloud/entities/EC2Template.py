from __future__ import annotations

from typing import Optional
from .enums import ImageID, EC2Type
from dataclasses import dataclass

@dataclass
class InstanceTemplate:
    image_id: ImageID
    ec2_type: EC2Type
    setup_script: str = ''
    key_pair_name: Optional[str] = None
    network_interface_id: Optional[str] = None
    instance_name: Optional[str] = None
    security_group: Optional[str] = None
    instance_profile_arn: Optional[str] = None


    @classmethod
    def make_default(cls) -> InstanceTemplate:
        new_instance = cls(image_id=ImageID.UBUNTU_2204, ec2_type=EC2Type.T3_MICRO)
        return new_instance


    def get_params(self, num : int):
        params = {
            "ImageId": self.image_id,
            "MinCount": num,
            "MaxCount": num,
            "InstanceType": self.ec2_type,
        }

        if self.setup_script:
            params["UserData"] = self.setup_script

        if self.key_pair_name:
            params["KeyName"] = self.key_pair_name

        if self.network_interface_id:
            interfaces = {
                'DeviceIndex': 0,
                'NetworkInterfaceId': self.network_interface_id,
                'AssociatePublicIpAddress': True
            }
            params["NetworkInterfaces"] = [interfaces]

        if self.instance_name:
            name_tag = {
                'Key': 'Name',
                'Value': self.instance_name
            }

            tag_specs = {
                'ResourceType': 'instance',
                'Tags': [name_tag]
            }

            params["TagSpecifications"] = [tag_specs]

        if self.security_group:
            params["SecurityGroupIds"] = [self.security_group]

        if self.instance_profile_arn:
            params["IamInstanceProfile"] = {
                'Arn': self.instance_profile_arn
            }

        return params
