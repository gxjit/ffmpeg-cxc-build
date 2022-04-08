from subprocess import run
from sys import argv, exit
from datetime import datetime
from os import mkdir, chdir, environ, chmod
from os.path import expanduser
import stat

# run("sudo apt-get -y install autoconf automake build-essential libarchive-tools cmake git-core gperf g++-mingw-w64 gcc-mingw-w64 libtool mercurial meson nasm pkg-config python-lxml ragel subversion texinfo yasm wget autopoint -y")

repoName = "ffmpeg-cxc-build"
repoUrl = f"https://github.com/gxjit/{repoName}.git"

usrHome = expanduser("~")
currDTime = lambda: datetime.now().strftime("%y%m%d-%H%M%S")

run("pip3 install -U --user meson")

nativeBuild = None
if len(argv) > 1 and argv[1] == "native":
    nativeBuild = True

if nativeBuild:
    buildType = "native"
    buldTarget = "linux64"
else:
    buildType = "cxc"
    buldTarget = "mingw64"

print(f"\nBuilding for {buldTarget}\n")

rootPath = f"{usrHome}/ff{buldTarget}-build-{currDTime()}"

mkdir(rootPath)
chdir(rootPath)

run(f"git clone {repoUrl}")

cmdPath = f"{rootPath}/{repoName}/ffmpeg-{buildType}-{buldTarget}"

usrEnv = environ.copy()
usrEnv["ROOT_PATH"] = rootPath
usrEnv["HINTS_FILE"] = f"{rootPath}/{repoName}/ffmpeg-{buildType}-build-hints-custom"

if nativeBuild:
    cmdPath = cmdPath.replace(f"-{buldTarget}", "")

run(f"chmod +rx {cmdPath}")
chmod(cmdPath, stat.S_IXUSR)

run(f"sh {cmdPath} 2>&1 | tee {rootPath}/ffmpeg-build-{currDTime()}.log",shell=True, env=usrEnv, text=True)
