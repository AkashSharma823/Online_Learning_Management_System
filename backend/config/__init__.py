# MySQL is provided through the mysqlclient package (MySQLdb).
# No PyMySQL compatibility shim is required.
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    # mysqlclient can still be used when PyMySQL is not installed.
    pass
