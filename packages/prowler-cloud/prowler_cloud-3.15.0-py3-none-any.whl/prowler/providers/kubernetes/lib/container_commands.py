def check_container_command(commands, command, value = None):
    """
    Check if a command is present in the container commands.

    This function takes in a dictionary of container commands and checks if the
    specified command is present in the container commands.

    Args:
        commands (Dict[str, str]): The dictionary of container commands.
        command (str): The command to check for.
        value (str): The value to check for.

    Returns:
        bool: True if the command is present, False otherwise.
    """
    if command in commands:
        if value:
            if commands[command] == value:
                return True
            else:
                return False
        return True
    return False