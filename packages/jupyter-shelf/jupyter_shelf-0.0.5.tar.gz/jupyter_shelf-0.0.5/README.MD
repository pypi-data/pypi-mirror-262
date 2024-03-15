## Jupyter Shelf

If you are using Jupyter notebooks extensively and need a convenient way to use virtual environments with the notebooks, Shelf may be suitable for you.

Shelf allows you create a virtual environment and use it with a set of notebooks in a Jupyter lab environment, hence the name shelf.

It is easy to create and dispose shelves. Shelf can help you organize your workspace and notebooks.

### Why Shelf was needed ?

I use Jupyter notebooks for a wide range of tasks ranging from testing python libraries&tools to training&testing language models. Most of the time testing requires a different python environment. I always needed to use Jupyter notebooks with use virtual environments. You need to run several commands to create a kernel from a virtual environment and then you can use the kernel within the jupyter lab. This manual approach kept me away from using virtual environments. Then I developed several bash functions to alleviate the burden of managing virtual environment kernels. Then I realized that I need a real solution that I can use in different environments. 

## Instructions

### Installation
```bash
pip install jupyter-shelf --upgrade
```

Print Help:
```bash
shelf -h
```
Sample output:
```text
usage: shelf [-h] {mk,rm,ls,start,stop} ...

positional arguments:
  {mk,rm,ls,start,stop}
    mk                  Create a new shelf.
    rm                  Remove specified shelf. Retains notebooks.
    ls                  List shelves in the given root directory.
    start               Start jupyter lab in the specified shelf.
    stop                Stop jupyter lab running in the specified shelf.

options:
  -h, --help            show this help message and exit
```

#### Trouble shooting

During installation, if a virtual environment is used or a conda distribution is used, shelf executable should end up in the system path. In other situations, shelf executable may be put in a location that is not in the system path. As a precaution, `~/.bashrc` file is modified such that `~/.local/bin/` is added to the PATH variable.

If you experience `shelf: command not found` errors, you may need to find shelf executable and put it to your PATH.

### How to use?

#### Make a shelf

Create a shelf named hf-demo under the given root directory.
```bash
shelf mk hf-demo --root ~/workspace/shelves --python-version 3.11
```

This will create `~/workspace/shelves/hf-demo` directory. Initialize a virtual environment there. Install jupyter-lab. And create src directory to keep notebooks.

`~/workspace/shelves` is the default shelf root and can be omitted. A typical usage would look like this:

```bash
shelf mk torch-demo
```
List all shelves under a root directory. 
```bash
shelf ls --root ~/workspace/shelves
```
Again `~/workspace/shelves` is the default root and can be omitted.

#### Start jupyter lab

Following command will start jupyter lab in the given shelf.
```bash
shelf start hf-demo --root ~/workspace/shelves --port 8888
```

Jupyter-lab will start in `src` sub-directory of the shelf. `8888` is the default port used by jupyter and can be omitted. If collusion occurs, jupyter will try next port. So typical usage would look like this:
```bash
shelf start hf-demo
```

Send CTRL+C to kill the Jupyter process. You can have multiple jupyter processes starting from different shells but each one will block its shell until you send CTRL+C. Starting multiple jupyter processes in the same shelf is possible but not recommended.

#### Remove a shelf

Following command will remove a shelf directory.
```bash
shelf rm hf-demo --root ~/workspace/shelves
```
This command will not remove `src` directory if it contains any files. This is to ensure your source files are not wasted. This command does not have an override option. If you are sure about deleting your source files, you will need to do it manually.


## Commands to publish

Make sure you are up-to-date.
```bash
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine
```
Build and publish
```bash
python3 -m build
python3 -m twine upload --repository pypi dist/*
```

## References
1. [Packaging](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
2. [Entry point](https://setuptools.pypa.io/en/latest/userguide/entry_point.html)
3. [Sample Setup-tools Project](https://github.com/pypa/sampleproject/tree/main)