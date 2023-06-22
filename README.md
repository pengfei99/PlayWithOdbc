# PlayWithOdbc
In this repo, we will play with odbc. First we will install some dbms and use odbc to connect them and provides
odbc DSN (Data source name) for the connected database. Then we will use different languages (e.g. python, java)
to read the odbc dsn and perform sql operations.

## What is odbc?

**ODBC stands for Open Database Connectivity**. It is an industry-standard application programming interface (API) that 
allows applications to interact with relational database management systems (RDBMS) using a common interface. `ODBC 
provides a consistent way for applications to communicate with various database systems, regardless of the specific 
database vendor or underlying operating system.`

The main purpose of ODBC is to enable applications to access and manipulate data in a database using SQL 
(Structured Query Language). It provides a set of functions and rules for establishing a connection to a database, 
executing SQL queries or commands, fetching query results, and managing transactions.

ODBC operates based on a **client-server model**, where the client application interacts with the database server 
through the ODBC driver. The driver acts as a mediator between the application and the database, translating the ODBC 
function calls into commands understood by the database system. Each database vendor typically provides its own 
ODBC driver, which needs to be installed and configured on the client machine.