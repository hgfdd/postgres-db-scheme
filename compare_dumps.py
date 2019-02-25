import sys
import datetime

etalon_dump_data={ }
working_dump_data={ }

def parse_dump_file(file):
    data={ }

    f=''
    try:
        f = open(file, 'r')
    except:
        print('ERROR: cannot open file %s' % (file))
        sys.exit(1)

    lines = f.readlines()

    for line in lines:
        line=line.strip()
        parts=line.split(";")

        if len(parts) >= 2:
            type=parts[0]
            name=parts[1]

            if type not in data:
                data[type]=[name]
            else:
                data[type].append(name)
        else:
            print("ERROR: invalid file %s" % (file))
            sys.exit(1)

    return data

def compare_dumps(etalon_dump, working_dump):
    error_data={ }
    for type in etalon_dump:
        for data in etalon_dump[type]:
            if type not in working_dump or data not in working_dump[type]:
                if type not in error_data:
                    error_data[type]=[data]
                else:
                    error_data[type].append(data)

    return error_data

def clean_log(log_file):
    if log_file != '':
        f=''
        try:
            f = open(log_file, 'w')
        except:
            print('ERROR: cannot open log file %s' % (log_file))
            sys.exit(1)

def write_to_log(log_file, message):
    if log_file != '':
        f = ''
        try:
            f = open(log_file, 'a')
        except:
            print('ERROR: cannot open log file %s' % (log_file))
            sys.exit(1)

        f.write(message)
        f.write("\n")
    else:
        print(message)


if __name__ == "__main__":
    etalon_dump=''
    working_dump=''
    log_file=''

    paramInd = 1
    while paramInd < len(sys.argv):

        if sys.argv[paramInd] == "--etalon_dump_file" and len(sys.argv) > (paramInd + 1):
            etalon_dump = sys.argv[paramInd + 1]
            paramInd = paramInd + 1
        if sys.argv[paramInd] == "--working_dump_file" and len(sys.argv) > (paramInd + 1):
            working_dump = sys.argv[paramInd + 1]
            paramInd = paramInd + 1
        if sys.argv[paramInd] == "--log_file" and len(sys.argv) > (paramInd + 1):
            log_file = sys.argv[paramInd + 1]
            paramInd = paramInd + 1

        if sys.argv[paramInd] == "--help":
            # print("Usage: --etalon_dump_file <etalon_dump_file> --working_dump_file <working_dump_file>")
            write_to_log(log_file, "Usage: --etalon_dump_file <etalon_dump_file> --working_dump_file <working_dump_file> --log_file <log_file>")
            sys.exit(1)

        paramInd = paramInd + 1

    if log_file != '':
        clean_log(log_file)

    write_to_log(log_file, str(datetime.datetime.now()))
    write_to_log(log_file, "Start dump compare...")

    if etalon_dump == '' or working_dump == '':
        # print("ERROR: dump files is empty")
        write_to_log(log_file, "ERROR: dump files is empty")
        sys.exit(1)

    etalon_data = parse_dump_file(etalon_dump)
    working_data = parse_dump_file(working_dump)

    error_data = compare_dumps(etalon_data, working_data)
    extra_data = compare_dumps(working_data, etalon_data)

    if not error_data and not extra_data:
        write_to_log(log_file, "OK: dumps are equal")

    else:
        write_to_log(log_file, "Dumps are different!")
        write_to_log(log_file, "==== In the etalon base, not in working:")
        for type in error_data:
            for data in error_data[type]:
                write_to_log(log_file, type + ' ' + data)
        write_to_log(log_file, "==== In the working base, not in etalon:")
        for type in extra_data:
                for data in extra_data[type]:
                    write_to_log(log_file, type + ' ' + data)

    sys.exit(0)