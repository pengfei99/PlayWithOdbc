import pyodbc


class OdbcConnector:
    def __init__(self, connectionConfig: str):
        self.config = connectionConfig
        self.connection = pyodbc.connect(DSN=connectionConfig)
        self.cursor = self.connection.cursor()

    def executeQuery(self, query: str):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        for row in results:
            print(row)


def main():
    # Set up the connection parameters
    dsn = 'mysqlitedb;'
    odbcConn = OdbcConnector(dsn)
    query = """SELECT
                c.country_name,
                c.country_id,
                l.country_id,
                l.street_address,
                l.city
                FROM
                    countries c
                LEFT JOIN locations l ON l.country_id = c.country_id
                WHERE
                c.country_id IN ('US', 'UK', 'CN')"""
    odbcConn.executeQuery(query)


if __name__ == "__main__":
    main()
