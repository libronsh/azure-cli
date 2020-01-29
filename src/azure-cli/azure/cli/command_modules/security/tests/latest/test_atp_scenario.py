# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.testsdk import (ScenarioTest, ResourceGroupPreparer, StorageAccountPreparer)


class SecurityAtpSettingsTests(ScenarioTest):
    @ResourceGroupPreparer()
    @StorageAccountPreparer()
    def test_security_atp_settings(self, resource_group, resource_group_location, storage_account):
        # run show cli
        atp_settings = self.cmd('security atp storage show --resource-group {} --storage-account-name {}'
                                .format(resource_group, storage_account)).get_output_in_json()
        self.assertTrue(len(atp_settings) >= 0)

        # enable atp
        atp_settings = self.cmd('security atp storage update --resource-group {} --storage-account-name {} --is-enabled true'
                                .format(resource_group, storage_account)).get_output_in_json()
        self.assertTrue(atp_settings["isEnabled"])

        # validate atp setting
        atp_settings = self.cmd('security atp storage show --resource-group {} --storage-account-name {}'
                                .format(resource_group, storage_account)).get_output_in_json()
        self.assertTrue(atp_settings["isEnabled"])

        # disable atp
        atp_settings = self.cmd('security atp storage update --resource-group {} --storage-account-name {} --is-enabled false'
                                .format(resource_group, storage_account)).get_output_in_json()
        self.assertFalse(atp_settings["isEnabled"])

        # validate atp setting
        self.cmd('security atp storage show --resource-group {} --storage-account-name {}'
                 .format(resource_group, storage_account)).get_output_in_json()
        self.assertFalse(atp_settings["isEnabled"])
