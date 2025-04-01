
from core import create_table, list_snippets, add_snippet, table_exists

def print_hi(name):
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

if __name__ == '__main__':
    if table_exists('snippets'):
        print('Table exists')
    else:
        print('Table does not exist, creating now...')
        create_table()

