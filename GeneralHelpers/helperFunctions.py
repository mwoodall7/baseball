import subprocess


def getDictItemByKey(d, key):
    if key in d:
        return d[key]
    for k, v in d.items():
        if isinstance(v, dict):
            item = getDictItemByKey(v, key)
            if item is not None:
                return item
    return None


def getCmdOutput(command, getErr=False):
    output = None
    with subprocess.Popen(command, shell=True, stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          encoding='utf-8') as proc:
        out, err = proc.communicate()
        output = "stdout: " + out if out != '' and not getErr else "stderr: " + err
    return output
