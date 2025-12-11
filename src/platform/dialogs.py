import os
import logging
from PySide6.QtWidgets import QMessageBox

log = logging.getLogger(__name__)


def should_show_popups() -> bool:
    val = os.environ.get('REBUILD_DISABLE_AUTO_POPUPS', '')
    return not (val.lower() in ('1', 'true', 'yes'))


def maybe_warning(parent, title: str, message: str):
    """Display a QMessageBox.warning unless REBUILD_DISABLE_AUTO_POPUPS is set.
    When suppression is on, log a warning instead of showing a dialog.
    """
    if should_show_popups():
        QMessageBox.warning(parent, title, message)
    else:
        log.warning('Suppressed warning dialog: %s - %s', title, message)
