import sys
import subprocess
import os


def get_internal_jupyter_process_details():
    """
    Find out details of how Jupyter Lab is being executed in this environment 
    """
    runnig_exec = sys.executable 

    jupyter_process = {
        "base_url": "",
        "token": "",
        "auth_header_str": "",
        "directory": "",
        "runnig_exec": runnig_exec,
        "running_servers": [],
    }

    try:
        completed_process = subprocess.run(
            ["jupyter", "server", "list"], capture_output=True, timeout=2, check=True
        )
    except FileNotFoundError as exc:
        print(f"Process failed because the executable could not be found.\n{exc}")
    except subprocess.CalledProcessError as exc:
        print(
            f"Process failed because did not return a successful return code. "
            f"Returned {exc.returncode}\n{exc}"
        )
    except subprocess.TimeoutExpired as exc:
        print(f"Process timed out.\n{exc}")

    if completed_process.returncode != 0:
        print(f"Something went wrong -> Return code: {completed_process.returncode}")
    else:  
        outstr = completed_process.stdout.decode()
        servers = [srv for srv in outstr.split('\n') if "http" in srv]
        jupyter_process['running_servers'] = servers
        for server in servers:
            url_str, directory = server.split(' :: ')
            if directory in runnig_exec:
                jupyter_process['directory'] = directory
                jupyter_process['base_url'] = url_str.split('/?')[0]
                jupyter_process['token'] = url_str.split('token=')[1] if "token=" in url_str else ""
                jupyter_process['auth_header_str'] = " ".join(url_str.split('?')[1].split('=')) if jupyter_process['token'] else ""

    return jupyter_process


def safe_file_open_w(path):
    """ 
    Open "path"/file for writing, creating any parent directories as needed.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

    return open(path, 'w', newline='')


def safe_file_open_wb(path):
    """ 
    Open binary "path"/file for writing, creating any parent directories as needed.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

    return open(path, 'wb')


def parse_content_disposition_header(cd_header: str):
    """
    Extract the filename out of a Content-Disposition header string
    """
    header_chunks = cd_header.split(';')
    filename = "".join([chunk.split("=")[1].strip(' ').strip('\"') for chunk in header_chunks if "filename" in chunk])

    return filename
