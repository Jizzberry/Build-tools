import compileall
import os
import shutil
import zipfile
from os.path import relpath
from urllib.request import Request, urlopen

BASE_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__)))

out_path = os.path.join(BASE_DIR, "build")
download_path = os.path.join(BASE_DIR, "downloads")
app_dir = "app"
Jizzberry_dir = os.path.join(BASE_DIR, "Jizzberry-Django")

output_path_win64 = os.path.join(out_path, "Jizzberry-win64")
platform_win64 = os.path.join(BASE_DIR, "platform", "win64")
arch_win64 = "win64"

output_path_win32 = os.path.join(out_path, "Jizzberry-win32")
platform_win32 = os.path.join(BASE_DIR, "platform", "win32")
arch_win32 = "win32"


def compile_py():
    print("Compiling python files...")
    compileall.compile_dir(Jizzberry_dir, quiet=True, force=True)


def make_dirs(output_path):
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    if os.path.exists(os.path.join(output_path)):
        for root, dirs, files in os.walk(output_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.makedirs(os.path.join(output_path, app_dir))


def copy_files(output_dir, arch):
    print("Copying files...")
    for (dirpath, dirnames, filenames) in os.walk(Jizzberry_dir):
        for item in filenames:
            extension = os.path.splitext(item)[1]
            if extension == ".pyc":
                item_tmp = item[:]
                item = item.replace('.cpython-38', "")
                folder = relpath(dirpath, Jizzberry_dir).replace("__pycache__", "")
                if not os.path.exists(os.path.join(os.path.join(output_dir, app_dir), folder)):
                    os.makedirs(os.path.join(os.path.join(output_dir, app_dir), folder))
                shutil.copy(os.path.join(dirpath, item_tmp), os.path.join(os.path.join(output_dir, app_dir),
                                                                          folder, item))
    shutil.copytree(os.path.join(Jizzberry_dir, "Jizzberry", "templates"), os.path.join(output_dir, app_dir,
                                                                                        "Jizzberry", "templates"))
    if not os.path.exists(os.path.join(output_dir, app_dir, "Database")):
        os.makedirs(os.path.join(output_dir, app_dir, "Database"))
    shutil.copy(os.path.join(Jizzberry_dir, "Database", "Pornstar_data.db"),
                os.path.join(output_dir, app_dir, "Database", "Pornstar_data.db"))
    shutil.copytree(os.path.join(download_path, arch), os.path.join(output_dir, "py-dist"))
    shutil.copy(os.path.join(BASE_DIR, "launch.bat"), os.path.join(output_dir, app_dir, "launch.bat"))


def download_packages(url, arch):
    if not os.path.exists(os.path.join(download_path, arch)):
        print("Downloading package: " + arch + ".zip")
        file_name = arch + ".zip"
        useragent = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'
        req = Request(url=url, headers={'User-Agent': useragent})
        filedata = urlopen(req)
        datatowrite = filedata.read()
        if url.endswith('.zip'):
            with open(os.path.join(download_path, file_name), 'wb') as f:
                f.write(datatowrite)
        unzip(file_name, arch)


def unzip(file_name, arch):
    print("Unzipping package: " + arch + ".zip")
    with zipfile.ZipFile(os.path.join(download_path, file_name), 'r') as zip_ref:
        zip_ref.extractall(os.path.join(download_path, arch))
    os.remove(os.path.join(download_path, file_name))


def generate(url, output_dir, arch):
    make_dirs(output_dir)
    download_packages(url=url, arch=arch)
    compile_py()
    copy_files(output_dir, arch)


def generate_win64():
    generate(url="https://github.com/Jizzberry/Portable-Python-Installations/raw/master/win64.zip", arch="win64"
             , output_dir=output_path_win64)


def generate_win32():
    generate(url="https://github.com/Jizzberry/Portable-Python-Installations/raw/master/win32.zip", arch="win32"
             , output_dir=output_path_win32)


def generate_all():
    generate_win64()
    generate_win32()


if __name__ == '__main__':
    archs = {
        1: generate_win64,
        2: generate_win32,
        3: generate_all
    }

    arch_choice = int(input("Choose arch\n1: Win64\n2: Win32\n3: All\n[1-3]: "))
    func = archs.get(arch_choice, lambda: "Invalid arch")()
