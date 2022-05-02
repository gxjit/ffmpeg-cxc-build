import stat
from argparse import ArgumentParser
from datetime import datetime
from functools import partial
from os import chdir, environ, mkdir
from pathlib import Path
from subprocess import run
from sys import exit
from zipfile import ZipFile


def parseArgs():
    parser = ArgumentParser()
    buildSelect = parser.add_mutually_exclusive_group(required=True)
    buildSelect.add_argument("-l", "--linux64", action="store_true")
    buildSelect.add_argument("-w", "--mingw64", action="store_true")
    parser.add_argument("-uh", "--home", action="store_true")

    return parser.parse_args()


pargs = parseArgs()

repoName = "ffmpeg-cxc-build"
repoUrl = f"https://github.com/gxjit/{repoName}.git"

buildRoot = Path.cwd() if not pargs.home else Path.home()

logDTime = lambda: datetime.now().strftime("%y%m%d-%H%M%S")
fDate = lambda: datetime.now().strftime("%d-%m-%y")

if pargs.linux64:
    buildType = "native"
    buldTarget = "linux64"
elif pargs.mingw64:
    buildType = "cxc"
    buldTarget = "mingw64"
else:
    exit()

buildName = f"ff{buldTarget}-build"
rootPath = buildRoot.joinpath(buildName)
hintsFile = rootPath.joinpath(repoName).joinpath(
    f"ffmpeg-{buildType}-build-hints-custom"
)
buildLog = rootPath.joinpath(f"{buildName}.log")
assetsZip = rootPath.joinpath(f"{buildName}-{fDate()}.zip")
# cmdPath
cmdPath = f"{rootPath}/{repoName}/ffmpeg-{buildType}-{buldTarget}"

if not pargs.mingw64:
    cmdPath = cmdPath.replace(f"-{buldTarget}", "")

print(f"\nBuilding for {buldTarget} in {rootPath}\n")

deps = (
    "autoconf automake build-essential libarchive-tools cmake git-core "
    "gperf libtool mercurial nasm pkg-config "
    "python-lxml ragel subversion texinfo yasm wget autopoint meson"
)

if pargs.mingw64:
    deps = f"{deps} g++-mingw-w64 gcc-mingw-w64"

runP = partial(run, shell=True, check=True)

runP(f"sudo apt-get -y install {deps}")

mkdir(rootPath)
chdir(rootPath)

runP(f"git clone --depth 1 {repoUrl}")

usrEnv = environ.copy()
usrEnv["ROOT_PATH"] = rootPath
usrEnv["HINTS_FILE"] = hintsFile

runP(f"chmod +rx {cmdPath}")
# chmod(cmdPath, stat.S_IRUSR)
# chmod(cmdPath, stat.S_IXUSR)

runP(
    f"bash {cmdPath} 2>&1 | tee {buildLog}",
    env=usrEnv,
)

built = list(rootPath.rglob("bin/ff*"))

with ZipFile(assetsZip, "w") as zipit:
    for f in built:
        zipit.write(f, f.name)
    zipit.write(buildLog, buildLog.name)


# shlex.split()
# chdir(buildRoot)
# print(list(rootPath.glob("**/ff*build*.zip")))
# workflows/b* bin/ff*
# rootPath = f"{buildRoot}/ff{buldTarget}-build-{logDTime()}" , ffmpeg-build-{logDTime()}.log"
# run("pip3 install -U --user meson", shell=True)
