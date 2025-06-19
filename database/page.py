from typing import List, Any
from typing import TypeAlias
RowType: TypeAlias = list[dict[str, Any]] 

class Pageable:
    def __init__(self, page: int = 1, size: int = 10):
        self.page = page
        self.size = size
    
    def get_offset(self):
        return (self.page - 1) * self.size
    
    def get_limit(self):
        return self.size

    def limit_sql(self):
        return f"limit {self.get_limit()} offset {self.get_offset()}"

class PageResult:
    def __init__(self, data: RowType, total: int, pageable: Pageable):
        self.data = data
        self.total = total
        self.pageable = pageable

    
