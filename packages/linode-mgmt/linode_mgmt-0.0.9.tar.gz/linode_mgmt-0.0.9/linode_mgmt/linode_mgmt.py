#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file name: linode_mgmt.py
author: Shlomi Ben-David <shlomi.ben.david@gmail.com>
file version: 0.0.1
"""
import linode_api4.errors
from linode_api4 import LinodeClient, Instance
import sys
import logging
from linode_mgmt.args import get_cli_args
from pylib3 import init_logging

logger = logging.getLogger(__name__)
logging.getLogger('kubernetes.client.rest').setLevel('WARNING')


# ---- FLAGS ----
cluster_creation = False
disk_modifications = True
config_modifications = True


class LinodeMGMT(object):
    """Linode Management Class"""
    def __init__(self, token, label):
        """
        Initialization function

        :param str token: a personal API token
        :param str label: a cluster name (which configured as a label)
        """
        self.client = LinodeClient(token)
        self.label = label
        self.cluster = self.get_cluster()
        # This was set in purpose to specify action per a specific cluster
        if self.cluster:
            self.nodes = self.get_nodes()

    def get_cluster(self):
        """
        Get a cluster per a specific label
        :returns: cluster object or None
        """
        logger.info(f"Getting '{self.label}' cluster details")
        clusters = self.client.lke.clusters()
        for _cluster in clusters or []:
            if self.label == _cluster.label:
                return _cluster

        logger.debug(f"Cluster '{self.label}' does not exist.")
        return ""

    def get_nodes(self, pool_id=None):
        """
        Get cluster nodes

        :param int pool_id: pool id number
        :returns nodes object or None
        """
        logger.info("Getting nodes details")
        nodes = []
        logger.debug(f"number of pools: {self.cluster.pools.total_items}")
        for pool in self.cluster.pools:
            logger.debug(f"pool_id: {pool.id}")
            if pool_id and pool_id == pool.id:
                return pool.nodes

            if isinstance(pool.nodes, list):
                nodes += pool.nodes
        logger.debug(f"number of nodes: {len(nodes)}")
        return nodes

    def get_node_instance(self, node_name):
        """
        Get the node instance object from the passed node name

        :param str node_name: a node name (label)
        :returns (obj) node instance or None
        """
        logger.info(f"Getting {node_name} node instance object")
        if not self.nodes:
            logger.debug("Could not find any nodes!!!")
            return

        for node in self.nodes:
            instance = Instance(self.client, node.instance_id)
            _node_name = instance.label
            logger.debug(f"node_name: {_node_name}")
            if node_name == _node_name:
                return instance

        return

    def create_cluster(self, args, node_pool_limit=100):
        """
        Creates or Updates a cluster

        :param obj args: command line arguments
        :param int node_pool_limit: a limit of number of nodes in a pool (must be between 1-100)
        """
        logger.info(f"Creating '{args.cluster}' cluster")
        if self.cluster:
            logger.warning(f"Cluster '{args.cluster}' already exist, nothing to do!!!")
            return

        full_node_pools = 1
        partial_nodes = 0
        node_pools = []
        multiple_node_pools = False
        if args.node_count > node_pool_limit:
            multiple_node_pools = True
            full_node_pools = round(args.node_count / node_pool_limit)
            partial_nodes = args.node_count - (full_node_pools * node_pool_limit)

        logger.debug(f"node_count: {args.node_count}")
        logger.debug(f"full_node_pools: {full_node_pools}")
        logger.debug(f"partial_nodes: {partial_nodes}")

        if multiple_node_pools:
            while full_node_pools > 0:
                node_pools.append(self.client.lke.node_pool(args.node_type, node_pool_limit))
                full_node_pools -= 1

            if partial_nodes:
                node_pools.append(self.client.lke.node_pool(args.node_type, partial_nodes))
        else:
            node_pools.append(self.client.lke.node_pool(args.node_type, args.node_count))

        self.client.lke.cluster_create(
            region=args.region,
            label=args.cluster,
            node_pools=node_pools,
            kube_version=args.kube_version,
            control_plane={"high_availability": True}
        )

    def update_cluster(self, args):
        """
        Updates existing cluster by increasing/decreasing the node number

        :param obj args: command line arguments
        """
        if not self.cluster:
            logger.debug(f"Cluster '{args.cluster}' does not exist, aborting...")
            return

        logger.info(f"Updating '{args.cluster}' cluster nodes")
        pools = getattr(self.cluster, 'pools', [])
        cluster_pools = []
        for pool in pools:
            logger.debug(f"cluster pool_id: {pool.id}")
            cluster_pools.append(pool.id)
            if args.pool_id and args.pool_id != pool.id:
                logger.debug(f"requested pool_id: {args.pool_id}")
                continue

            api_endpoint = f"/lke/clusters/{self.cluster.id}/pools/{pool.id}"
            logger.debug(f"api_endpoint: {api_endpoint}")
            data = {"count": args.node_count}
            logger.debug(f"data: {data}")
            self.client.put(api_endpoint, data=data)
            logger.debug(f"Cluster '{args.cluster}' nodes in {pool.id} pool updated successfully")

        if args.pool_id and args.pool_id not in cluster_pools:
            logger.warning(f"No such pool id ({args.pool_id})")

    def upgrade_cluster(self, args):
        """
        Upgrade existing cluster in recycle mode.
        This recycles each worker node on a rolling basis so that only one node is down at any particular moment.
        In the highest level of detail, each worker node is independently drained and cordoned one at a time.

        :param obj args: command line arguments
        """
        if not self.cluster:
            logger.debug(f"Cluster '{args.cluster}' does not exist, aborting...")
            return

        logger.info(f"Upgrading '{args.cluster}' cluster")
        logger.info("Step 1/2 - upgrading the control plane")
        api_endpoint = f"/lke/clusters/{self.cluster.id}"
        logger.debug(f"api_endpoint: {api_endpoint}")
        data = {"k8s_version": args.kube_version}
        logger.debug(f"data: {data}")
        response = self.client.put(api_endpoint, data=data)
        if not response:
            logger.error("Failed to upgrade the control plane")
            return

        logger.debug(f"response: {response}")
        logger.info("Step 2/2 - upgrading the worker nodes")
        api_endpoint = f"/lke/clusters/{self.cluster.id}/recycle"
        logger.debug(f"api_endpoint: {api_endpoint}")
        self.client.post(api_endpoint)

    def get_cluster_id(self, args=None):
        """
        Get cluster id

        :param obj args: command line arguments
        """
        logger.info(f"Getting '{args.cluster}' cluster id")
        logger.info(f"cluster_id: {self.cluster.id}")
        return self.cluster.id

    def get_node(self, node_name):
        """
        Gets node object from the passed node name

        :param str node_name: a node name
        :returns: node object
        """
        logger.debug(f"Getting '{node_name}' node id")
        for node in self.nodes:
            if node.instance.label != node_name:
                continue

            logger.debug(f"node_id: {node.instance_id}")
            return node

    def get_volumes(self):
        """
        Gets all volumes

        :returns: list with all volumes
        """
        logger.debug("Getting all volumes")
        volumes = self.client.volumes()
        logger.debug(f"volumes: {volumes}")
        return volumes or []

    def list_volumes(self, args=None):
        """
        list all volumes
        """
        logger.info("Listing all volumes")
        volumes = self.get_volumes()
        for volume in volumes:
            logger.debug("-" * 80)
            logger.debug(f"volume name: {volume.label}")
            logger.debug(f"volume id: {volume.id}")
            logger.debug(f"attached to: {volume.linode_id}")
            logger.debug(f"size: {volume.size}")
            logger.debug(f"region: {volume.region}")

    def delete_volume(self, args=None):
        """
        Deletes volume

        :param obj args: command line arguments
        """
        logger.info(f"Deleting volume(s)")
        volumes = self.get_volumes()
        for volume in volumes:
            _volume_name = volume.label
            if not args.all and getattr(args, 'volume_name') and args.volume_name != _volume_name:
                continue

            if not volume.linode_id and _volume_name.startswith('pvc'):
                logger.debug("-" * 80)
                logger.debug(f"Deleting {_volume_name} volume")
                logger.debug(f"attached to: {volume.linode_id}")
                api_endpoint = f"/volumes/{volume.id}"
                logger.debug(f"api_endpoint: {api_endpoint}")
                self.client.delete(api_endpoint)

    @staticmethod
    def poweroff_node(instance, args=None):
        """
        Power Off a node

        :params obj instance: node instance object
        """
        logger.info(f"Powering Off '{instance.label}' instance")
        try:
            if instance.shutdown():
                logger.info(f"Instance '{instance.label}' successfully turned off.")
        except linode_api4.errors.ApiError as err:
            logger.error(f"Failed to power off '{instance.label}' instance ({err.errors})")

    def poweroff_all_nodes(self, args):
        """
        Power off all nodes

        :param obj args: command line arguments
        """
        logger.info(f"Powering off all nodes")
        if not self.nodes:
            logger.warning(f"Could not find any nodes in {args.cluster} cluster, aborting...")
            return

        for node in self.nodes:
            instance = Instance(self.client, node.instance_id)
            if node.status == "not_ready":
                logger.info(f"Instance '{instance.label}' is not ready, skipping...")
                continue
            self.poweroff_node(instance=instance)

    def poweron_node(self, instance=None, args=None):
        """
        Power On a node

        :params obj instance: node instance object
        """
        instance = instance or self.get_node_instance(args.node_name)
        logger.info(f"Powering On '{instance.label}' instance")
        try:
            if instance.reboot():
                logger.info(f"Instance '{instance.label}' successfully turned on")
        except linode_api4.errors.ApiError as err:
            logger.error(f"Failed to power on '{instance.label}' instance ({err.errors})")

    def poweron_all_nodes(self, args):
        """
        Power on all nodes

        :param obj args: command line arguments
        """
        logger.info(f"Powering on all nodes")
        if not self.nodes:
            logger.warning(f"Could not find any nodes in {args.cluster} cluster, aborting...")
            return

        for node in self.nodes:
            instance = Instance(self.client, node.instance_id)
            if node.status == "not_ready":
                logger.info(f"Instance '{instance.label}' is not ready, skipping...")
                continue
            self.poweron_node(instance=instance)

    def restart_node(self, instance=None, args=None):
        """
        Restart a node

        :params obj instance: node instance object
        """
        instance = instance or self.get_node_instance(args.node_name)
        logger.info(f"Restarting '{instance.label}' instance")
        self.poweroff_node(args)
        self.poweron_node(args)

    def restart_all_nodes(self, args):
        """
        Restart all nodes

        :param obj args: command line arguments
        """
        logger.info(f"Restarting all nodes")
        self.poweroff_all_nodes(args)
        self.poweron_all_nodes(args)

    def update_node(self, node=None, args=None):
        """
        update a node

        :params obj node: node instance object
        """
        node = node or self.get_node(node_name=args.node_name)
        instance = Instance(self.client, node.instance_id)
        logger.info(f"Updating '{instance.label}' node")
        api_endpoint = f"/linode/instances/{node.instance_id}"
        logger.debug(f"api_endpoint: {api_endpoint}")
        data = {
            "alerts": {
                "cpu": args.node_cpu_alert or 0,
                "network_in": args.node_network_in_alert or 0,
                "network_out": args.node_network_out_alert or 0,
                "transfer_quota": args.node_transfer_quota_alert or 0,
                "io": args.node_io_alert or 0
            }
        }
        logger.debug(f"data: {data}")
        result = self.client.put(api_endpoint, data=data)
        if result:
            logger.debug(f"Node '{instance.label}' updated successfully")
            logger.debug(f"result: {result}")

    def update_all_nodes(self, args):
        """
        Update all nodes

        :param obj args: command line arguments
        """
        logger.info(f"Updating all nodes")
        if not self.nodes:
            logger.warning(f"Could not find any nodes in {args.cluster} cluster, aborting...")
            return

        for node in self.nodes:
            instance = Instance(self.client, node.instance_id)
            if node.status == "not_ready":
                logger.info(f"Instance '{instance.label}' is not ready, skipping...")
                continue

            self.update_node(args=args, node=node)

    def get_storage_cluster(self):
        """
        Get the storage cluster

        :returns: storage bucket object
        """
        logger.info(f"Getting {self.cluster.label} storage cluster")
        storage_clusters = self.client.object_storage.clusters()
        region_id = self.cluster.region.id
        logger.debug(f"region_id: {region_id}")
        for storage_cluster in storage_clusters:
            if region_id not in storage_cluster.id:
                continue

            logger.debug(f"storage_cluster: {storage_cluster.id}")
            return storage_cluster

    def create_storage(self, args):
        """
        Creates or Updates a storage bucket

        :param obj args: command line arguments
        """
        logger.info(f"Creating '{args.bucket_name}' bucket")
        storage_cluster = self.get_storage_cluster()
        if not storage_cluster:
            logger.error("Could find storage cluster")
            return

        self.client.object_storage.bucket_create(
            cluster=storage_cluster,
            label=args.bucket_name
        )

    def delete_storage(self, args):
        """
        Deletes a storage bucket

        :param obj args: command line arguments
        """
        logger.info(f"Deleting '{args.bucket_name}' bucket")
        storage_cluster = self.get_storage_cluster()
        if not storage_cluster:
            logger.error("Could find storage cluster")
            return

        api_endpoint = f"/object-storage/buckets/{storage_cluster.id}/{args.bucket_name}"
        logger.debug(f"api_endpoint: {api_endpoint}")
        try:
            self.client.delete(api_endpoint)
        except Exception as err:
            if err and getattr(err, 'status') == 404:
                raise Exception(f"Bucket '{args.bucket_name}' does not exist ({err.status})")

    def list_storage(self, args=None):
        """
        list all storage objects
        """
        logger.info("Listing all storage objects")
        buckets = self.client.object_storage.buckets()
        for bucket in buckets:
            logger.debug("-" * 80)
            logger.debug(f"bucket name: {bucket.label}")
            logger.debug(f"bucket id: {bucket.id}")
            logger.debug(f"hostname: {bucket.hostname}")
            logger.debug(f"cluster: {bucket.cluster}")
            logger.debug(f"objects: {bucket.objects}")
            logger.debug(f"size: {bucket.size}")

    def get_func(self, action, resource, all):
        """
        Get a function based on the passed action/resource

        :param str action: action name (i.e., update, create)
        :param str resource: resource name (i.e., cluster)
        :param bool all: used to select a function that will be implemented on all items in the resource
        :return: func object
        """
        if not action:
            return

        cluster_action_to_func_mapper = {
            'create': self.create_cluster,
            'update': self.update_cluster,
            'upgrade': self.upgrade_cluster,
            'get-id': self.get_cluster_id,
        }

        node_action_to_func_mapper = {
            'poweron': self.poweron_all_nodes if all else self.poweron_node,
            'poweroff': self.poweroff_all_nodes if all else self.poweroff_node,
            'restart': self.restart_all_nodes if all else self.restart_node,
            'update': self.update_all_nodes if all else self.update_node
        }

        volume_action_to_func_mapper = {
            'list': self.list_volumes,
            'delete': self.delete_volume
        }

        storage_action_to_func_mapper = {
            'list': self.list_storage,
            'delete': self.delete_storage,
            'create': self.create_storage
        }

        resource_to_func_mapper = {
            'cluster': cluster_action_to_func_mapper.get(action),
            'node': node_action_to_func_mapper.get(action),
            'volume': volume_action_to_func_mapper.get(action),
            'storage': storage_action_to_func_mapper.get(action)
        }

        return resource_to_func_mapper.get(resource)


def main():
    """ MAIN FUNCTION """

    try:
        # get app arguments
        args = get_cli_args()

        # initialize logger
        init_logging(
            log_file=args.log_file or '',
            verbose=args.verbose,
            console=args.console,
            info='green', debug='cyan'
        )

        logger.info("Linode Management")
        client = LinodeMGMT(token=args.token, label=args.cluster)

        func = client.get_func(args.action, getattr(args, 'resource', None), getattr(args, 'all', None))
        if not func:
            raise Exception("No such action/resource")

        func(args=args)

    except Exception as err:
        logger.error(err.message) \
            if hasattr(err, 'message') else logger.error(err)
        return 1


if __name__ == '__main__':
    sys.exit(main())
