

class CustomerWhereCause:
    name: str
    address: str
    phone: str

    def __init__(self,name:str="",address:str="",phone:str=""):
        self.name=name
        self.address=address
        self.phone=phone

    def to_sql(self):
        sql = " WHERE 1=1 "
        if self.name:
            sql += f" AND name like '%{self.name}%' "
        if self.address:
            sql += f" AND address like '%{self.address}%' "
        if self.phone:
            sql += f" AND phone like '%{self.phone}%' "
        return sql
    