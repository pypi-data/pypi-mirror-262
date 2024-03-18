import multiprocessing
import os
import os.path
import platform
import subprocess
import sys
from shutil import which
from skbuild import setup

# CMake Options
SP2_USE_VCPKG = os.environ.get("SP2_USE_VCPKG", "1").lower() in ("1", "on")
CMAKE_OPTIONS = (
    ("SP2_BUILD_NO_CXX_ABI", "0"),
    ("SP2_BUILD_TESTS", "1"),
    ("SP2_MANYLINUX", "0"),
    ("SP2_BUILD_KAFKA_ADAPTER", "1"),
    ("SP2_BUILD_PARQUET_ADAPTER", "1"),
    # NOTE:
    # - omit vcpkg, need to test for presence
    # - omit ccache, need to test for presence
    # - omit coverage/gprof, not implemented
    # - omit ld classic, need to test for right system
)

# This will be used for e.g. the sdist
if SP2_USE_VCPKG:
    if not os.path.exists("vcpkg"):
        subprocess.call(["git", "clone", "https://github.com/Microsoft/vcpkg.git"])
    if not os.path.exists("vcpkg/ports"):
        subprocess.call(["git", "submodule", "update", "--init", "--recursive"])
    if not os.path.exists("vcpkg/buildtrees"):
        subprocess.call(["git", "pull"], cwd="vcpkg")
        if os.name == "nt":
            subprocess.call(["bootstrap-vcpkg.bat"], cwd="vcpkg")
            subprocess.call(["vcpkg", "install"], cwd="vcpkg")
        else:
            subprocess.call(["./bootstrap-vcpkg.sh"], cwd="vcpkg")
            subprocess.call(["./vcpkg", "install"], cwd="vcpkg")


python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
cmake_args = [f"-DSP2_PYTHON_VERSION={python_version}"]
vcpkg_toolchain_file = os.path.abspath(
    os.environ.get(
        "SP2_VCPKG_PATH",
        os.path.join("vcpkg/scripts/buildsystems/vcpkg.cmake"),
    )
)

if SP2_USE_VCPKG and os.path.exists(vcpkg_toolchain_file):
    cmake_args.extend(
        [
            "-DCMAKE_TOOLCHAIN_FILE={}".format(vcpkg_toolchain_file),
            "-DSP2_USE_VCPKG=ON",
        ]
    )
else:
    cmake_args.append("-DSP2_USE_VCPKG=OFF")

if "CXX" in os.environ:
    cmake_args.append(f"-DCMAKE_CXX_COMPILER={os.environ['CXX']}")

if "DEBUG" in os.environ:
    cmake_args.append("-DCMAKE_BUILD_TYPE=Debug")

for cmake_option, default in CMAKE_OPTIONS:
    if os.environ.get(cmake_option, default).lower() in ("1", "on"):
        cmake_args.append(f"-D{cmake_option}=ON")
    else:
        cmake_args.append(f"-D{cmake_option}=OFF")

if "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ:
    os.environ["CMAKE_BUILD_PARALLEL_LEVEL"] = str(multiprocessing.cpu_count())

if platform.system() == "Darwin":
    os.environ["OSX_DEPLOYMENT_TARGET"] = os.environ.get("OSX_DEPLOYMENT_TARGET", "10.13")
    os.environ["MACOSX_DEPLOYMENT_TARGET"] = os.environ.get("OSX_DEPLOYMENT_TARGET", "10.13")

if hasattr(platform, "mac_ver") and platform.mac_ver()[0].startswith("14"):
    cmake_args.append("-DSP2_USE_LD_CLASSIC_MAC=ON")

if which("ccache") and os.environ.get("SP2_USE_CCACHE", "") != "0":
    cmake_args.append("-DSP2_USE_CCACHE=On")

print(f"CMake Args: {cmake_args}")

setup(
    name="sp2",
    version="0.0.3",
    packages=["sp2"],
    cmake_install_dir="sp2",
    cmake_args=cmake_args,
    # cmake_with_sdist=True,
)
