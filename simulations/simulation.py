#!/usr/bin/env python3
"""Minimal LSC 5.0 energy-reconstruction toy simulation.

The original script required NumPy and Matplotlib and opened an interactive
plot. This version uses only the Python standard library and writes reproducible
CSV/SVG outputs that can be committed or inspected in CI.
"""

from __future__ import annotations

import csv
from pathlib import Path


def cross_section_ratio(energy: float, delta: float) -> float:
    """Toy sigma_true/sigma_observed ratio for sigma proportional to E^2."""
    observed = energy**2
    shifted = (energy * (1.0 + delta)) ** 2
    return shifted / observed


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    delta = 0.05
    energies = [0.5 + i * (4.5 / 99) for i in range(100)]
    rows = [{"energy": f"{e:.6f}", "delta": f"{delta:.6f}", "sigma_ratio": f"{cross_section_ratio(e, delta):.6f}"} for e in energies]

    csv_path = out_dir / "lsc5_energy_reconstruction.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["energy", "delta", "sigma_ratio"])
        writer.writeheader()
        writer.writerows(rows)

    width, height = 760, 420
    left, right, top, bottom = 60, 30, 30, 55
    plot_w = width - left - right
    plot_h = height - top - bottom
    y_min, y_max = 1.0, 1.2

    def map_x(e: float) -> float:
        return left + (e - min(energies)) / (max(energies) - min(energies)) * plot_w

    def map_y(y: float) -> float:
        return top + (y_max - y) / (y_max - y_min) * plot_h

    points = " ".join(f"{map_x(e):.2f},{map_y(cross_section_ratio(e, delta)):.2f}" for e in energies)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="white"/>
  <text x="{width / 2}" y="22" text-anchor="middle" font-size="18" font-family="Arial">LSC 5.0 toy energy reconstruction response</text>
  <line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#333"/>
  <line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#333"/>
  <polyline points="{points}" fill="none" stroke="#0066cc" stroke-width="3"/>
  <text x="{width / 2}" y="{height - 16}" text-anchor="middle" font-size="14" font-family="Arial">Energy [arbitrary units]</text>
  <text x="18" y="{height / 2}" transform="rotate(-90 18 {height / 2})" text-anchor="middle" font-size="14" font-family="Arial">sigma shifted / sigma observed</text>
</svg>
"""
    svg_path = out_dir / "lsc5_energy_reconstruction.svg"
    svg_path.write_text(svg, encoding="utf-8")

    print(f"Wrote {csv_path}")
    print(f"Wrote {svg_path}")


if __name__ == "__main__":
    main()
