import psycopg2 as ps
import psycopg2.extras

DB_HOST = 'ec2-54-170-163-224.eu-west-1.compute.amazonaws.com'
DB_NAME = 'df043ppajn3au9'
DB_USER = 'lfcjpjxpmcfqxi'
DB_PASS = '70ec9d90f402e4102fb1ea1d8699a2a0c232034016d6edacd6d681093a20772b'
conn = ps.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


def clear():
    cur.execute("DELETE FROM users")
    conn.commit()


def delete():
    cur.execute("DROP TABLE users")
    conn.commit()


def create():
    cur.execute('CREATE TABLE IF NOT EXISTS users (login TEXT PRIMARY KEY, password TEXT, admin boolean)')
    conn.commit()


choise = input('[D]elete | [C]lear | [S]ozdat: ').upper()

if choise[0] == 'D':
    delete()
elif choise[0] == 'C':
    clear()
elif choise[0] == 'S':
    create()
