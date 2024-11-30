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
            session.sendline(f'interface loopback {b}')
            result = session.expect([r'\(config-if\)#', pexpect.TIMEOUT, pexpect.EOF])
            print(f'Loopback interface configuration result: {result}')
            if result != 0:
                print(f'Error: Unable to configure Loopback {b}. Please check your input.')
                continue

            ip = input('Please enter a loopback address (e.g., 192.168.1.1): ')
            session.sendline(f'ip address {ip} 255.255.255.0')
            result = session.expect([r'\(config-if\)#', pexpect.TIMEOUT, pexpect.EOF])
            print(f'Loopback IP address configuration result: {result}')
            if result != 0:
                print('Error: Invalid IP address entered or already configured.')
            else:
                print(f'Loopback {b} configured with IP address {ip}.')
            session.sendline('exit')

        elif a == '2':
            int2 = input('Interface you want to edit: (G0/0 or G0/1)')
            session.sendline(f'interface {int2}')
            result = session.expect([r'\(config-if\)#', pexpect.TIMEOUT, pexpect.EOF])
            print(f'Interface {int2} configuration result: {result}')
            if result != 0:
                print(f'Error: Unable to enter {int2} configuration.')
                continue

            ip2 = input(f'Please enter an IP address for {int2} (e.g., 192.168.1.1): ')
            session.sendline(f'ip address {ip2} 255.255.255.0')
            result = session.expect([r'\(config-if\)#', pexpect.TIMEOUT, pexpect.EOF])
            print(f'{int2} IP address configuration result: {result}')
            if result != 0:
                print('Error: Invalid IP address entered or already configured.')
            else:
                print(f'{int2} configured with IP address {ip2}.')
            session.sendline('exit')

        elif a == '3':
            interface = input('Enter the interface ID: ')
            session.sendline(f'interface {interface}')
            result = session.expect([r'\(config-if\)#'])
            print(f'Remove IP address from interface {interface} result: {result}')
            if result != 0:
                print(f'Error: Invalid interface {interface}.')
                continue

            session.sendline('no ip address')
            result = session.expect([r'\(config-if\)#', pexpect.TIMEOUT, pexpect.EOF])
            print(f'Removing IP address from {interface} result: {result}')
            if result != 0:
                print(f'Error: Unable to remove IP address from {interface}.')
            else:
                print(f'IP address removed from {interface}.')
            session.sendline('exit')

        elif a == '4':
            session.sendline('do show ip interface brief')
            result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])
            print(f'Show IP interface brief result: {result}')
            if result == 0:
                display = session.before.splitlines()[1:-1]
                for line in display:
                    print(line)
            else:
                print('Error: Unable to show IP interface brief.')

        elif a == '5':
            print('Exiting configuration.')
            running11 = False

        else:
            print('Invalid operation. Please try again.')

if __name__ == '__main__':
    interfaces()
