import psycopg2 as ps
import psycopg2.extras
import sys

DB_HOST = 'ec2-54-170-163-224.eu-west-1.compute.amazonaws.com'
DB_NAME = 'df043ppajn3au9'
DB_USER = 'lfcjpjxpmcfqxi'
DB_PASS = '70ec9d90f402e4102fb1ea1d8699a2a0c232034016d6edacd6d681093a20772b'
conn = ps.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# cur.execute('UPDATE users SET admin = %s WHERE login = %s', (False, 'sanekakf'))
# conn.commit()


def clear():
    cur.execute("DELETE FROM users")
    conn.commit()
    print("Готово\n")


def delete():
    cur.execute("DROP TABLE users")
    conn.commit()
    print("Готово\n")


def create():
    cur.execute('CREATE TABLE IF NOT EXISTS users (login TEXT PRIMARY KEY, password TEXT, admin boolean)')
    conn.commit()
    print("Готово\n")


def print_users():
    # cur.execute('SELECT * FROM users')
    # for user in cur.fetchall():
    # print(cur.fetchall())
    count = 0
    while True:
        try:
            cur.execute('SELECT * FROM users')
            print(cur.fetchall()[count])
            count += 1
        except Exception as e:
            break
    print('Готово\n')


def thinking():

    choise = input('[D]elete | [C]lear | [S]ozdat | [P]rint | [E]xit: ').upper()

    if choise[0] == 'D':
        delete()
        thinking()

    elif choise[0] == 'C':
        clear()
        thinking()

    elif choise[0] == 'S':
        create()
        thinking()

    elif choise[0] == 'P':
        print_users()
        thinking()

    elif choise[0] == 'E':
        print("Выходим...")
        sys.exit()

    else:
        print("Выбран не тот режим \n")
        thinking()


if __name__ == '__main__':
    thinking()
