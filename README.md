pg_grep
=======

A python tool for searching PostgreSQL databases when structure is unknown

Use pg_grep when you are unsure of where specific information in your database is. 

Specific example:
When using JBoss and GateIn, user information is stored in jbid_io* tables. It is not apparently know which table houses specific information. Use this tool to search for an entry that will point you to where the information is. 

Another possible use-case is to find sensitive information. If you just want to look for all occurences of a certain word or phrase (or number such as a SSN), you can search for it and it will return all occurences of the searched value.
