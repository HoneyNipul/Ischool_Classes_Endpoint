import pyodbc

ISCHOOL_OLDDB_SERVER = "ist-s-sql2.ad.syr.edu"
ISCHOOL_OLDDB_USER = 'web-class-api-ro'
ISCHOOL_OLDDB_PASSWD = 'sho11NxqCZf7gGRi3acv'
ISCHOOL_OLDDB_DATABASE = "iSchoolDb"
ISCHOOL_OLDDB_DB_DRIVER = 'ODBC Driver 17 for SQL Server'


class iSchoolDBData():

    def __init__(self):
        self.conn = pyodbc.connect('DRIVER={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % 
            (ISCHOOL_OLDDB_DB_DRIVER, ISCHOOL_OLDDB_SERVER, ISCHOOL_OLDDB_DATABASE, ISCHOOL_OLDDB_USER, ISCHOOL_OLDDB_PASSWD))


    def get_waitlist_by_term(self, termId, profnetid):
        rows = []
        with self.conn.cursor() as cursor:
            cursor.execute("""SELECT [WaitLists].[Id]
            ,[WaitLists].[classId]
            ,[WaitLists].[userId]
            ,[addDatetime]
            ,[listStatus]
            ,[termId]
            ,[notes]
            ,[lastUpdate]
            ,[lastUpdateUserId]
            ,[lastUpdateSubject]
            ,[lastUpdateMessage]
            ,[provUsers].[netId]
            ,[provUsers].[email]
            ,[provUsers].[lastName]
            ,[provUsers].[firstName]
            ,profdata.netId as profNetId
        FROM [iSchoolDb].[dbo].[WaitLists]
            JOIN [iSchoolDb].[dbo].[provUsers] ON userId = provUsers.id
            JOIN (SELECT [provUsers].netId, [provClassInstructors].classId FROM [iSchoolDb].[dbo].[provUsers] 
                JOIN [iSchoolDb].[dbo].[provClassInstructors] ON [provClassInstructors].userId = [provUsers].id) as profdata
                ON profdata.classId = [WaitLists].classId 
        WHERE [WaitLists].termId = ? AND profdata.netId = ?;""", termId, profnetid)
            rows = cursor.fetchall()
        return rows

