from shotglass2.takeabeltof.database import SqliteTable


class Location(SqliteTable):
    """Event Location Table"""
    def __init__(self,db_connection):
        super().__init__(db_connection)
        self.table_name = 'location'
        self.order_by_col = 'lower(location_name), id'
        self.defaults = {}
        
    def create_table(self):
        """Define and create the table"""
        
        sql = """
        location_name TEXT NOT NULL,
        street_address TEXT,
        city  TEXT,
        state  TEXT,
        zip TEXT,
        lat  NUMBER,
        lng  NUMBER
        """
                
        super().create_table(sql)

        
class Event(SqliteTable):
    """Events where reservations are needed"""
    def __init__(self,db_connection):
        super().__init__(db_connection)
        self.table_name = 'event'
        self.order_by_col = 'start'
        self.defaults = {
            'max_reservations':10,
            'reservations_per_appointment':0,
            'location_id':None,
        }
        
    def create_table(self):
        """Define and create a table"""
        
        sql = """
            title TEXT,
            start DATETIME,
            end DATETIME,
            max_reservations INTEGER DEFAULT 10,
            reservations_per_appointment INTEGER DEFAULT 0, -- 0 means max for period
            contact_email TEXT,
            contact_phone TEXT,
            reservation_open DATETIME,
            reservation_close DATETIME,
            location_id INTEGER
            """
        super().create_table(sql)
        
        
    @property
    def _column_list(self):
        """A list of dicts used to add fields to an existing table.
        """
    
        # {'name':'expires','definition':'DATETIME',},
        column_list = [
        ]
    
        return column_list


class Period(SqliteTable):
    """Divide event into time based chunks"""
    def __init__(self,db_connection):
        super().__init__(db_connection)
        self.table_name = 'period'
        self.order_by_col = 'start'
        self.defaults = {'max_reservations':4,}

    def create_table(self):
        """Define and create a table"""

        sql = """
            start DATETIME,
            max_reservations INTEGER DEFAULT 4,
            event_id INTEGER,
            FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE
            """
        super().create_table(sql)


    @property
    def _column_list(self):
        """A list of dicts used to add fields to an existing table.
        """

        # {'name':'expires','definition':'DATETIME',},
        column_list = [
        ]

        return column_list

class Appointment(SqliteTable):
    """People showing up with their bikes to be fixed"""
    def __init__(self,db_connection):
        super().__init__(db_connection)
        self.table_name = 'appointment'
        self.order_by_col = 'id'
        self.defaults = {'count':0,}

    def create_table(self):
        """Define and create a table"""

        sql = """
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT,
            expires DATETIME,
            count INTEGER DEFAULT 0,
            period_id INTEGER,
            FOREIGN KEY (period_id) REFERENCES period(id) ON DELETE CASCADE
            """
        super().create_table(sql)


    @property
    def _column_list(self):
        """A list of dicts used to add fields to an existing table.
        """

        # {'name':'expires','definition':'DATETIME',},
        column_list = [
        ]

        return column_list

