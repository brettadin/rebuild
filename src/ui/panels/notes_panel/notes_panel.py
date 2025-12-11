from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QTextEdit, QLabel
from src.notes.registry import get_note_repo


class NotesPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.note_repo = get_note_repo()
        self._build_ui()
        self.refresh_notes_list()

    def _build_ui(self):
        layout = QVBoxLayout()
        header = QLabel("Notes")
        header.setObjectName("panelHeader")
        layout.addWidget(header)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()
        self.btn_refresh = QPushButton("Refresh")
        self.btn_delete = QPushButton("Delete Note")
        self.btn_edit = QPushButton("Edit Note")
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)
        layout.addLayout(btn_layout)

        self.detail = QTextEdit()
        self.detail.setReadOnly(True)
        layout.addWidget(self.detail)

        self.setLayout(layout)

        self.list_widget.itemSelectionChanged.connect(self.on_select)
        self.btn_refresh.clicked.connect(self.refresh_notes_list)
        self.btn_delete.clicked.connect(self.delete_note)
        self.btn_edit.clicked.connect(self.edit_note)

    def refresh_notes_list(self):
        self.list_widget.clear()
        for n in self.note_repo.list():
            label = f"{n.id}: {n.text[:40]}"
            self.list_widget.addItem(label)

    def on_select(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        nid = item.text().split(':', 1)[0]
        note = self.note_repo.get(nid)
        if not note:
            return
        details = f"ID: {note.id}\nDataset: {note.dataset_id}\nX: {note.x}\nCreated: {note.created_at}\n\n{note.text}"
        self.detail.setPlainText(details)

    def delete_note(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        nid = item.text().split(':', 1)[0]
        self.note_repo.remove_note(nid)
        self.refresh_notes_list()

    def edit_note(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        nid = item.text().split(':', 1)[0]
        note = self.note_repo.get(nid)
        if not note:
            return
        from PySide6.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(self, 'Edit Note', 'Note text:', text=note.text)
        if not ok:
            return
        note.text = text
        self.note_repo.update_note(note)
        self.refresh_notes_list()

    
        