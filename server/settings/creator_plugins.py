"""Creator settings for Mocha Pro."""
from __future__ import annotations

from ayon_server.settings import BaseSettingsModel, SettingsField


def tracking_exporter_enum_2024_5() -> list[dict[str, str]]:
    """Return enum for tracking exporters."""
    return [
        {
            "label": "2D SynthEyes Tracker Data (*.sni)",
            "value": "SynthEyes2DTracker"},
        {
            "label": "After Effects CC Power Pin (*.txt)",
            "value": "AfxCCPowerPin"},
        {
            "label": ("After Effects CS3 Corner Pin [supports motion blur, "
                      "CS3 and older] (*.txt)"),
            "value": "AfxCS3CornerPin"},
        {
            "label": ("After Effects Corner Pin [corner pin only, "
                      "supports RG Warp and mochaImport] (*.txt)"),
            "value": "AfxCornerPin"},
        {
            "label": ("After Effects Corner Pin "
                      "[supports motion blur] (*.txt)"),
            "value": "AfxCornerPinMotionBlur"},
        {
            "label": ("After Effects Transform Data [position, "
                      "scale and rotation] (*.txt)"),
            "value": "AfxTransformData"},
        {
            "label": "Alembic Mesh Data (*.abc)",
            "value": "AlembicMeshData"},
        {
            "label": "Alembic Vertex Transform Data (*.abc)",
            "value": "AlembicVertexTransform"},
        {
            "label": "Assimilate SCRATCH Corner Pin (*.txt)",
            "value": "AssimilateSCRATCHCornerPin"},
        {
            "label": "Autodesk Flame Axis (*.mask)",
            "value": "FlameAxis"},
        {
            "label": "Autodesk IFFFSE Point Tracker Data (*.ascii)",
            "value": "IFFFSEPointTracker"},
        {
            "label": ("Autodesk IFFFSE Point Tracker Data "
                      "(Flame 2014) (*.ascii)"),
            "value": "Flame2014PointTracker"},
        {
            "label": "Autodesk IFFFSE Stabilizer Data (*.stabilizer)",
            "value": "IFFFSEStabilizer"},
        {
            "label": ("Autodesk IFFFSE Stabilizer Data (Flame 2014) "
                      "(*.stabilizer)"),
            "value": "Flame2014Stabilize"},
        {
            "label": "Avid DS Tracking Data (*.fraw)",
            "value": "AvidDSTrackingData"},
        {
            "label": "Blackmagic Fusion COMP Data (*.comp)",
            "value": "FusionCompData"},
        {
            "label": "Boris FX Center Point (Continuum 11 and older) (*.txt)",
            "value": "BorisFXCenterPoint"},
        {
            "label": "Boris FX Corner Pin (Continuum 11 and older) (*.txt)",
            "value": "BorisFXCornerPin"},
        {
            "label": ("Final Cut Basic Motion "
                      "[translate, rotate, scale] (*.xml)"),
            "value": "FinalCutBasicMotion"},
        {
            "label": "Final Cut Distort [corner pin] (*.xml)",
            "value": "FinalCutDistort"},
        {
            "label": "Flowbox corner pin (*.flowbox)",
            "value": "FlowboxCornerPin"},
        {
            "label": "HitFilm Corner Pin [supports motion blur] (*.hfcs)",
            "value": "HitFilmCornerPin"},
        {
            "label": ("HitFilm Transform Data "
                      "[position, scale and rotation] (*.hfcs)"),
            "value": "HitFilmTransformData"},
        {
            "label": "Mistika Point Tracker File (*.trk)",
            "value": "MistikaPointTracker"},
        {
            "label": "MochaBlend tracking data (*.txt)",
            "value": "MochaBlend"},
        {
            "label": "Motion basic transform (*.motn)",
            "value": "MotionBasicTransform"},
        {
            "label": "Motion corner pin (*.motn)",
            "value": "MotionCornerPin"},
        {
            "label": "Nuke 7 Tracker (*.nk)",
            "value": "Nuke7Tracker"},
        {
            "label": "Nuke Ascii (*.txt)",
            "value": "NukeAscii"},
        {
            "label": "Nuke Corner Pin (*.nk)",
            "value": "NukeCornerPin"},
        {
            "label": "Nuke Mesh Tracker (*.nk)",
            "value": "NukeMeshTracker"},
        {
            "label": "Quantel Corner Pin Data (*.xml)",
            "value": "QuantelCornerPin"},
        {
            "label": "Shake Script (*.shk)",
            "value": "ShakeScript"},
        {
            "label": "Silhouette corner pin (*.txt)",
            "value": "SilhouetteCornerPin"},
    ]


def tracking_exporter_enum_2025() -> list[dict[str, str]]:
    """Return enum for tracking exporters."""
    return [
        {
            "label": "After Effects CC Power Pin",
            "value": "AfxCCPowerPin",
        },
        {
            "label": "After Effects CS3 Corner Pin",
            "value": "AfxCS3CornerPin",
        },
        {
            "label": "After Effects Corner Pin",
            "value": "AfxCornerPin",
        },
        {
            "label": "After Effects Corner Pin with Motion Blur",
            "value": "AfxCornerPinMotionBlur",
        },
        {
            "label": "After Effects Transform Data",
            "value": "AfxTransformData",
        },
        {
            "label": "Alembic 2D Mesh Data",
            "value": "AlembicMeshData",
        },
        {
            "label": "Alembic 2D Vertex Transform",
            "value": "AlembicVertexTransform",
        },
        {
            "label": "Avid DS Tracking Data",
            "value": "AvidDSTrackingData",
        },
        {
            "label": "Continuum Center Point - 11.0.0",
            "value": "BorisFXCenterPoint",
        },
        {
            "label": "Continuum Corner Pin - 11.0.0",
            "value": "BorisFXCornerPin",
        },
        {
            "label": "Final Cut Basic Motion - 7.0.0",
            "value": "FinalCutBasicMotion",
        },
        {
            "label": "Final Cut Distort - 7.0.0",
            "value": "FinalCutDistort",
        },
        {
            "label": "Flame Axis",
            "value": "FlameAxis",
        },
        {
            "label": "Flame Point Stabilizer Data - 2014.0.0",
            "value": "Flame2014Stabilize",
        },
        {
            "label": "Flame Point Tracker Data",
            "value": "IFFFSEPointTracker",
        },
        {
            "label": "Flame Point Tracker Data - 2014.0.0",
            "value": "Flame2014PointTracker",
        },
        {
            "label": "Flame Stabilizer Data",
            "value": "IFFFSEStabilizer",
        },
        {
            "label": "Flowbox Corner Pin",
            "value": "FlowboxCornerPin",
        },
        {
            "label": "Fusion Tracker Data",
            "value": "FusionCompData",
        },
        {
            "label": "HitFilm Corner Pin with Motion Blur",
            "value": "HitFilmCornerPin",
        },
        {
            "label": "HitFilm Transform Data",
            "value": "HitFilmTransformData",
        },
        {
            "label": "Mistika Point Tracker File",
            "value": "MistikaPointTracker",
        },
        {
            "label": "MochaBlend Tracking Data",
            "value": "MochaBlend",
        },
        {
            "label": "Motion Basic Transform Data",
            "value": "MotionBasicTransform",
        },
        {
            "label": "Motion Corner Pin",
            "value": "MotionCornerPin",
        },
        {
            "label": "Nuke Ascii",
            "value": "NukeAscii",
        },
        {
            "label": "Nuke Corner Pin",
            "value": "NukeCornerPin",
        },
        {
            "label": "Nuke PowerMesh to Tracker Data",
            "value": "NukePowerMesh",
        },
        {
            "label": "Nuke Tracker Data - 7.0+",
            "value": "Nuke7Tracker",
        },
        {
            "label": "Quantel Corner Pin Data",
            "value": "QuantelCornerPin",
        },
        {
            "label": "SCRATCH Corner Pin Data",
            "value": "AssimilateSCRATCHCornerPin",
        },
        {
            "label": "Shake Tracking Data",
            "value": "ShakeScript",
        },
        {
            "label": "Silhouette Corner Pin",
            "value": "SilhouetteCornerPin",
        },
        {
            "label": "SynthEyes 2D Tracker Data",
            "value": "SynthEyes2DTracker",
        },
    ]


def shapes_exporter_enum_2024_5() -> list[dict[str, str]]:
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


def shapes_exporter_enum_2025() -> list[dict[str, str]]:
    """Return enum for shape exporters form Mocha Pro 2025."""
    return [
        {
            "label": "After Effects Mask Data",
            "value": "AfxMask",
        },
        {
            "label": "Combustion GMask Script",
            "value": "CombustionGMask",
        },
        {
            "label": "Final Cut Mocha Shape Data - 7.0.0",
            "value": "FinalCutMochaShape",
        },
        {
            "label": "Flame Gmask Script",
            "value": "FlameGMask",
        },
        {
            "label": "Flame Tracer [Basic]",
            "value": "FlameTracerBasic",
        },
        {
            "label": "Flame Tracer [Shape & Axis]",
            "value": "FlameTracerShapeAxis",
        },
        {
            "label": "Fusion MultiPoly Shape Data",
            "value": "FusionMultiPoly",
        },
        {
            "label": "Fusion Poly Shape Data",
            "value": "FusionShapes",
        },
        {
            "label": "HitFilm Mask Data",
            "value": "HitFilmTransformShape",
        },
        {
            "label": "MochaBlend Shape Data",
            "value": "MochaBlend",
        },
        {
            "label": "Nuke Roto [Basic]",
            "value": "NukeRotoBasic",
        },
        {
            "label": "Nuke Roto [Transform & Shape]-6.2+",
            "value": "NukeRotoTransformShape",
        },
        {
            "label": "Nuke RotoPaint [Basic]",
            "value": "NukeRotoPaintBasic",
        },
        {
            "label": "Nuke RotoPaint [Transform & Shape] - 6.2+",
            "value": "NukeRotoPaint",
        },
        {
            "label": "Nuke SplineWarp",
            "value": "NukeSplineWarp",
        },
        {
            "label": "Premiere Shape Data",
            "value": "PremiereShape",
        },
        {
            "label": "Shake RotoShape",
            "value": "ShapeRotoshape",
        },
        {
            "label": "Silhouette Shape Data",
            "value": "SilhouetteShapes",
        },
    ]


class Mocha2024TrackingModel(BaseSettingsModel):
    """Mocha Pro 2024 tracking settings."""
    default_exporters: list[str] = SettingsField(
        default_factory=list, title="Default exporters",
        enum_resolver=tracking_exporter_enum_2024_5)


class Mocha2025TrackingModel(BaseSettingsModel):
    """Mocha Pro 2025 tracking settings."""
    default_exporters: list[str] = SettingsField(
        default_factory=list, title="Default exporters",
        enum_resolver=tracking_exporter_enum_2025)


class CreateTrackingPointsModel(BaseSettingsModel):
    """Settings for creating tracking points."""
    enabled: bool = SettingsField(
        default=True, title="Enabled")
    mocha_2024_5: Mocha2024TrackingModel = SettingsField(
        default_factory=Mocha2024TrackingModel,
        title="Mocha Pro 2024")
    mocha_2025: Mocha2025TrackingModel = SettingsField(
        default_factory=Mocha2025TrackingModel,
        title="Mocha Pro 2025")


class Mocha2024ShapeModel(BaseSettingsModel):
    """Mocha Pro 2024 shape settings."""
    default_exporters: list[str] = SettingsField(
        default_factory=list, title="Default exporters",
        enum_resolver=shapes_exporter_enum_2024_5)


class Mocha2025ShapeModel(BaseSettingsModel):
    """Mocha Pro 2025 shape settings."""
    default_exporters: list[str] = SettingsField(
        default_factory=list, title="Default exporters",
        enum_resolver=shapes_exporter_enum_2025)


class CreateShapeDataModel(BaseSettingsModel):
    """Settings for creating shapes."""
    enabled: bool = SettingsField(
        default=True, title="Enabled")
    mocha_2024_5: Mocha2024ShapeModel = SettingsField(
        default_factory=Mocha2024ShapeModel,
        title="Mocha Pro 2024")
    mocha_2025: Mocha2025ShapeModel = SettingsField(
        default_factory=Mocha2025ShapeModel,
        title="Mocha Pro 2025")


class MochaProCreatorPlugins(BaseSettingsModel):
    """Mocha Pro creator plugins settings."""
    CreateTrackingPoints: CreateTrackingPointsModel = SettingsField(
        default_factory=CreateTrackingPointsModel,
        title="Create Tracking Points")
    CreateShapeData: CreateShapeDataModel = SettingsField(
        default_factory=CreateShapeDataModel,
        title="Create Shapes")
