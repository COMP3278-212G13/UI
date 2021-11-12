from PyQt5.QtWidgets import QCalendarWidget, QDialog, QDialogButtonBox, QFormLayout


class selectdate(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.NoVerticalHeader
        self.calendar.setNavigationBarVisible(True)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        
        layout = QFormLayout(self)
        layout.addWidget(self.calendar)
        layout.addWidget(buttonBox)
        
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
    
    def getInputs(self):
        return (self.calendar.selectedDate())
