import pyodbc

class OrmManager(object):
    def __get__(self, instance, owner):
        self.owner = owner
        
        settings = __import__("settings")
        
        self.connection = pyodbc.connect(
            driver=settings.DB_DRIVER,
            database=settings.DB_NAME,
            server=settings.DB_SERVER,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
        )
        return self

    def create(self, **kwargs):
        cursor = self.connection.cursor()
        
        sql = f"""
        INSERT INTO {self.owner} ({', '.join(list(kwargs.keys()))}) VALUES ({', '.join(['?']*len(kwargs))})
        """
        
        
        cursor.execute(sql, list(kwargs.values()))
        cursor.commit()
        return self.owner(**kwargs)
    
    def all(self):
        cursor = self.connection.cursor()
        sql = f"SELECT * FROM {self.owner.__name__}"
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        rows = [self.owner(**dict(zip(columns, row))) for row in cursor.fetchall()] #cursor.fetchall()
        return rows
    
    
    def where_clause_generate(self, **kwargs):
        where_clause = 'WHERE ' + ' AND '.join([k +' = ' + str(v) for k, v in kwargs.items()])
        return where_clause
    
    
    def filter(self, **kwargs):
        cursor = self.connection.cursor()
        sql = f"""
        SELECT * FROM {self.owner.__name__} {self.where_clause_generate(**kwargs)}"""
        cursor.execute(sql)
        columns = [column[0] for column in cursor.description]
        rows = [self.owner(**dict(zip(columns, row))) for row in cursor.fetchall()] #cursor.fetchall()
        return rows
    
    def update(self, where_clause: str, **kwargs):
        print(kwargs)
        cursor = self.connection.cursor()
        if where_clause:
            sql = f"""
            UPDATE {self.owner.__name__} SET {', '.join([k +' = ?' for k in kwargs.keys()])} {where_clause}"""
        else:
            sql = f"""
            UPDATE {self.owner.__name__} SET {', '.join([k +' = ?' for k in kwargs.keys()])}"""
        cursor.execute(sql, list(kwargs.values()))
        cursor.commit()
        return self.owner(**kwargs)