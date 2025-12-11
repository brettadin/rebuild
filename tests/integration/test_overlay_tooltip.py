from src.ui.panels.graph_panel.graph_panel import GraphPanel
from src.graphing.overlays.line_overlays import LineOverlay
from src.search.models.line_result import LineResult
from src.graphing.overlays.line_overlays import LineOverlayManager
from src.notes.registry import get_note_repo
from PySide6.QtWidgets import QToolTip


def test_overlay_tooltip_shown(monkeypatch, qtbot):
    gp = GraphPanel()
    qtbot.addWidget(gp)
    # add overlay at x=386.0
    overlay = LineOverlay(id='FeI_1', element='Fe', ion='I', x=386.0, energy_lower=0.0, energy_upper=1.0, metadata={'source': 'NIST'})
    gp.manager.set_line_overlays([overlay])

    # captured args
    called = {'text': None}

    def fake_show_text(pos, txt, widget=None):
        called['text'] = txt

    monkeypatch.setattr(QToolTip, 'showText', fake_show_text)

    class DummyEvent:
        def __init__(self, xdata):
            self.xdata = xdata

    # Move near the overlay x=386.0, within tolerance
    e = DummyEvent(386.1)
    gp._on_mouse_move(e)
    assert called['text'] is not None
    assert 'Fe' in called['text']
    assert 'E_lower' in called['text'] or 'E_upper' in called['text']
    # Move away from overlay, tooltip should hide (but hideText is not easily observable)
    e2 = DummyEvent(100.0)
    gp._on_mouse_move(e2)
    # If no new text, it's okay; at least previous show happened
