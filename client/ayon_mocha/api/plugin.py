"""Plugin API for Mocha Pro AYON addon."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ayon_core.pipeline import (
    CreatedInstance,
    Creator,
)

if TYPE_CHECKING:
    from .pipeline import MochaProHost


class MochaCreator(Creator):
    """Mocha Pro creator."""
    def create(self,
               product_name: str,
               instance_data: dict,
               pre_create_data: dict) -> CreatedInstance:
        """Create product instance in the host application.

        Args:
            product_name (str): Name of the product to be created.
            instance_data (dict): Data to be used for creating the product.
            pre_create_data (dict): Data to be used before
                creating the product.

        Returns:
            CreatedInstance: Created product instance.

        """
        instance = CreatedInstance(
            self.product_type,
            product_name,
            instance_data,
            self,
        )
        self._add_instance_to_context(instance)
        host: MochaProHost = self.host
        host.add_publish_instance(instance.data_to_store())\

        return instance

    def collect_instances(self) -> None:
        """Collect instances from the host application."""
        host: MochaProHost = self.host
        for instance_data in host.get_publish_instances():
            if instance_data["creator_identifier"] != self.identifier:
                continue
            created_instance = CreatedInstance.from_existing(
                instance_data, self
            )
            self._add_instance_to_context(created_instance)

    def update_instances(self, update_list: list[dict]) -> None:
        """Update instances in the host application.

        Args:
            update_list (list[dict]): List of instances to be updated.

        """
        host: MochaProHost = self.host
        concurrent_instances = host.get_publish_instances()
        instances_by_id = {
            i_data["instance_id"]: i_data
            for i_data in concurrent_instances
            if i_data["instance_id"]
        }

        for instance, changes in update_list:
            instance_data = changes.new_values
            cur_instance_data = instances_by_id.get(instance.instance_id)
            if cur_instance_data is None:
                concurrent_instances.append(instance_data)
                continue
            for key in set(cur_instance_data) - set(instance_data):
                cur_instance_data.pop(key)
            cur_instance_data.update(instance_data)
        host.write_create_instances(concurrent_instances)

    def remove_instances(self, instances: list[CreatedInstance]) -> None:
        """Remove instances from the host application.

        Args:
            instances (list[CreatedInstance]): List of instances to be removed.

        """
        host: MochaProHost = self.host
        for instance in instances:
            self._remove_instance_from_context(instance)
            host.remove_create_instance(instance.id)
