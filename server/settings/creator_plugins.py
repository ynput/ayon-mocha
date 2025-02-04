"""Creator settings for Mocha Pro."""
from __future__ import annotations

from ayon_server.settings import BaseSettingsModel, SettingsField


def shapes_exporter_enum() -> list[dict[str, str]]:
    """Return enum for shape exporters."""
    return [
        {
            "label": "Adobe After Effects Mask Data (*.shape4ae)",
            "value": "AfxMask"},
        {
            "label": "Adobe Premiere shape data (*.xml)",
            "value":  "PremiereShape"},
        {
            "label": "BlackMagic Fusion 19+ MultiPoly shapes (*.comp)",
            "value":  "FusionMultiPoly"},
        {
            "label": "BlackMagic Fusion shapes (*.comp)",
            "value":  "FusionShapes"},
        {
            "label": "Combustion GMask Script (*.gmask)",
            "value":  "CombustionGMask"},
        {
            "label": "Flame GMask Script (*.gmask)",
            "value":  "FlameGMask"},
        {
            "label": "Flame Tracer [Basic] (*.mask)",
            "value":  "FlameTracerBasic"},
        {
            "label": "Flame Tracer [Shape + Axis] (*.mask)",
            "value":  "FlameTracerShapeAxis"},
        {
            "label": "HitFilm [Transform & Shape] (*.hfcs)",
            "value":  "HitFilmTransformShape"},
        {
            "label": "Mocha shape data for Final Cut (*.xml)",
            "value":  "MochaShapeFinalCut"},
        {
            "label": "MochaBlend shape data (*.txt)",
            "value": "MochaBlend"},
        {
            "label": "Nuke Roto [Basic] (*.nk)",
            "value":  "NuRotoBasic"},
        {
            "label": "Nuke RotoPaint [Basic] (*.nk)",
            "value":  "NukeRotoPaintBasic"},
        {
            "label": "Nuke SplineWarp (*.nk)",
            "value": "NukeSplineWarp"},
        {
            "label": "Nuke v6.2+ Roto [Transform & Shape] (*.nk)",
            "value":  "NukeRotoTransformShape"},
        {
            "label": "Nuke v6.2+ RotoPaint [Transform & Shape] (*.nk)",
            "value":  "NukeRotoPaint"},
        {
            "label": "Shake Rotoshape (*.ssf)",
            "value":  "ShapeRotoshape"},
        {
            "label": "Silhouette shapes (*.fxs)",
            "value":  "SilhouetteShapes"},
    ]

class CreateShapeDataModel(BaseSettingsModel):
    """Settings for creating shapes."""
    enabled: bool = SettingsField(
        default=True, title="Enabled")
    default_exporters: list[str] = SettingsField(
        default_factory=list, title="Default exporters",
        enum_resolver=shapes_exporter_enum)


class MochaProCreatorPlugins(BaseSettingsModel):
    """Mocha Pro creator plugins settings."""
    CreateShapeData: CreateShapeDataModel = SettingsField(
        default_factory=CreateShapeDataModel,
        title="Create Shapes")
