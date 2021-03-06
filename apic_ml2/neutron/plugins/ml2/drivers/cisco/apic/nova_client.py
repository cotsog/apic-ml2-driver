#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import novaclient.client as nclient
from novaclient import exceptions as nova_exceptions
from oslo_config import cfg
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class NovaClient(object):

    def __init__(self):

        bypass_url = "%s/%s" % (cfg.CONF.nova_url,
                                cfg.CONF.nova_admin_tenant_id)

        self.client = nclient.Client(
            '2', username=cfg.CONF.nova_admin_username,
            api_key=cfg.CONF.nova_admin_password,
            project_id=None,
            tenant_id=cfg.CONF.nova_admin_tenant_id,
            auth_url=cfg.CONF.nova_admin_auth_url,
            bypass_url=bypass_url,
            region_name=cfg.CONF.nova.region_name)

    def get_server(self, server_id):
        try:
            return self.client.servers.get(server_id)
        except nova_exceptions.NotFound:
            LOG.warning(_("Nova returned NotFound for server: %s"),
                        server_id)
        except Exception as e:
            LOG.exception(e)
