import pyodbc


def pyTypeToSqlType(pythonType):
    defaultType = 'VARCHAR(255)'
    typeMapping = {
        int: 'INT',
        float: 'FLOAT',
        str: 'VARCHAR(255)',
        bytes: 'BLOB',
        bool: 'BOOLEAN',
        # Add more mappings as needed
    }

    return typeMapping.get(pythonType, defaultType)


class OdbcConnector:
    def __init__(self, connectionConfig: str):
        self.config = connectionConfig
        self.connection = pyodbc.connect(DSN=connectionConfig)
        self.cursor = self.connection.cursor()

    def executeQuery(self, query: str):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        if results:
            for row in results:
                print(row)
        else:
            print("No result")

    def getTableSchema(self, tableName: str):
        """
        This function takes a tableName, and returns the schema of the table in a dictionary. The key is the column name
         and the value is the column type (in python data type). The table Name can be a parquet file path
        beware the file path extension must be .parquet and '' must be part of the path value. For example
        '/tmp/test.parquet' is a valid path. /tmp/test.parquet is not valid.
        The
        :param tableName:
        :type tableName:
        :return:
        :rtype:
        """
        query = f"SELECT * FROM {tableName} LIMIT 0;"
        self.cursor.execute(query)
        columnNames = [column[0] for column in self.cursor.description]
        columnTypes = [column[1] for column in self.cursor.description]
        columns = {}
        for colName, colType in zip(columnNames, columnTypes):
            columns[colName] = colType
        return columns

    def getTableSchemaInSQL(self, tableName: str):
        """
        This function takes a tableName, and returns the schema of the table. The table Name can be a parquet file path
        beware the file path extension must be .parquet and '' must be part of the path value. For example
        '/tmp/test.parquet' is a valid path. /tmp/test.parquet is not valid.
        :param tableName:
        :type tableName:
        :return:
        :rtype:
        """
        columns = self.getTableSchema(tableName)
        columnSchema = ""
        for colName, colType in columns.items():
            columnSchema = columnSchema + f"{colName} {pyTypeToSqlType(colType)},"
        print(columnSchema)

    def loadParquetFileToTable(self, parquetFilePath: str, targetTableName):
        query = f"CREATE TABLE {targetTableName} AS SELECT * FROM '{parquetFilePath}'"
        result = self.cursor.execute(query)
        print(result)
        self.cursor.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


def connectSqlite():
    """
    This function calls a dsn mysqlitedb which uses a sqlite instance. It has two tables countries, and locations
    :return:
    :rtype:
    """
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
    odbcConn.close()


def connectInMemoryDuckDb():
    """
    This function calls a dsn duckdb which uses a memory based duckdb instance. We can read a parquet file
    directly. Or create a table by loading the parquet file.
    :return:
    :rtype:
    """
    dsn = "duckdb;"
    server = OdbcConnector(dsn)
    # test 1: read parquet
    # query1 = """select * from '/home/pengfei/data_set/sf_fire/sf_fire_snappy.parquet' limit 10;
    #         """
    # server.executeQuery(query1)

    # test 2: generate schema
    # server.getTableSchemaInSQL(r"'/home/pengfei/data_set/sf_fire/sf_fire_snappy.parquet'")

    # test 3: load parquet to table
    server.loadParquetFileToTable('/home/pengfei/data_set/sf_fire/sf_fire_snappy.parquet', "sf_fire")
    query2 = "select * from sf_fire limit 10;"
    server.executeQuery(query2)
    server.close()


def connectFileBasedDuckDb():
    """This function calls a dsn fduckdb which uses a file based duckdb instance. A table called sf_fire is
    already loaded in this database. so we can query it directly"""
    dsn = "fduckdb;"
    server = OdbcConnector(dsn)
    # test 1: read table sf_fire

    # query1 = "select * from sf_fire limit 10;"
    # server.executeQuery(query1)

    # test 2: count total row
    query2 = "select count(*) as total_row from sf_fire;"
    server.executeQuery(query2)
    server.close()


def main():
    # connectSqlite()
    connectFileBasedDuckDb()


if __name__ == "__main__":
    main()
