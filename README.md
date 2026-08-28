# SIH 2026 - Deep Learning Based Satellite Super-Resolution Mapping (SRM)

A comprehensive, production-grade GIS pre-processing and post-processing subsystem for satellite imagery super-resolution.

---

## 🌟 GIS Subsystem Architecture

```
                       ┌──────────────────────────────────────────────┐
                       │           RAW SATELLITE GEOTIFF             │
                       │    (Sentinel-2, Landsat-8, OLI2MSI, etc.)    │
                       └──────────────────────┬───────────────────────┘
                                              │
                    ┌─────────────────────────▼─────────────────────────┐
                    │        1. GIS PRE-PROCESSING ENGINE              │
                    │   • Multi-Sensor Ingestion & CRS Validation       │
                    │   • Radiometric TOA / Reflectance Normalization  │
                    │   • NoData / Cloud Masking & Manifest Logging     │
                    │   • Sliding-Window Scene Tiling with Overlap      │
                    │   • Synthetic Sensor Degradation / Real Pairing   │
                    └─────────────────────────┬─────────────────────────┘
                                              │
                                  [Normalized Tile Patches]
                                              │
                    ┌─────────────────────────▼─────────────────────────┐
                    │        2. MACHINE LEARNING SUPER-RESOLUTION      │
                    │   • SRCNN / EDSR / RCAN / SwinIR Upsampling       │
                    └─────────────────────────┬─────────────────────────┘
                                              │
                               [Super-Resolved Patches]
                                              │
                    ┌─────────────────────────▼─────────────────────────┐
                    │        3. GIS POST-PROCESSING ENGINE             │
                    │   • 2D Cosine / Gaussian Overlap Blending         │
                    │   • Spatial Resolution & Geotransform Rescaling   │
                    │   • Radiometric De-normalization                  │
                    │   • Cloud-Optimized GeoTIFF (COG) & Overviews     │
                    └─────────────────────────┬─────────────────────────┘
                                              │
                    ┌─────────────────────────▼─────────────────────────┐
                    │     4. DOWNSTREAM GIS & REMOTE SENSING PRODUCTS  │
                    │   • Biophysical Indices (NDVI, NDWI, NDBI, EVI)  │
                    │   • Vector Feature Extraction (GeoJSON Polygons)  │
                    │   • Quantitative Metrics (SAM, ERGAS, PSNR, SSIM) │
                    │   • Interactive Web GIS Studio Viewer (Leaflet)   │
                    └───────────────────────────────────────────────────┘
```

---

## 📁 Package Structure

```
srm-satellite-gis/
├── src/
│   ├── gis/
│   │   ├── __init__.py           # Export high-level GIS API
│   │   ├── raster_utils.py       # Raster I/O, CRS reprojection, georeferenced export
│   │   ├── preprocessor.py       # Normalizer (percentile, minmax, reflectance, zscore)
│   │   ├── tiling.py             # Sliding-window tiling with overlap & GeoJSON footprints
│   │   ├── pair_generator.py     # Sensor PSF blur, noise degradation, training pair generation
│   │   ├── postprocessor.py      # Seamless mosaicker with 2D cosine/gaussian overlap blending
│   │   ├── indices.py            # Spectral index engine (NDVI, NDWI, NDBI, EVI, SAVI)
│   │   ├── vectorizer.py         # Vector polygon extraction (GeoJSON water/veg/urban masks)
│   │   ├── metrics.py            # RS fidelity metrics (SAM, ERGAS, UIQI, PSNR, SSIM)
│   │   ├── cog.py                # Cloud-Optimized GeoTIFF & image pyramid generator
│   │   ├── sample_data.py        # Synthetic multi-band satellite scene generator
│   │   ├── pipeline.py           # End-to-end full scene GIS pipeline orchestrator
│   │   └── cli.py                # Unified command-line interface
│   │
│   ├── dl/                       # PyTorch models (SRCNN, EDSR), dataset loader, training
│   ├── backend/                  # FastAPI service with Web GIS studio endpoints
│   ├── viewer/                   # Interactive Leaflet Web GIS studio (split-slider, indices)
│   └── utils/                    # Shared YAML config loader
│
├── data/                         # Raw scenes, tiles, samples
├── outputs/                      # Super-resolved GeoTIFFs & downstream products
└── tests/                        # Full automated test suite (15 unit & integration tests)
```

---

## 🚀 Quickstart & Usage

### 1. Generate Synthetic Sample Scene
```bash
python -m src.gis.cli sample --output data/raw/sample_scene.tif
```

### 2. GIS Pre-Processing (Tiling & Training Pair Generator)
```bash
python -m src.gis.cli preprocess --input data/raw --output data/tiles --scale 4
```

### 3. Run Full End-to-End GIS Pipeline
```bash
python -m src.gis.cli pipeline --input data/raw/sample_scene.tif --output outputs/sr_scene.tif --scale 4 --indices --vectorize
```

### 4. Calculate Spectral Vegetation, Water & Urban Indices
```bash
python -m src.gis.cli indices --input outputs/sr_scene.tif --output outputs/indices
```

### 5. Extract Vector Polygons (GeoJSON)
```bash
python -m src.gis.cli vectorize --input outputs/sr_scene.tif --output outputs/vectors
```

### 6. Evaluate Remote Sensing Metrics vs Ground Truth HR
```bash
python -m src.gis.cli evaluate --pred outputs/sr_scene.tif --target data/raw/ground_truth_hr.tif --scale 4 --output outputs/evaluation
```

### 7. Run Interactive Web GIS Studio
```bash
uvicorn src.backend.main:app --reload --port 8000
```
Open `http://localhost:8000` in your browser to view the interactive map with split comparison slider, live index inspector, and vector layers!

---

## 🧪 Run Automated Tests

```bash
pytest tests/ -v
```
All 15 unit and integration tests verify raster I/O, geotransform scaling, sliding window tiling, overlap blending, spectral indices, vector polygon extraction, metrics (SAM, ERGAS, PSNR, SSIM), and full pipeline execution.
