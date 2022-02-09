import sqlite3
import os
import argparse

db = sqlite3.connect('safe.db')
cur = db.cursor()


def create_table():
    sql = """
    CREATE TABLE if not exists SAFE(
    name TEXT UNIQUE,
    ext VARCHAR(5),
    bin_data BLOB
    );
    """
    cur.execute(sql)


create_table()


def upload_file(path):
    if not os.path.exists(path):
        print('File not Found.\nCheck filename/path correctly.')
        return
    filename, ext = os.path.splitext(os.path.basename(path))
    sql = 'INSERT INTO SAFE(name,ext,bin_data) VALUES(?,?,?)'
    file_to_upload = open(path, 'rb')
    file_content = file_to_upload.read()
    cur.execute(sql, (filename, ext, file_content))
    db.commit()
    print('Successfullly upload {}'.format(filename))
    return filename


def download_file(name):
    sql = 'SELECT * FROM SAFE WHERE name = ?'
    items = cur.execute(sql, (name,))
    file_data = [i for i in items]
    if not file_data:
        print('No file in database with name "{}"'.format(name))
        return
    file_data = file_data[0]

    filename = file_data[0]
    ext = file_data[1]
    bin_data = file_data[2]

    with open(filename+ext, 'wb') as f:
        f.write(bin_data)
    print('Successfully downloaded {}'.format(name))
    return True


def delete_file(name):
    sql = 'DELETE FROM SAFE WHERE name = ?'
    cur.execute(sql, (name,))
    db.commit()
    print('Successfully deleted {}'.format(name))


def all_files():
    sql = 'SELECT name,ext FROM SAFE'
    items = cur.execute(sql)
    files_data = [i for i in items]
    if not files_data:
        print('no files in database.')
    files_data = files_data[::-1]
    print('Files:\n')
    for file in files_data:
        print(file[0]+file[1])


# all_files()

my_parser = argparse.ArgumentParser(
    prog='safe.py', description='Completely hide sensitive files.')
my_parser.add_argument(
    '-u', '--upload', help='Enter file path to upload', action='store')
my_parser.add_argument(
    '-d', '--download', help='Enter file name to download', action='store')
my_parser.add_argument(
    '-r', '--remove', help='Enter filename to delete.', action='store')
my_parser.add_argument(
    '-a', '--all', help='Show all files', action='store_true')

args = my_parser.parse_args()

your_password = 'password'


def enter_password():
    password = input('Enter password: ')
    if password == your_password:
        return True
    print('Wrong password.')
    return False


if args.all:
    all_files()
elif args.upload:
    if enter_password():
        upload_file(args.upload)
elif args.download:
    if enter_password():
        download_file(args.download)
elif args.remove:
    if enter_password():
        delete_file(args.remove)
else:
    my_parser.print_help()
