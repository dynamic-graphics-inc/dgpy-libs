import tarfile
import zipfile

from rich import print

from shellfish import sh


def get_wheel_files_list(wheel_filepath: str):
    return zipfile.ZipFile(wheel_filepath).namelist()


def get_targz_files_list(targz_filepath):
    with tarfile.open(targz_filepath, "r:gz") as tar:
        return tar.getnames()


def main():
    files = list(sh.files_gen("dist"))
    wheels = [f for f in files if f.endswith(".whl")]
    targzs = [f for f in files if f.endswith(".tar.gz")]
    for f in wheels:
        print("------------------------")
        print(f)
        print(get_wheel_files_list(f))
    for f in targzs:
        print("------------------------")
        print(f)
        print(get_targz_files_list(f))


if __name__ == "__main__":
    main()
