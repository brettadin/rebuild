from src.ui.panels.graph_panel.graph_panel import GraphPanel
from src.graphing.overlays.line_overlays import LineOverlay
from src.search.models.line_result import LineResult
from src.domain.datasets.registry import get_dataset_repo
from src.domain.datasets.dataset_model import DatasetModel, DatasetMetadata


def test_overlay_toggle(qtbot):
    ds_repo = get_dataset_repo()
    ds_repo._datasets = {}
    md = DatasetMetadata(units_x='nm')
    ds = DatasetModel(id='ds1', x=[1.0], y=[10], metadata=md)
    ds_repo.add(ds)

    gp = GraphPanel()
    qtbot.addWidget(gp)
    gp.manager.add_dataset(ds)
    overlay = LineOverlay(id='FeI_1', element='Fe', ion='I', x=386.0, dataset_id='ds1', metadata={})
    gp.manager.set_line_overlays([overlay])
    assert any(o.id == 'FeI_1' for o in gp.manager.line_overlay_manager.lines)
    # toggle off overlays globally
    gp.toggle_overlays_cb.setChecked(False)
    assert gp.manager.line_overlay_manager.lines == []
    # toggle on overlays globally
    gp.toggle_overlays_cb.setChecked(True)
    assert any(o.id == 'FeI_1' for o in gp.manager.line_overlay_manager.lines)
    # test per-dataset toggle: it should affect only overlay visibility flag
    # ensure dataset selected
    gp.list_widget.setCurrentItem(gp.list_widget.item(0))
    # per-dataset toggle off
    gp.show_dataset_overlays_cb.setChecked(False)
    # overlay should still be present but mark as not visible
    assert any(o.id == 'FeI_1' and not o.visible for o in gp.manager.line_overlay_manager.lines)
    # per-dataset toggle on
    gp.show_dataset_overlays_cb.setChecked(True)
    assert any(o.id == 'FeI_1' and o.visible for o in gp.manager.line_overlay_manager.lines)
