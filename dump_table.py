#!/usr/bin/env python
import rethinkdb as r
import json
import os
import sys
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

db_name = "mm_2015_scores"
table_name = "scoreboard"
my_port = 28015

def del_entries(conn):
    result = r.table(table_name).run(conn)
    for entry in result:
        r.table(table_name).get(entry['id']).delete().run(conn);

if __name__=="__main__":
    conn = r.connect(host="localhost", port=my_port, db=db_name)
    try:
        results = del_entries(conn)
    except RqlRuntimeError:
        print("Some error detected")
