import pexpect

def interfaces():
    ip_address = '192.168.56.101'
    username = 'prne'
    password = 'cisco123!'
    password_enable = 'class123!'

    session = pexpect.spawn(f'ssh -o StrictHostKeyChecking=no {username}@{ip_address}', encoding='utf-8', timeout=60)
    result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])
    print(f'SSH connection result: {result}')

    if result == 0:
        session.sendline(password)
    else:
        print('Fail! Creating session for:', ip_address)
        newip = input('Try a different IP address: ')
        session = pexpect.spawn(f'ssh -o StrictHostKeyChecking=no {username}@{newip}', encoding='utf-8', timeout=60)

    result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])
    print(f'Prompt for regular mode result: {result}')
    if result != 0:
        print('Fail! Entering password:', password)
        exit()

    session.sendline('enable')
    result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])
    print(f'Enable mode result: {result}')

    if result == 0:
        session.sendline(password_enable)
    else:
        print('Failure! Entering enable mode')
        exit()

    result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])
    print(f'Prompt after enable mode result: {result}')
    if result != 0:
        print('Failure! Entering enable mode after sending password!')
        exit()

    session.sendline('conf t')
    result = session.expect([r'\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
    print(f'Configuration mode result: {result}')
    if result != 0:
        print('Failure entering config mode')
        exit()

    running11 = True
    while running11:
        print('Choose an option: ')
        print('1. Configure loopback address')
        print('2. Configure another interface address')
        print('3. Remove IP address from interface')
        print('4. Show IP interface')
        print('5. Exit')
        a = input('Option: ')

        if a == '1':
            b = input('Number Loopback: ')
            session.sendline(f'interface loop
