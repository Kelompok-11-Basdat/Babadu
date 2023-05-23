from django.db import connection
import datetime
import uuid

@staticmethod
def execute(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, (str(val) if isinstance(val, uuid.UUID) 
                                else val.strftime("%Y-%m-%d") if isinstance(val, datetime.date) 
                                else val.strftime("%H:%M") if isinstance(val, datetime.time) 
                                else val for val in row)))
            for row in cursor.fetchall()
        ]
    return results