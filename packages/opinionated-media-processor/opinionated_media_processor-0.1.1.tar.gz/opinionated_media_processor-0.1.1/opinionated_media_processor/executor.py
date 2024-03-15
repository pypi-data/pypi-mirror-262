import subprocess


def execute(command):
    output = []

    command_list = []
    for item in command:
        if isinstance(item, str):
            command_list.append(item)
        elif isinstance(item, list):
            for subitem in item:
                command_list.append(str(subitem))
        else:
            command_list.append(str(item))

    print("Command: ".join(command_list))
    p = subprocess.Popen(
        command_list,
        bufsize=1,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )

    for line in p.stdout:
        output.append(line.strip())

        print(line, end="")

    retcode = p.wait()
    if retcode != 0:
        raise Exception(
            f"An error occurred when running the command '{' '.join(command_list)}'. "
            f"The command was not executed. Error code returned: {retcode}"
        )

    return output
