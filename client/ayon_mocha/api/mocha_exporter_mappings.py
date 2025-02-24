"""Exporters representation name mappings for Mocha.

This is a mapping of representation names to exporter ids as
the representation name has limits both in how it is now displayed
in the UI and how it is stored in the project - it is a string
without spaces and special characters. It must be updated now
and then to keep it in sync with the actual Mocha exporting
capabilities.
"""

TRACKING_MAPPING_2024_5 = {
    "2D SynthEyes Tracker Data (*.sni)": "SynthEyes2DTracker",
    "After Effects CC Power Pin (*.txt)": "AfxCCPowerPin",
    ("After Effects CS3 Corner Pin "
     "[supports motion blur, CS3 and older] (*.txt)"): "AfxCS3CornerPin",
    ("After Effects Corner Pin "
     "[corner pin only, supports "
     "RG Warp and mochaImport] (*.txt)"): "AfxCornerPin",
    ("After Effects Corner Pin "
     "[supports motion blur] (*.txt)"): "AfxCornerPinMotionBlur",
    ("After Effects Transform Data "
     "[position, scale and rotation] (*.txt)"): "AfxTransformData",
    "Alembic Mesh Data (*.abc)": "AlembicMeshData",
    "Alembic Vertex Transform Data (*.abc)": "AlembicVertexTransform",
    "Assimilate SCRATCH Corner Pin (*.txt)": "AssimilateSCRATCHCornerPin",
    "Autodesk Flame Axis (*.mask)": "FlameAxis",
    "Autodesk IFFFSE Point Tracker Data (*.ascii)": "IFFFSEPointTracker",
    ("Autodesk IFFFSE Point Tracker "
     "Data (Flame 2014) (*.ascii)"): "Flame2014PointTracker",
    "Autodesk IFFFSE Stabilizer Data (*.stabilizer)": "IFFFSEStabilizer",
    ("Autodesk IFFFSE Stabilizer Data "
    "(Flame 2014) (*.stabilizer)"): "Flame2014Stabilize",
    "Avid DS Tracking Data (*.fraw)": "AvidDSTrackingData",
    "Blackmagic Fusion COMP Data (*.comp)": "FusionCompData",
    ("Boris FX Center Point "
     "(Continuum 11 and older) (*.txt)"): "BorisFXCenterPoint",
    "Boris FX Corner Pin (Continuum 11 and older) (*.txt)": "BorisFXCornerPin",
    ("Final Cut Basic Motion "
     "[translate, rotate, scale] (*.xml)"): "FinalCutBasicMotion",
    "Final Cut Distort [corner pin] (*.xml)": "FinalCutDistort",
    "Flowbox corner pin (*.flowbox)": "FlowboxCornerPin",
    "HitFilm Corner Pin [supports motion blur] (*.hfcs)": "HitFilmCornerPin",
    ("HitFilm Transform Data "
     "[position, scale and rotation] (*.hfcs)"): "HitFilmTransformData",
    "Mistika Point Tracker File (*.trk)": "MistikaPointTracker",
    "MochaBlend tracking data (*.txt)": "MochaBlend",
    "Motion basic transform (*.motn)": "MotionBasicTransform",
    "Motion corner pin (*.motn)": "MotionCornerPin",
    "Nuke 7 Tracker (*.nk)": "Nuke7Tracker",
    "Nuke Ascii (*.txt)": "NukeAscii",
    "Nuke Corner Pin (*.nk)": "NukeCornerPin",
    "Nuke Mesh Tracker (*.nk)": "NukeMeshTracker",
    "Quantel Corner Pin Data (*.xml)": "QuantelCornerPin",
    "Shake Script (*.shk)": "ShakeScript",
    "Silhouette corner pin (*.txt)": "SilhouetteCornerPin",
}


SHAPE_MAPPING_2024_5 = {
    "Adobe After Effects Mask Data (*.shape4ae)": "AfxMask",
    "Adobe Premiere shape data (*.xml)": "PremiereShape",
    "BlackMagic Fusion 19+ MultiPoly shapes (*.comp)": "FusionMultiPoly",
    "BlackMagic Fusion shapes (*.comp)": "FusionShapes",
    "Combustion GMask Script (*.gmask)": "CombustionGMask",
    "Flame GMask Script (*.gmask)": "FlameGMask",
    "Flame Tracer [Basic] (*.mask)": "FlameTracerBasic",
    "Flame Tracer [Shape + Axis] (*.mask)": "FlameTracerShapeAxis",
    "HitFilm [Transform & Shape] (*.hfcs)": "HitFilmTransformShape",
    "Mocha shape data for Final Cut (*.xml)": "MochaShapeFinalCut",
    "MochaBlend shape data (*.txt)": "MochaBlend",
    "Nuke Roto [Basic] (*.nk)": "NukeRotoBasic",
    "Nuke RotoPaint [Basic] (*.nk)": "NukeRotoPaintBasic",
    "Nuke SplineWarp (*.nk)": "NukeSplineWarp",
    "Nuke v6.2+ Roto [Transform & Shape] (*.nk)": "NukeRotoTransformShape",
    "Nuke v6.2+ RotoPaint [Transform & Shape] (*.nk)": "NukeRotoPaint",
    "Shake Rotoshape (*.ssf)": "ShapeRotoshape",
    "Silhouette shapes (*.fxs)": "SilhouetteShapes",
}


TRACKING_MAPPING_2025 = {
    "After Effects CC Power Pin": "AfxCCPowerPin",
    "After Effects CS3 Corner Pin": "AfxCS3CornerPin",
    "After Effects Corner Pin": "AfxCornerPin",
    "After Effects Corner Pin with Motion Blur": "AfxCornerPinMotionBlur",
    "After Effects Transform Data": "AfxTransformData",
    "Alembic 2D Mesh Data": "AlembicMeshData",
    "Alembic 2D Vertex Transform": "AlembicVertexTransform",
    "Avid DS Tracking Data": "AvidDSTrackingData",
    "Continuum Center Point - 11.0.0": "BorisFXCenterPoint",
    "Continuum Corner Pin - 11.0.0": "BorisFXCornerPin",
    "Final Cut Basic Motion - 7.0.0": "FinalCutBasicMotion",
    "Final Cut Distort - 7.0.0": "FinalCutDistort",
    "Flame Axis": "FlameAxis",
    "Flame Point Stabilizer Data - 2014.0.0": "Flame2014Stabilize",
    "Flame Point Tracker Data": "IFFFSEPointTracker",
    "Flame Point Tracker Data - 2014.0.0": "Flame2014PointTracker",
    "Flame Stabilizer Data": "IFFFSEStabilizer",
    "Flowbox Corner Pin": "FlowboxCornerPin",
    "Fusion Tracker Data": "FusionCompData",
    "HitFilm Corner Pin with Motion Blur": "HitFilmCornerPin",
    "HitFilm Transform Data": "HitFilmTransformData",
    "Mistika Point Tracker File": "MistikaPointTracker",
    "MochaBlend Tracking Data": "MochaBlend",
    "Motion Basic Transform Data": "MotionBasicTransform",
    "Motion Corner Pin": "MotionCornerPin",
    "Nuke Ascii": "NukeAscii",
    "Nuke Corner Pin": "NukeCornerPin",
    "Nuke PowerMesh to Tracker Data": "NukePowerMesh",
    "Nuke Tracker Data - 7.0+": "Nuke7Tracker",
    "Quantel Corner Pin Data": "QuantelCornerPin",
    "SCRATCH Corner Pin Data": "AssimilateSCRATCHCornerPin",
    "Shake Tracking Data": "ShakeScript",
    "Silhouette Corner Pin": "SilhouetteCornerPin",
    "SynthEyes 2D Tracker Data": "SynthEyes2DTracker",
}


SHAPE_MAPPING_2025 = {
    "After Effects Mask Data": "AfxMask",
    "Combustion GMask Script": "CombustionGMask",
    "Final Cut Mocha Shape Data - 7.0.0": "FinalCutMochaShape",
    "Flame Gmask Script": "FlameGMask",
    "Flame Tracer [Basic]": "FlameTracerBasic",
    "Flame Tracer [Shape & Axis]": "FlameTracerShapeAxis",
    "Fusion MultiPoly Shape Data": "FusionMultiPoly",
    "Fusion Poly Shape Data": "FusionShapes",
    "HitFilm Mask Data": "HitFilmTransformShape",
    "MochaBlend Shape Data": "MochaBlend",
    "Nuke Roto [Basic]": "NukeRotoBasic",
    "Nuke Roto [Transform & Shape]-6.2+": "NukeRotoTransformShape",
    "Nuke RotoPaint [Basic]": "NukeRotoPaintBasic",
    "Nuke RotoPaint [Transform & Shape] - 6.2+": "NukeRotoPaint",
    "Nuke SplineWarp": "NukeSplineWarp",
    "Premiere Shape Data": "PremiereShape",
    "Shake RotoShape": "ShapeRotoshape",
    "Silhouette Shape Data": "SilhouetteShapes",
}


EXPORTER_MAPPING = {
    "shape": {
        "2024.5": SHAPE_MAPPING_2024_5,
        "2025": SHAPE_MAPPING_2025,
    },
    "tracking": {
        "2024.5": TRACKING_MAPPING_2024_5,
        "2025": TRACKING_MAPPING_2025,
    }
}
