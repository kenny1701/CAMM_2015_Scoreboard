#!/usr/bin/env python
import rethinkdb as r
import json
import os
import sys
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

db_name = "mm_2015_scores"
table_name = "scoreboard"
my_port = 28015

def get_entry(conn):
    result = r.table(table_name).run(conn)
    return result

if __name__=="__main__":
    conn = r.connect(host="localhost", port=my_port, db=db_name)
    try:
        # Insert new score
        results = get_entry(conn)
        for entry in results:
            print(entry)
    except RqlRuntimeError:
        print("Some error detected")
