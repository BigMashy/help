
import pexpect


def interfaces():
    # Run SSH to retrieve and save the running configuration
    # This will save running config to existing-config.txt

    # Define the file to compare with
    ip_address = '192.168.56.101'
    username = 'prne'
    password = 'cisco123!'
    password_enable = 'class123!'

    session = pexpect.spawn(f'ssh -o StrictHostKeyChecking=no {username}@{ip_address}', encoding='utf-8', timeout=20)
    result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

    if result == 0:
        session.sendline(password)
    else:
        print('Fail! Creating session for:', ip_address)
        newip = input('Try a different IP address: ')
        session = pexpect.spawn(f'ssh -o StrictHostKeyChecking=no {username}@{newip}', encoding='utf-8', timeout=20)

    # Check prompt for regular mode
    result = session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])
    if result != 0:
        print('Fail! Entering password:', password)
        exit()

    # Enter enable mode
    session.sendline('enable')
    result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

    # Check for error
    if result == 0:
        session.sendline(password_enable)
    else:
        print('Failure! Entering enable mode')
        exit()

    # Check prompt after enable
    result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])
    if result != 0:
        print('Failure! Entering enable mode after sending password!')
        exit()

    session.sendline('conf t')
    result = session.expect([r'\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
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
            session.sendline('conf t')
            session.expect('#')
            b = input('Number Loopback: ')

            session.sendline(f'interface loopback{b}')
            result = session.expect([r'\(config-if\)#', pexpect.TIMEOUT, pexpect.EOF])
            if result != 0:
                print(f'Error: Unable to configure Loopback{b}. Please check your input.')
                continue

            ip = input('Please enter a loopback address (e.g., 192.168.1.1): ')
            session.sendline(f'ip address {ip} 255.255.255.0')
            result = session.expect([r'\(config-if\)#', pexpect.TIMEOUT, pexpect.EOF])
            if result != 0:
                print('Error: Invalid IP address entered or already configured.')
            else:
                print(f'Loopback{b} configured with IP address {ip}.')
            session.sendline('exit')

        elif a == '2':
            session.sendline('conf t')
            session.expect('#')
            result = session.expect([r'\(config-if\)#', pexpect.TIMEOUT, pexpect.EOF])
            result2 = session.expect([r'\(config\)#', pexpect.TIMEOUT, pexpect.EOF])
            if result != 0 or result2 != 0:
                print('Entering Configuration mode...')
                session.sendline('conf t')

            int2 = input('Interface you want to edit: (G0/0 or G0/1)')
            session.sendline(f'interface {int2}')
            result = session.expect([r'\(config-if\)#', pexpect.TIMEOUT, pexpect.EOF])
            if result != 0:
                print(f'Error: Unable to enter {int2} configuration.')
                continue

            ip2 = input(f'Please enter an IP address for {int2} (e.g., 192.168.1.1): ')
            session.sendline(f'ip address {ip2} 255.255.255.0')
            result = session.expect([r'\(config-if\)#', pexpect.TIMEOUT, pexpect.EOF])
            if result != 0:
                print('Error: Invalid IP address entered or already configured.')
            else:
                print(f'{int2} configured with IP address {ip2}.')
            session.sendline('exit')

        elif a == '3':
            session.sendline('conf t')
            session.expect('#')
            interface = input('Enter the interface ID: ')
            session.sendline(f'interface {interface}')
            result = session.expect([r'\(config-if\)#'])
            if result != 0:
                print(f'Error: Invalid interface {interface}.')
                continue

            session.sendline('no ip address')
            result = session.expect([r'\(config-if\)#', pexpect.TIMEOUT, pexpect.EOF])
            if result != 0:
                print(f'Error: Unable to remove IP address from {interface}.')
            else:
                print(f'IP address removed from {interface}.')
            session.sendline('exit')

        elif a == '4':

            session.sendline('exit')
            session.expect('#')
            session.sendline('end')
            session.expect('#')
            session.sendline('show ip interface brief')
            session.expect('#')
            display = session.before.splitlines()[1:-1]

            for a in display:
                print(a)

        elif a == '5':
            print('Exiting configuration.')
            running11 = False

        else:
            print('Invalid operation. Please try again.')


# Call interfaces to execute the process
if __name__ == '__main__':
    interfaces()