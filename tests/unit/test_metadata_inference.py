from src.domain.datasets.dataset_metadata import infer_metadata_from_filepath, infer_units_from_header


def test_infer_metadata_from_filepath():
    md = infer_metadata_from_filepath('local_lab/planet_spectrum.csv')
    assert md.object_type == 'planet'
    md2 = infer_metadata_from_filepath('file_nist_fe_i.csv')
    assert md2.object_type == 'element'
    md3 = infer_metadata_from_filepath('my_lab_data.csv')
    assert md3.object_type == 'unknown'


def test_infer_units_from_header():
    out = infer_units_from_header('wavelength_nm,flux')
    assert out['units_x'] == 'nm'
    assert out['units_y'] == 'flux'
    out2 = infer_units_from_header('wavenumber, intensity')
    assert out2['units_x'] == 'cm^-1'
