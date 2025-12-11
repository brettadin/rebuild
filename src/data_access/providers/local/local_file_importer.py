import csv
import json
from pathlib import Path
from typing import Optional
from src.domain.datasets.dataset_model import DatasetModel, DatasetMetadata
from src.domain.datasets.dataset_metadata import infer_metadata_from_filepath, infer_units_from_header
import uuid


class LocalFileImporter:
    """ Minimal local file importer supporting CSV and TXT formats.

    CSV expected columns: wavelength, flux (or x, y). Header is optional. First numeric column is x, second numeric is y.
    """

    def parse_csv(self, path: Path, units_x: str = "", units_y: str = "") -> DatasetModel:
        x = []
        y = []
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            # Try header detection
            first = next(reader)
            try:
                # if first row is numeric
                float(first[0])
                float(first[1])
                x.append(float(first[0]))
                y.append(float(first[1]))
            except Exception:
                # assume header; try to infer units from header line
                header_line = ','.join(first)
                inferred = infer_units_from_header(header_line)
                if not units_x:
                    units_x = inferred.get('units_x', '')
                if not units_y:
                    units_y = inferred.get('units_y', '')
            for row in reader:
                if len(row) < 2:
                    continue
                try:
                    xv = float(row[0])
                    yv = float(row[1])
                    x.append(xv)
                    y.append(yv)
                except Exception:
                    continue
        md = DatasetMetadata(units_x=units_x, units_y=units_y, provenance={"path": str(path)})
        # add filename and inferred object_type from path heuristics
        md.filename = path.name
        inferred_md = infer_metadata_from_filepath(str(path))
        if inferred_md.object_type != 'unknown':
            md.object_type = inferred_md.object_type
        ds = DatasetModel(id=str(uuid.uuid4()), x=x, y=y, metadata=md)
        return ds

    def parse_txt(self, path: Path, units_x: str = "", units_y: str = "") -> DatasetModel:
        # simple whitespace-separated values
        x = []
        y = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                stripped = line.strip()
                if not stripped or stripped.startswith('#'):
                    continue
                parts = stripped.split()
                if len(parts) < 2:
                    continue
                try:
                    xv = float(parts[0])
                    yv = float(parts[1])
                    x.append(xv)
                    y.append(yv)
                except Exception:
                    continue
        md = DatasetMetadata(units_x=units_x, units_y=units_y, provenance={"path": str(path)})
        md.filename = path.name
        inferred_md = infer_metadata_from_filepath(str(path))
        if inferred_md.object_type != 'unknown':
            md.object_type = inferred_md.object_type
        ds = DatasetModel(id=str(uuid.uuid4()), x=x, y=y, metadata=md)
        return ds

    def import_file(self, path: str, units_x: str = "", units_y: str = "") -> Optional[DatasetModel]:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(path)
        ext = p.suffix.lower()
        if ext in ['.csv']:
            return self.parse_csv(p, units_x, units_y)
        if ext in ['.txt', '.dat']:
            return self.parse_txt(p, units_x, units_y)
        # Placeholder for FITS etc. Could implement with astropy later
        raise ValueError(f"Unsupported file type: {ext}")

    def export_csv(self, dataset: DatasetModel, out_path: str):
        p = Path(out_path)
        with open(p, 'w', encoding='utf-8', newline='') as f:
            # Write metadata as JSON header inside comment lines
            meta = dataset.metadata
            header = f"# METADATA: {json.dumps(dataset.to_dict()['metadata'])}\n"
            f.write(header)
            writer = csv.writer(f)
            writer.writerow(["x", "y"])  # header
            for xv, yv in zip(dataset.x, dataset.y):
                writer.writerow([xv, yv])
