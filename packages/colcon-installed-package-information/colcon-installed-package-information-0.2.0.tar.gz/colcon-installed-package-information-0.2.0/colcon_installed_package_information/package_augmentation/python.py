# Copyright 2022 Open Source Robotics Foundation, Inc.
# Licensed under the Apache License, Version 2.0

import sysconfig

try:
    from importlib.metadata import Distribution
except ImportError:
    # TODO: Drop this when dropping Python 3.7 support
    from importlib_metadata import Distribution

from colcon_core.package_augmentation \
    import PackageAugmentationExtensionPoint
from colcon_core.package_augmentation.python \
    import create_dependency_descriptor
from colcon_core.plugin_system import satisfies_version


class InstalledPythonPackageAugmentation(PackageAugmentationExtensionPoint):
    """
    Augment installed packages with Python distribution information.

    Only packages of the `installed` type are considered.
    """

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(
            PackageAugmentationExtensionPoint.EXTENSION_POINT_VERSION,
            '^1.0')

    def augment_packages(  # noqa: D102
        self, descs, *, additional_argument_names=None
    ):
        descs = {d for d in descs if d.type == 'installed'}
        if not descs:
            return

        for desc in descs:
            dists = Distribution.discover(
                path=_enumerate_python_dirs(str(desc.path)),
                name=desc.name)
            try:
                dist = next(iter(dists))
            except IndexError:
                continue

            version = dist.version
            if version and not desc.metadata.get('version'):
                desc.metadata['version'] = version
            desc.type = 'installed.python'
            # TODO: We should find a clean way to exclude test-oriented extras
            #       from this enumeration.
            desc.dependencies['run'].update(
                create_dependency_descriptor(str(req))
                for req in dist.requires)


def _enumerate_python_dirs(prefix):
    get_path_vars = {'base': prefix, 'platbase': prefix}
    yield sysconfig.get_path('purelib', vars=get_path_vars)
    yield sysconfig.get_path('platlib', vars=get_path_vars)
