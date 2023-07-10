"""Application model."""

from PyQt6.QtCore import QAbstractTableModel, Qt
from pandas import DataFrame


class TableModel(QAbstractTableModel):
    """Model to convert LS data to be TableView compatible."""

    def __init__(self, data: DataFrame = None):
        """Initialize class."""
        super().__init__()
        self._data = data

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """Create data model."""
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        """Get the number of rows."""
        if self._data is None:
            return 0
        return self._data.shape[0]

    def columnCount(self, index):
        """Get the number of columns."""
        if self._data is None:
            return 0
        return self._data.shape[1]

    def headerData(self, section, orientation, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole):
        headerLabels = {
            "token": "Token",
            "attribute_3": "Codi del cicle",
            "attribute_4": "Id de cicle",
            "sent": "Invitació enviada",
            "completed": "Sol·licitud de matrícula completada",
            "email": "Email",
            "firstname": "Nom",
            "lastname": "Cognoms",
        }
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                colName = str(self._data.columns[section])
                return headerLabels[colName]
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

    def getColumnName(self, index):
        """Get column name based of an index."""
        return self._data.columns[index.column()]

    def getRowData(self, row: int):
        """Return a row form the dataframe."""
        return self._data.iloc[row]

    def update(self, new_data: DataFrame):
        """Update model."""
        self._data = new_data
