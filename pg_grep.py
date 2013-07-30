#!/usr/bin/env python
# pg_grep.py
# A tool for searching PostgreSQL Databases
# for values if table and column name are unknown

import sys
import psycopg2
import optparse
import re
import time

#
# getDatabaseConnection
#
# In:  username, password
# Out: Active database connection to requested database

def getDatabaseConnection(username, password):
    try:
        cxstring = "host='localhost' dbname='development' user='"+username+"' password='"+password+"'"

        result = psycopg2.connect(cxstring)

        return result
    except Exception, e:
        print "Program encountered an exception: %s" % e
        # relace with actual error message
        exit

###################

def getRows(username, password, datatype, searchvalue):
    cur = getDatabaseConnection(username, password).cursor()

    getTablesAndColumnsStatement = "SELECT table_name, column_name FROM "
    getTablesAndColumnsStatement += "information_schema.columns WHERE table_name IN "
    getTablesAndColumnsStatement += "(SELECT tablename FROM pg_tables WHERE schemaname = 'public') "
    getTablesAndColumnsStatement += "AND data_type='"+datatype+"'"
    
    try:
        cur.execute(getTablesAndColumnsStatement)
        getTablesAndColumnsRows = cur.fetchall()

        for getTablesAndColumnsRow in getTablesAndColumnsRows:
            table_name = getTablesAndColumnsRow[0]
            column_name = getTablesAndColumnsRow[1]

# Need to define all possibilities for all data_types
            if datatype == "integer" or datatype == "double precision":
                getValuesStatement = "SELECT "+column_name+" FROM "+table_name+" WHERE "+column_name+" = "+str(searchvalue)
            else:
                getValuesStatement = "SELECT "+column_name+" FROM "+table_name+" WHERE "+column_name+" LIKE '%"+searchvalue+"%'"
            
            try:
                cur = getDatabaseConnection(username, password).cursor()
                cur.execute(getValuesStatement)
                getValuesRows = cur.fetchall()

                for getValuesRow in getValuesRows:
                    value = getValuesRow[0]
                    print table_name+"."+column_name+": "+ str(value)
                    cur.close()
            except Exception, e:
                print "Program encountered an exception: %s" % e
    except Exception, e:
        print "Program encountered an exception: %s" % e
        
        sys.exit(0)
    
###################
        
def exitOnUsage():
    print """
Usage:
Standard usage: pg_grep.py -U username -t 'data_type' -s 'value to search for'

Options:
    -h, --help                              Show this help message and exit
    -U USERNAME, --user=USERNAME            Specify database username
    -p PASSWORD, --password=PASSWORD        Specifiy database password
    -t DATATYPE, --type=DATATYPE            Specify column data_type. Supports PostgreSQL native data types.
    -s SEARCHVALUE, --search=SEARCHVALUE    Specify what to search for
    
NOTE: Does not currently support PostGIS data types.

"""
  
    sys.exit(0)
    
###################
        
def exitOnUnsupportedDataType(datatype):
    print """
The datatype """ + datatype + """ is currently not supported.
"""

    sys.exit(0)
    
###################
    
def main():
        
    parser = optparse.OptionParser("\n Standard usage: %prog -U username -t 'data_type' -s 'value to search for' \n Brute Force Example: %prog -U username -b -s 'value to search for'")
    parser.add_option("-U", "--user", dest="username", type="string", help="Specify database user name")
    parser.add_option("-p", "--password", dest="password", type="string", help="Specify database password")
    parser.add_option("-t", "--type", dest="datatype", type="string", help="Specify column data_type. Supports PostgreSQL native data types.")    
    parser.add_option("-s", "--search", dest="searchvalue", type="string", help="Specify what to search for")
    # include a -i command
    #parser.add_option("-i", "--ignore-case", dest="ignorecase", action="count", help="Used to search case insensitively. When used with numeric data types, this will have no effect.")

    (options, arguments) = parser.parse_args()
    username = options.username
    datatype = options.datatype
    searchvalue = options.searchvalue
    password = options.password

    # Create unsupported datatypes list, maybe make it a method?
    unsupported_datatypes_list = ["bytea"]
    

    
    if len(sys.argv[1:]) == 0:
        exitOnUsage()
    else:
        startTime = time.time()
        if datatype in unsupported_datatypes_list:
            exitOnUnsupportedDataType(datatype)
        else:
            getRows(username, password, datatype, searchvalue)

        endTime = time.time()
        # DEBUG Line. Used to calculate time. Use for optimization.
        print "Time to execute: ", (endTime - startTime), " seconds"
##        if options.brute == 1:
##            getRowsBrute(username, searchvalue)
##        else:
##            getRows(username, datatype, searchvalue)
                         
           
    
##    exitOnUsage()
##    #getRows("josh", "integer", "1")

#
# Redirect to main
#
if __name__ == "__main__":
    main()


