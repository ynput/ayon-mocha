"""Extract tracking points from Mocha."""
from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, List, Optional

import clique
from ayon_core.pipeline import KnownPublishError, publish
from ayon_mocha.api.lib import (
    ExporterProcessInfo,
    get_mocha_version,
)
from ayon_mocha.api.mocha_exporter_mappings import EXPORTER_MAPPING
from mocha.project import Layer, Project, View

if TYPE_CHECKING:
    from logging import Logger

    import pyblish.api
    from ayon_mocha.api.lib import ExporterInfo

EXTENSION_PATTERN = re.compile(r"(?P<name>.+)\(\*\.(?P<ext>\w+)\)")
MOCHA_2025 = 2025


class ExportShape(publish.Extractor):
    """Export shapes."""

    label = "Export Shapes"
    families: ClassVar[list[str]] = ["matteshapes"]
    log: Logger

    def process(self, instance: pyblish.api.Instance) -> None:
        """Process the instance."""
        dir_path = Path(self.staging_dir(instance))
        project: Project = instance.context.data["project"]
        layer: Layer = instance.data["layer"]

        process_info = ExporterProcessInfo(
            mocha_python_path=instance.context.data["mocha_python_path"],
            mocha_exporter_path=instance.context.data["mocha_exporter_path"],
            current_project_path=instance.context.data["currentFile"],
            staging_dir=dir_path,
            options={}
        )

        outputs = self.export(
            instance.data["productName"],
            project,
            instance.data["use_exporters"],
            layer,
            process_info,
        )

        representations = self.process_outputs_to_representations(
            outputs, instance)

        instance.data.setdefault(
            "representations", []).extend(representations)

        self.log.debug(instance.data["representations"])

    def process_outputs_to_representations(
            self, outputs: list[dict],
            instance: pyblish.api.Instance) -> list[dict]:
        """Process the output to representations.

        This will process output from the exporters to representations.

        Args:
            outputs (list[dict]): list of outputs.
            instance (pyblish.api.Instance): instance.

        Returns:
            list[dict]: list of representations.

        Raises:
            KnownPublishError: if the exporter produced multiple
                sequences and single files.

        """
        representations = []
        staging_dir = Path(self.staging_dir(instance))

        for output in outputs:
            # if there are multiple files in one representation
            # we need to check if it is sequence or not as current
            # integration does not support multiple files that are not
            # in sequences.
            repre_name = self._exporter_name_to_representation_name(
                output["name"])

            cols, rems = clique.assemble(output["files"])
            if rems and cols:
                # there are both sequences and single files
                if cols > 1:
                    # the extractor produced multiple sequences
                    # and single files. This is not supported now
                    # due to the complexity.
                    msg = ("The exporter produced multiple sequences "
                           "and single files. This is not supported.")
                    raise KnownPublishError(msg)
                output_files = cols[0]
                for reminder in rems:
                    self.add_to_resources(
                        Path(self.staging_dir(instance)) / reminder, instance)
                representations.append({
                    "name": repre_name,
                    "ext": output["ext"],
                    "files": output_files,
                    "stagingDir": output["stagingDir"],
                    "outputName": output["outputName"],
                })
            if rems and not cols:
                if len(rems) > 1:
                    # if there are only non-sequence files
                    for reminder in rems:
                        self.add_to_resources(
                            Path(self.staging_dir(instance)) / reminder, instance)  # noqa: E501
                    manifest_file = self._create_manifest_file(
                        staging_dir, rems, repre_name)
                    representations.append({
                        "name": repre_name,
                        "ext": output["ext"],
                        "files": manifest_file,
                        "stagingDir": output["stagingDir"],
                        "outputName": output["outputName"],
                    })
                else:
                    # if there is only one non-sequence file
                    representations.append({
                        "name": repre_name,
                        "ext": output["ext"],
                        "files": rems[0],
                        "stagingDir": output["stagingDir"],
                        "outputName": output["outputName"],
                    })
            if cols and not rems:
                # if there are only sequences
                if len(cols) > 1:
                    # the extractor produced multiple sequences
                    # and single files. This is not supported now
                    # due to the complexity.
                    msg = ("The exporter produced multiple sequences "
                           "and single files. This is not supported.")
                    raise KnownPublishError(msg)
                representations.append({
                    "name": repre_name,
                    "ext": output["ext"],
                    "files": list(cols[0]),
                    "stagingDir": output["stagingDir"],
                    "outputName": output["outputName"],
                })
        return representations

    @staticmethod
    def _create_manifest_file(
            staging_dir: Path, files: list[str], repre_name: str) -> str:
        """Create a manifest file.

        This will put all the files to a manifest file that
        will be used as a representation. This is because the
        current integration does not support multiple files
        that are not in sequences.

        Args:
            staging_dir (Path): staging directory.
            files (list[str]): list of files.
            repre_name (str): representation name.

        Returns:
            str: manifest file name.

        """
        file_name = f"{repre_name}.manifest"
        manifest_file = staging_dir / file_name
        with open(manifest_file, "w", encoding="utf-8") as file:
            file.writelines(files)
        return file_name

    @staticmethod
    def export(
            product_name: str,
            project: Project,
            exporters: list[ExporterInfo],
            layer: Layer,
            process_info: ExporterProcessInfo
        ) -> list[dict]:
        """Export the instance.

        This is using in-process export but since the export
        times are pretty fast, it's easier and probably
        faster than using the external export.

        Args:
            product_name (str): used for naming the resulting
                files.
            project (Project): Mocha project.
            exporters (list[ExporterInfo]): exporters to use.
            layer (Layer): layer to export.
            process_info (ExporterProcessInfo): process information.

        Returns:
            list[dict]: list of exported files.

        Raises:
            KnownPublishError: if the exporter name is not found

        """
        views = [view_info.name for view_info in project.views]
        views_to_export: set[View] = {
            View(num)
            for num, view_info in enumerate(project.views)
            if view_info.name in views or view_info.abbr in views
        }

        output: list[dict] = []
        for exporter_info in exporters:
            exporter_name = exporter_info.label
            if not exporter_name:
                msg = ("Cannot get exporter name "
                       f"from {exporter_info.label} exporter.")
                raise KnownPublishError(msg)

            exporter_short_hash = exporter_info.id[:8]

            version = get_mocha_version() or "2024"

            # exporters were rewritten in 2025. For older version
            # we need to parse the file extension from the exporter
            # label. We add it here so it is later on used from the
            # resulted file name.
            file_name = f"{product_name}_{exporter_short_hash}"
            if int(version.split(".")[0]) < MOCHA_2025:
                ext = ExportShape._get_extension(exporter_info)
                if not ext:
                    msg = ("Cannot get extension "
                           f"from {exporter_info.label} exporter.")
                    raise KnownPublishError(msg)
                file_name += f".{ExportShape._get_extension(exporter_info)}"

            tracking_file_path = (
                    process_info.staging_dir / file_name
            )

            # this is for some reason needed to pass it to `do_render()`
            views_typed: List[View] = list(views_to_export)
            layers_typed: List[Layer] = [layer]
            result = exporter_info.exporter.do_export(
                project,
                layers_typed,
                tracking_file_path.as_posix(),
                views_typed
            )

            if not result:
                msg = f"Export failed for {exporter_name}."
                raise KnownPublishError(msg)

            output_files = []
            ext = None
            for k, v in result.items():
                Path(k).write_bytes(v)
                output_files.append(Path(k).name)

                if ext is None:
                    ext = Path(k).suffix[1:]

            output.append({
                "name": exporter_info.label,
                "ext": ext,
                "files": output_files,
                "stagingDir": process_info.staging_dir.as_posix(),
                "outputName": exporter_short_hash,
            })

        return output

    def add_to_resources(
            self, path: Path, instance: pyblish.api.Instance) -> None:
        """Add the path to the resources."""
        self.log.debug("Adding to resources: %s", path)

        publish_dir_path = Path(instance.data["publishDir"])
        instance.data["transfers"].append(
            [path.as_posix(), (publish_dir_path / path.name).as_posix()])

    @staticmethod
    def _get_extension(exporter_info: ExporterInfo) -> Optional[str]:
        """Get the extension of the exporter.

        This is used only if the exporter name contains the extension.
        From Mocha 2025 the extension is not part of the exporter name
        anymore.

        Returns:
            Optional[str]: extension of the exporter if detected.

        """
        match = re.search(EXTENSION_PATTERN, exporter_info.label)
        return match["ext"] if match else None

    @staticmethod
    def _exporter_name_to_representation_name(
            exporter_name: str) -> str:
        """Convert the exporter name to representation name.

        Args:
            exporter_name (str): exporter name.

        Returns:
            str: exporter representation name.

        """
        version = get_mocha_version() or "2024"
        try:
            mapping = EXPORTER_MAPPING["shape"][version]
        except KeyError:
            mapping = EXPORTER_MAPPING["shape"]["2024.5"]

        return mapping.get(
            exporter_name, exporter_name)
