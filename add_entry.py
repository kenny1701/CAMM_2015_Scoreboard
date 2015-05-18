#!/usr/bin/env python
import rethinkdb as r
import json
import os
import sys
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

db_name = "mm_2015_scores"
table_name = "scoreboard"
my_port = 28015

team_name = ""
school = ""
time = ""
completed = ""
cell_count = ""

def to_ms(tm):
    temp = tm.split(":")
    return int(temp[0])*60000 + int(temp[1])*1000 + int(temp[2])

def is_replacable(old_tm, new_tm, old_flag, new_flag, old_cc, new_cc):
    temp1 = old_tm.split(":")
    temp2 = new_tm.split(":")
    old_ms = to_ms(old_tm)
    new_ms = to_ms(new_tm)
    print(str(old_ms) + "   " + str(new_ms))
    if int(old_flag) is int(new_flag):
        print("DEBUG: same flag")
        if int(new_flag) is 1:
            return int(new_ms) < int(old_ms)
        else:
            return int(old_cc) < int(new_cc)
    else:
        print("DEBUG: different flag")
        if int(new_flag) is 1:
            return True
        else:
            return False


def ins_entry(conn, tn, sch, tm, flag, cc):
    result = get_entry(conn, tn)
    if result is None:
        r.table(table_name).insert([
            {
                "team_name": tn,
                "school": sch,
                "time": tm,
                "time_ms": to_ms(tm),
                "completed": flag,
                "cell_count": cc
            }
        ]).run(conn)
        print("inserted")
    else:
        if is_replacable(result['time'], tm, result['completed'], flag, result['cell_count'], cc):
            r.table(table_name).get(result['id']).delete().run(conn)
            r.table(table_name).insert([
                {
                    "team_name": tn,
                    "school": sch,
                    "time": tm,
                    "time_ms": to_ms(tm),
                    "completed": flag,
                    "cell_count": cc
                }
                ]).run(conn)
            print("updated")
        else:
            print("not changed")

def get_entry(conn, tn):
    result = r.table(table_name).run(conn)
    for entry in result:
        if entry["team_name"] == tn:
            return entry
    return None

if __name__=="__main__":
    conn = r.connect(host="localhost", port=my_port, db=db_name)
    try:
        # Parse argument
        if (len(sys.argv) is not 6):
            print("Insufficient arguments")
            print("Usage: ./add_entry <team_name> <school> <time> <completed flag> <cell_count>")
            sys.exit(0)
        team_name = sys.argv[1]
        school = sys.argv[2]
        time = sys.argv[3]
        completed = sys.argv[4]
        cell_count = sys.argv[5]
        # Insert new score
        ins_entry(conn, team_name, school, time, completed, cell_count)
    except RqlRuntimeError:
        print("Some error detected")
