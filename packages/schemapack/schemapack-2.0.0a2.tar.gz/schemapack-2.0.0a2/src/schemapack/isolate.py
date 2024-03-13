# Copyright 2021 - 2023 Universität Tübingen, DKFZ, EMBL, and Universität zu Köln
# for the German Human Genome-Phenome Archive (GHGA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Logic to isolate a resource from a non-rooted datapack to create a rooted datapack."""

from collections import defaultdict
from collections.abc import Mapping
from typing import Optional

from schemapack.exceptions import ValidationAssumptionError
from schemapack.spec.datapack import (
    ClassName,
    DataPack,
    Resource,
    ResourceId,
)
from schemapack.spec.schemapack import SchemaPack


def identify_dependencies(
    *,
    datapack: DataPack,
    class_name: ClassName,
    resource_id: ResourceId,
    schemapack: SchemaPack,
    include_target: bool = False,
    _resource_blacklist: Optional[Mapping[ClassName, set[ResourceId]]] = None,
) -> Mapping[ClassName, set[ResourceId]]:
    """Identify all dependencies (recursively) for a given resource
    of the given class in the given datapack. Please note that it is assumed that
    the datapack has already been validated against the schemapack.

    Args:
        datapack:
            Containing the target resource and all dependencies.
        class_name:
            The class of the target resource.
        resource_id:
            The id of the target resource.
        schemapack:
            The schemapack used for looking up the classes of relations.
        include_target:
            Set to true if the target dependency shall be included in the result.
        _resource_blacklist:
            A mapping containing resources (resource ids as values and class names as
            keys) that shall be ignored during the dependency resolution and thus will
            not appear in the result. This is only used internally for recursion.

    Returns:
        A mapping containing resource ids (values) of dependencies by class names
        (keys).

    Raises:
        KeyError:
            If the resource_class or the resource_id does not exist in the schemapack
            or datapack.
        schemapack.Exceptions.ValidationAssumptionError:
            If it became apparent that the datapack was not already validated against
            the schemapack.
    """
    target_resource = datapack.resources[class_name][resource_id]
    target_class_definition = schemapack.classes[class_name]

    # Define a blacklist of resources to avoid getting lost in infinity loop for
    # circular dependencies:
    resource_blacklist: dict[ClassName, set[ResourceId]] = defaultdict(set)
    resource_blacklist[class_name].add(resource_id)
    if _resource_blacklist:
        for class_name, resource_ids in _resource_blacklist.items():
            resource_blacklist[class_name].update(resource_ids)

    dependencies_by_class: dict[ClassName, set[ResourceId]] = defaultdict(set)

    for relation_name in target_resource.relations:
        try:
            target_class_name = target_class_definition.relations[
                relation_name
            ].targetClass
        except KeyError as error:
            raise ValidationAssumptionError(
                context="relation resolution in schemapack"
            ) from error

        try:
            target_ids = target_resource.get_target_id_set(relation_name)
        except KeyError as error:
            raise ValidationAssumptionError(
                context="relation resolution in datapack"
            ) from error

        for target_id in target_ids:
            if (
                target_class_name in resource_blacklist
                and target_id in resource_blacklist[target_class_name]
            ):
                continue

            dependencies_by_class[target_class_name].add(target_id)

            # Recursively add dependencies of this target resource:
            nested_dependencies = identify_dependencies(
                datapack=datapack,
                class_name=target_class_name,
                resource_id=target_id,
                schemapack=schemapack,
                _resource_blacklist=resource_blacklist,
            )
            for nested_class_name, nested_ids in nested_dependencies.items():
                dependencies_by_class[nested_class_name].update(nested_ids)

    if include_target:
        dependencies_by_class[class_name].add(resource_id)

    return dependencies_by_class


def downscope_datapack(
    datapack: DataPack,
    resource_map: Mapping[ClassName, set[ResourceId]],
    ignore_non_existing: bool = False,
) -> DataPack:
    """Downscope a datapack to only contain the given resources.

    Args:
        ignore_non_existing:
            Controls how to handle resources from the resource_map that are not in the
            datapack. If set to `True`, these resources will be ignored. If set to
            `False` (default), a KeyError will be raised.

    Raises:
        KeyError:
            If a resource from the resource_map is not in the datapack and
            ignore_non_existing is set to `False`.

    """
    resources: dict[ClassName, dict[ResourceId, Resource]] = defaultdict(dict)

    for class_name, resource_ids in resource_map.items():
        try:
            existing_resources = datapack.resources[class_name]
        except KeyError as error:
            if ignore_non_existing:
                continue
            raise error

        for resource_id in resource_ids:
            try:
                existing_resource = existing_resources[resource_id]
            except KeyError as error:
                if ignore_non_existing:
                    continue
                raise error

            resources[class_name][resource_id] = existing_resource

    return datapack.model_copy(update={"resources": resources})


def isolate_resource(
    *,
    datapack: DataPack,
    class_name: ClassName,
    resource_id: ResourceId,
    schemapack: SchemaPack,
) -> DataPack:
    """Isolate a resource from a non-rooted datapack to created a rooted datapack. I.e.
    the resulting datapack will only contain resources referenced by the root resource
    as well as the root resource itself.

    Please note:
        The returned rooted datapack will not be compatible anymore with the original
        non-rooted schemapack.
    """
    dependency_map = identify_dependencies(
        datapack=datapack,
        class_name=class_name,
        resource_id=resource_id,
        schemapack=schemapack,
        include_target=True,
    )
    rooted_datapack = downscope_datapack(datapack=datapack, resource_map=dependency_map)
    rooted_datapack.root_resource = resource_id
    return rooted_datapack


def isolate_class(*, class_name: ClassName, schemapack: SchemaPack) -> SchemaPack:
    """Return a copy of the provided schemapack that is rooted to the specified class."""
    return schemapack.model_copy(update={"root_class": class_name})


def isolate(
    *,
    class_name: ClassName,
    resource_id: ResourceId,
    schemapack: SchemaPack,
    datapack: DataPack,
) -> tuple[SchemaPack, DataPack]:
    """Create copies of the provided schemapacks and datapacks that are rooted towards
    the specified class and resource. I.e. the resulting datapack will only contain
    resources referenced by the root resource as well as the root resource itself.

    Returns:
        A tuple containing both the rooted schemapack and the rooted datapack.
    """
    rooted_schemapack = isolate_class(class_name=class_name, schemapack=schemapack)
    rooted_datapack = isolate_resource(
        datapack=datapack,
        class_name=class_name,
        resource_id=resource_id,
        schemapack=schemapack,
    )
    return rooted_schemapack, rooted_datapack
