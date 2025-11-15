import oracledb
import sys
import os
from glob import glob
from contextlib import contextmanager

DB_HOST = "localhost"
DB_PORT = 1521
DB_SERVICE = "FREE"
DB_USER = "sys"
DB_PASS = "helloworld"


@contextmanager
def get_connection():
    connection = None
    dsn = f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}"
    print(f"Connecting to {dsn}...")
    connection = oracledb.connect(
        user=DB_USER, password=DB_PASS, dsn=dsn, mode=oracledb.SYSDBA
    )
    print("Connection successful.")
    yield connection
    if connection:
        connection.close()
        print("Connection closed.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <student-folder>")
        sys.exit(1)

    student_dir = sys.argv[1]
    sql_files = glob(f"{os.path.join('submissions', student_dir, '*.sql')}")
    sql = ""
    if len(sql_files) > 1:
        # combine all files into one mega SQL
        for sql_file in sorted(sql_files):
            with open(sql_file) as f:
                sql += f.read()
    else:
        with open(sql_files[0]) as f:
            sql += f.read()

    try:
        with get_connection() as connection:
            print("Connection retrieved. Running script(s)...")
            with connection.cursor() as cursor:
                cursor.callproc("dbms_output.enable")

                statements = sql.split(";")

                for statement in statements:
                    statement = statement.strip()
                    if not statement:  #  trailing ;
                        break
                    if not statement.endswith(";"):
                        statement = f"{statement};"
                    print(f"Running statement {statement}")
                    cursor.execute(statement)
                    if "select" not in statement.lower():
                        continue

                    rows = cursor.fetchall()
                    if rows:
                        # Print column headers
                        columns = [desc[0] for desc in cursor.description]
                        print(f"\n{' | '.join(columns)}")
                        print(
                            "-"
                            * (
                                sum(len(col) for col in columns)
                                + 3 * (len(columns) - 1)
                            )
                        )

                        # Print rows
                        for row in rows:
                            print(" | ".join(str(val) for val in row))
                        print(f"\n({len(rows)} row(s) returned)")
                    else:
                        print("(No rows returned)")

                    # Fetch and print any DBMS_OUTPUT lines
                    print(f"--- DBMS_OUTPUT (from {student_dir}) ---")
                    lines_var = cursor.arrayvar(oracledb.STRING, 100)
                    num_lines_var = cursor.var(int)
                    chunk_size = 100
                    output_found = False
                    while True:
                        num_lines_var.setvalue(0, chunk_size)
                        cursor.callproc(
                            "dbms_output.get_lines", (lines_var, num_lines_var)
                        )
                        num_lines = num_lines_var.getvalue()
                        lines = lines_var.getvalue()
                        if num_lines == 0:
                            break
                        output_found = True
                        for i in range(num_lines):
                            print(lines[i])
                        if num_lines < chunk_size:
                            break
                    if not output_found:
                        print("(No DBMS_OUTPUT)")
                    print("---------------------------------")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Execution stopped.")
        sys.exit(1)
