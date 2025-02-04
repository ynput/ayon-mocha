"""Extract tracking points from Mocha."""
from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, List, Optional

import clique
from ayon_core.pipeline import KnownPublishError, publish
from ayon_mocha.api.lib import (
    SHAPE_EXPORTERS_REPRESENTATION_NAME_MAPPING,
    ExporterProcessInfo,
)
from mocha.project import Layer, Project, View

if TYPE_CHECKING:
    from logging import Logger

    import pyblish.api
    from ayon_mocha.api.lib import ExporterInfo

EXTENSION_PATTERN = re.compile(r"(?P<name>.+)\(\*\.(?P<ext>\w+)\)")


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
        """Process the output to representations."""
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
                if cols > 1:
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

        """
        file_name = f"{repre_name}.manifest"
        manifest_file = staging_dir / file_name
        with open(manifest_file, "w") as file:
            for file_path in files:
                file.write(f"{file_path}\n")
        return file_name

    def export(
            self,
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

            ext = self._get_extension(exporter_info)
            if not ext:
                msg = ("Cannot get extension "
                       f"from {exporter_info.label} exporter.")
                raise KnownPublishError(msg)

            exporter_short_hash = exporter_info.id[:8]
            file_name = f"{product_name}_{exporter_short_hash}.{ext}"

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
            for k, v in result.items():
                with open(k, "wb") as file:
                    file.write(v)
                output_files.append(Path(k).name)

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
            [path.as_posix(),  (publish_dir_path / path.name).as_posix()])


    @staticmethod
    def _get_extension(exporter_info: ExporterInfo) -> Optional[str]:
        """Get the extension of the exporter."""
        match = re.search(EXTENSION_PATTERN, exporter_info.label)
        return match["ext"] if match else None

    def _exporter_name_to_representation_name(
            self, exporter_name: str) -> str:
        """Convert the exporter name to representation name."""
        return SHAPE_EXPORTERS_REPRESENTATION_NAME_MAPPING.get(
            exporter_name, exporter_name)
