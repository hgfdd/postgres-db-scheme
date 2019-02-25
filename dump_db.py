import psycopg2
import sys

fullData={}

fullData["indexes"]=[]
fullData["sequences"]=[]
fullData["tables"]=[]
fullData["functions"]=[]
fullData["version"]=[]

def fillData(type, records):
    global fullData
    print("Fill data for type = ", type)
    for record in records:
        fullData[type].append(record[0])


def fetchData(sql, cursor, type):
    cursor.execute(sql)
    records = cursor.fetchall()
    fillData(type, records)


def dumpToFile(path = ""):
    global fullData

    f=''
    try:
        f = open(path, 'w')
    except:
        print('ERROR: cannot open file %s' % (path))
        sys.exit(1)

    for type in fullData:
        for data in fullData[type]:
            f.write(type + ";" + data + "\n")


if __name__ == "__main__":
    print("Creating dump for database...")

    host = "127.0.0.1"
    port = 5432
    dump_file = 'dump.csv'
    db_name = "test_db"
    db_user = "postgres"
    db_password = ""

    paramInd=1

    while paramInd < len(sys.argv):

        if sys.argv[paramInd] == "--host" and len(sys.argv) > (paramInd + 1):
            host = sys.argv[paramInd + 1]
            paramInd = paramInd + 1
        if sys.argv[paramInd] == "--port" and len(sys.argv) > (paramInd + 1):
            port = sys.argv[paramInd + 1]
            paramInd = paramInd + 1
        if sys.argv[paramInd] == "--dump_file" and len(sys.argv) > (paramInd + 1):
            dump_file = sys.argv[paramInd + 1]
            paramInd = paramInd + 1
        if sys.argv[paramInd] == "--db_name" and len(sys.argv) > (paramInd + 1):
            db_name = sys.argv[paramInd + 1]
            paramInd = paramInd + 1
        if sys.argv[paramInd] == "--db_user" and len(sys.argv) > (paramInd + 1):
            db_user = sys.argv[paramInd + 1]
            paramInd = paramInd + 1
        if sys.argv[paramInd] == "--db_password" and len(sys.argv) > (paramInd + 1):
            db_password = sys.argv[paramInd + 1]
            paramInd = paramInd + 1

        if sys.argv[paramInd] == "--help":
            print("Usage: --db_name <db_name> --db_user <db_user> --db_password <db_password> --host <db server hostname> --port <db server port> --dump_file <file>")
            sys.exit()

        paramInd = paramInd + 1

    try:
        conn = psycopg2.connect(host=host, database=db_name, user=db_user, password=db_password)
    except:
        print("Cannot connect to database %s" % (host))
        sys.exit(1)

    print("Connecting to database OK")

    cursor = conn.cursor()

    # fetch tables
    sql = """ select distinct table_name 
            from information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE' 
            ORDER BY table_name DESC """

    fetchData(sql, cursor, 'tables')

    # fetch fuctions
    sql = """ SELECT distinct routine_name
            FROM information_schema.routines 
            WHERE routine_type='FUNCTION' AND specific_schema='public' 
            ORDER BY routine_name DESC """

    fetchData(sql, cursor, 'functions')

    sql = """ select distinct indexname
            from pg_indexes 
            where schemaname = 'public' 
            ORDER BY indexname DESC """

    fetchData(sql, cursor, 'indexes')

    sql = """ SELECT distinct sequence_name
            FROM information_schema.sequences 
            ORDER BY sequence_name DESC """

    fetchData(sql, cursor, 'sequences')

    dumpToFile(dump_file)

    print("Creating dump file for database DONE")
    sys.exit(0)
