"""
Turn raw medium-resolution scenes into LR/HR tile pairs for training.

Typical SRM setup: you don't have real "ground truth high-res" imagery
for the same scene, so the common approach is:
  1. Treat your available medium-res image as the HR target.
  2. Synthetically downsample it (bicubic/Gaussian blur + downsample)
     to create the LR input.
  3. Train the model to learn LR -> HR, then apply it to real medium-res
     imagery to produce a genuinely higher-resolution output.

If you DO have paired coarse/fine imagery (e.g. Sentinel-2 vs PlanetScope
over the same area), skip step 2 and pair them directly after
co-registration/reprojection instead.
"""
import argparse
from pathlib import Path

import numpy as np
import cv2
from tqdm import tqdm

from src.gis.raster_utils import read_raster
from src.utils.config import load_config


def normalize(arr: np.ndarray) -> np.ndarray:
    """Per-band min-max normalize to [0,1]; satellite bands vary wildly in range."""
    out = np.zeros_like(arr, dtype=np.float32)
    for c in range(arr.shape[0]):
        band = arr[c]
        lo, hi = np.percentile(band, 2), np.percentile(band, 98)  # clip outliers
        out[c] = np.clip((band - lo) / (hi - lo + 1e-6), 0, 1)
    return out


def make_lr(hr_tile: np.ndarray, scale_factor: int) -> np.ndarray:
    """Blur + downsample to simulate a lower-resolution sensor, then upscale
    back with bicubic so LR and HR tiles are the same array shape (standard
    SR training convention)."""
    c, h, w = hr_tile.shape
    lr = np.zeros_like(hr_tile)
    for i in range(c):
        blurred = cv2.GaussianBlur(hr_tile[i], (5, 5), 0)
        down = cv2.resize(blurred, (w // scale_factor, h // scale_factor), interpolation=cv2.INTER_AREA)
        lr[i] = cv2.resize(down, (w, h), interpolation=cv2.INTER_CUBIC)
    return lr


def tile_scene(scene_path: Path, out_dir: Path, tile_size: int, overlap: int,
                scale_factor: int, bands: list[int]):
    arr, _ = read_raster(str(scene_path), bands=bands)
    arr = normalize(arr)
    c, h, w = arr.shape
    step = tile_size - overlap

    idx = 0
    for y in range(0, h - tile_size, step):
        for x in range(0, w - tile_size, step):
            hr_tile = arr[:, y:y + tile_size, x:x + tile_size]
            lr_tile = make_lr(hr_tile, scale_factor)

            stem = f"{scene_path.stem}_{idx:05d}"
            np.save(out_dir / f"{stem}_hr.npy", hr_tile)
            np.save(out_dir / f"{stem}_lr.npy", lr_tile)
            idx += 1
    return idx


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="src/utils/config.yaml")
    args = parser.parse_args()

    cfg = load_config(args.config)
    raw_dir = Path(cfg["paths"]["raw_dir"])
    tiles_dir = Path(cfg["paths"]["tiles_dir"])
    tiles_dir.mkdir(parents=True, exist_ok=True)

    scenes = sorted(raw_dir.glob("*.tif"))
    if not scenes:
        print(f"No .tif scenes found in {raw_dir}. Add raw imagery there first.")
        return

    total = 0
    for scene in tqdm(scenes, desc="Tiling scenes"):
        total += tile_scene(
            scene, tiles_dir,
            cfg["gis"]["tile_size"], cfg["gis"]["overlap"],
            cfg["gis"]["scale_factor"], cfg["gis"]["bands"],
        )
    print(f"Wrote {total} LR/HR tile pairs to {tiles_dir}")


if __name__ == "__main__":
    main()
