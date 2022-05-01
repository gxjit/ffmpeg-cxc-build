from subprocess import run
from sys import argv, exit
from datetime import datetime
from os import mkdir, chdir, environ, chmod, getcwd
from os.path import expanduser
import stat

repoName = "ffmpeg-cxc-build"
repoUrl = f"https://github.com/gxjit/{repoName}.git"

buildRoot = getcwd()
# usrHome = expanduser("~")
currDTime = lambda: datetime.now().strftime("%y%m%d-%H%M%S")

nativeBuild = None
if len(argv) > 1 and argv[1] == "native":
    nativeBuild = True

if nativeBuild:
    buildType = "native"
    buldTarget = "linux64"
else:
    buildType = "cxc"
    buldTarget = "mingw64"

rootPath = f"{buildRoot}/ff{buldTarget}-build"

print(f"\nBuilding for {buldTarget}\n")

deps = (
    "autoconf automake build-essential libarchive-tools cmake git-core"
    "gperf g++-mingw-w64 gcc-mingw-w64 libtool mercurial nasm pkg-config"
    "python-lxml ragel subversion texinfo yasm wget autopoint meson"
)

if nativeBuild:
    deps = deps.replace("g++-mingw-w64 gcc-mingw-w64 ", "")

run(f"sudo apt-get -y install {deps}", shell=True)


mkdir(rootPath)
chdir(rootPath)

run(f"git clone {repoUrl}", shell=True)

cmdPath = f"{rootPath}/{repoName}/ffmpeg-{buildType}-{buldTarget}"

usrEnv = environ.copy()
usrEnv["ROOT_PATH"] = rootPath
usrEnv["HINTS_FILE"] = f"{rootPath}/{repoName}/ffmpeg-{buildType}-build-hints-custom"

if nativeBuild:
    cmdPath = cmdPath.replace(f"-{buldTarget}", "")

run(f"chmod +rx {cmdPath}", shell=True)
# chmod(cmdPath, stat.S_IRUSR)
# chmod(cmdPath, stat.S_IXUSR)


run(
    f"bash {cmdPath} 2>&1 | tee {rootPath}/ffmpeg-build.log",
    shell=True,
    env=usrEnv,
)

# shlex.split()
# rootPath = f"{buildRoot}/ff{buldTarget}-build-{currDTime()}" , ffmpeg-build-{currDTime()}.log"
# run("pip3 install -U --user meson", shell=True)
