import json
from seCore.JDBC import jdbcLoaded, jdbcDriver, jdbcEngine
from seCore.ODBC import odbcLoaded, odbcDriver, odbcEngine
from seCore.CustomLogging import logger


class connect:
    def __init__(self, server: str, port: int, user: str, password: str, trust: str, db: str = "", trustServerCertificate: bool = True, driverOverride: str = "", enableLogging: bool = True):
        self.__isConnected = False
        self.__enableLogging = enableLogging
        self.__odbcLoaded = odbcLoaded()
        self.__odbcDriver = odbcDriver()
        self.__jdbcLoaded = jdbcLoaded()
        self.__jdbcDriver = jdbcDriver()
        self.__driverOverride = driverOverride.lower() if driverOverride.lower() in ["odbc", "jdbc"] else "odbc"

        self.__connStr = {
            # "driver": self.__driver,
            "server": server,
            "port": port,
            "database": db,
            "user": user,
            "password": password,
            "trust": trust,
            "trustServerCertificate": trustServerCertificate
        }

        if self.__driverOverride == "odbc" and self.__odbcLoaded:
            self.__driverOverride = "odbc"
        elif self.__driverOverride == "jdbc" and self.__jdbcLoaded:
            self.__driverOverride = "jdbc"
        else:
            self.__driverOverride = "jdbc"

        match self.__driverOverride:
            case "odbc":
                self.__cnxn = odbcEngine(
                    server=self.__connStr['server'],
                    port=self.__connStr['port'],
                    db=self.__connStr['database'],
                    user=self.__connStr['user'],
                    password=self.__connStr['password'],
                    trust=self.__connStr['trust']
                )
                self.logging()

                try:
                    self.__cnxn.connect()
                    self.__isConnected = self.__cnxn.isConnected
                except Exception as e:
                    logger.error(e)

            case _:
                self.__cnxn = jdbcEngine(
                    server=self.__connStr['server'],
                    port=self.__connStr['port'],
                    user=self.__connStr['user'],
                    password=self.__connStr['password'],
                    trustServerCertificate=self.__connStr['trustServerCertificate']
                )
                self.logging()

                try:
                    self.__cnxn.connect()
                    self.__isConnected = self.__cnxn.isConnected

                except Exception as e:
                    logger.error(e)

    def query(self, query: str):
        try:
            return self.__cnxn.query(query)
        except Exception as e:
            raise SQLQueryException(f'{e}')

    def logging(self):
        if self.__enableLogging:
            oSqlDriver = {
                "driver-info":
                    {
                        "using": self.__driverOverride,
                        "odbc": {
                            "loaded": self.__odbcLoaded,
                            "driver": self.__odbcDriver
                        },
                        "jdbc": {
                            "loaded": self.__jdbcLoaded,
                            "driver": self.__jdbcDriver
                        }
                    }
            }
            logger.info(f'{json.dumps(oSqlDriver)}')

    @property
    def isConnected(self) -> bool:
        return self.__isConnected


class SQLQueryException(Exception):
    """Exception raised for anything caught by an SQL query."""
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return str(self.message)
