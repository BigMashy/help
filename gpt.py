elif a == '4':
    # Ensure the session is in privileged EXEC mode (`#`)
    while True:
        session.sendline('')
        mode = session.expect([r'\(config-if\)#', r'\(config\)#', r'>', r'#', pexpect.TIMEOUT, pexpect.EOF])
        if mode == 0:  # In interface configuration mode
            session.sendline('exit')
        elif mode == 1:  # In global configuration mode
            session.sendline('end')
        elif mode == 2:  # In user EXEC mode
            session.sendline('enable')
            session.expect('Password:')
            session.sendline(password_enable)
        elif mode == 3:  # In privileged EXEC mode
            break
        else:  # Handle unexpected states
            print("Error: Unable to reach privileged EXEC mode.")
            return

    # Once in privileged EXEC mode, execute the command
    session.sendline('show ip interface brief')
    session.expect('#')
    display = session.before.splitlines()[1:]  # Capture command output, skip the command line

    # Print the output
    print("IP Interface Brief:")
    for line in display:
        print(line)
