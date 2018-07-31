def is_terminal_state(state):
    commands = state['__COMMANDS__']
    for c in commands:
        if c['command'] == 'TERMINATE':
            return True
    return False
