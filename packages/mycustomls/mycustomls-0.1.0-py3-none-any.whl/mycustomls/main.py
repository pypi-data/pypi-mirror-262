import os
import stat
import sys
import argparse
import click

@click.command()
@click.argument('path',default=".", type=click.Path(exists=True))
@click.option('-l','--list', is_flag=True, help='List all files')
@click.option('-a','--all', is_flag=True, help='List hidden files')
def list_directory(path, list, all):
    try:
        entries = os.listdir(path)
        if not all:
            entries = [entry for entry in entries if not entry.startswith('.')]
        for entry in entries:
            if list:
                full_path = os.path.join(path, entry)
                stat_info = os.stat(full_path)
                permissions = stat.filemode(stat_info.st_mode)
                n_links = stat_info.st_nlink
                size = stat_info.st_size
                click.echo(f'{permissions} {n_links} {size} {entry}')
            else:
                click.echo(entry)
    except FileNotFoundError:
        print(f"Error: The directory '{path}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied to list contents of '{path}'.")



# parser = argparse.ArgumentParser(description='list all files in a directory')
# parser.add_argument('directory', nargs="?", default=".", help="the directory")
# parser.add_argument('-l','--list', action="store_true", help="list all data")
# parser.add_argument('-a','--all', action="store_true", help=" show hidden files")
# args = parser.parse_args()

if __name__ == '__main__':
    list_directory()




