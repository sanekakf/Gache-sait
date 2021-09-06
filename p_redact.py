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
    cur.execute("DELETE FROM production")
    conn.commit()
    print("Готово\n")


def delete():
    try:
        cur.execute("DROP TABLE production")
        conn.commit()
        print("Готово\n")
    except Exception as e:
        print(e)
        print('\nОшибка')


def print_users():
    # cur.execute('SELECT * FROM users')
    # for user in cur.fetchall():
    # print(cur.fetchall())
    count = 0
    while True:
        try:
            cur.execute('SELECT * FROM production')
            print(cur.fetchall()[count], sep='\n')
            count += 1
        except Exception as e:
            break
    print('Готово\n')


def new_product():
    try:
        name = input('Name\n>>>')
        price = input('Price\n>>>')
        long = input('Time\n>>>')
        zam = input('Zametka\n>>>')
        description = input('Description\n>>>')
        ava = input('url\n>>>')
        execute = 'INSERT INTO production VALUES (%s, %s, %s, %s, %s, %s)'
        x = cur.execute(execute, (name, price, description, long, zam, ava))
        print(x)
        conn.commit()
        print(f'\n\nСоздан новый товар\nИмя: {name}\nЦена: {price}/{long}\nОписание: {description}\nСсылка на аву: {ava}\nЗаметка: {zam}\n\n')
    except Exception as e:
        print('Error')
        print(e)


def thinking():

    choice = input('[D]elete | [C]lear | [S]ozdat | [P]rint | [E]xit: ').upper()

    if choice[0] == 'D' or choice[0] == 'В':
        delete()
        thinking()

    if choice[0] == 'S' or choice[0] == 'Ы':
        new_product()
        thinking()

    elif choice[0] == 'C' or choice[0] == 'С':
        clear()
        thinking()

    elif choice[0] == 'P' or choice[0] == 'З':
        print_users()
        thinking()

    elif choice[0] == 'E' or choice[0] == 'Е':
        print("Выходим...")
        sys.exit()

    else:
        print("Выбран не тот режим \n")
        thinking()


if __name__ == '__main__':
    thinking()
