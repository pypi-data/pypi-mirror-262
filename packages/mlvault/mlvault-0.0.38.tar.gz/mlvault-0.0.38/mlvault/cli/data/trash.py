from os import getcwd, listdir, path, remove
from shutil import move
from mlvault.util import resolve_relative_path
from mlvault.util import find_args

print(path.basename("asdasdas/dasdasf/sdfsd/test.file"))

def run_trash(args:list[str]):
    trash_bin = find_args(args, "-t")
    if not trash_bin:
        print("Please provide a trash bin")
        exit(1)
    trash_path = resolve_relative_path(trash_bin)
    to_delete_files = listdir(trash_path)
    to_delete_captions = list(map(lambda file: f"{path.splitext(file)[0]}.txt", to_delete_files))
    to_delete_files_and_captions = to_delete_files + to_delete_captions
    current = getcwd()
    maybe_targets = listdir(current)
    delete_targets = []
    for dir in maybe_targets:
        if dir != trash_bin and path.isdir(dir):
            items = listdir(dir)
            for item in items:
                if item in to_delete_files_and_captions:
                    to_del_file_path = path.join(dir, item)
                    print(f"Deleting {to_del_file_path} from {dir}")
                    delete_targets.append(to_del_file_path)
    print(f"Moving {len(delete_targets)} files to trash bin, are you sure? (y/n)")
    if input().lower() == "y":
        for file in delete_targets:
            filename = path.basename(file)
            move(file, f"{trash_path}/{filename}")
        print("Deleted files successfully")
