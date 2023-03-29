import gspread
from core.base import Base

class SpreadSheetClient(Base):
    def __init__(self, key_file_path):
        self._gs = gspread.service_account(key_file_path)
        self._wb = None
        
    def open_workbook_by_url(self, url):
        self._wb = self._gs.open_by_url(url)
        return self._wb
    
    def open_workbook_by_name(self, name):
        self._wb = self._gs.open(name)
        return self._wb    
    
    @property
    def wb(self):
        return self._wb 

    