<div align="center"><h1>sharepointNotification</h1><hr /></div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>

<!-- Getting started -->
## Getting started
To get a local copy of this repository up and running follow these steps

### Prerequisites
This tool has been build with Python 3.10, it might be able to run an previous versions of python 3, but if any problems arise, try Python 3.10
- [Python 3.10](https://www.python.org/downloads/)

### Installation
The following instructions all assume that you have an open terminal that's in the git folder

The step can be skipped, but it's recommended that you create a local environment

The instructions here will all assume that you have created a local environment
``` cmd
python -m venv .\venv 
```

Install required packages
``` cmd
.\venv\Scripts\pip.exe install -r .\requirements.txt
```

Open the `config.ini` in an editor of your choice.
This will include you login credentials for sharepoint, which view it should look at etc.

## Usage
Now you can run program
``` cmd
.\venv\Scripts\python.exe main.py
```
If `config.ini` wasn't updated you will get an error stating that it is missing e.g. username.

Alternatively, you can run the `run.ps1` script, that does the same thing.
