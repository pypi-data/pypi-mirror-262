import os

from setuptools import find_packages, setup

EXCLUDE = [
    "test",
    "test.core",
    "test.extensions",
    "benchmarks",
]


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, "dothttp", "__version__.py"), "r") as f:
    exec(f.read(), about)


# windows_req = "python-magic-bin==0.4.14"


def requirements():
    reqs = [req.split(";")[0] for req in read("requirements.txt").split("\n")]
    # if sys.platform == 'win32':
    #     return reqs.append(windows_req)
    return reqs


setup(
    name="dothttp_req-wasm",
    author="prasanth",
    author_email="kesavarapu.siva@gmail.com",
    description=("DotHttp recommended tool for making http requests."),
    license="MIT",
    package_data={"": ["*.tx", "*.md", "*.js"]},
    include_package_data=True,
    options={"bdist_wheel": {"universal": False}},
    packages=find_packages(exclude=EXCLUDE),
    install_requires=requirements(),
    long_description=read("README.md"),
    long_description_content_type=("text/markdown"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    version=about["__version__"],
)
