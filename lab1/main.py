import argparse

from port import CheckPort
import asyncio
from file.RWFile import RWFile
from port.PortManager import PortManager


async def monitor_ports(port_manager, rw_file):
    while True:
        choice_ports = get_ports(rw_file)
        tasks = []

        async with asyncio.TaskGroup() as tg:
            for port in choice_ports.values():
                com_port = port_manager.get_port_descriptor(port)
                if getattr(com_port, 'type'):
                    print(f"sending port: {port}")
                else:
                    print(f"receiving port: {port}")
                    tasks.append(tg.create_task(com_port.real_read()))

        await asyncio.sleep(5)


def main():
    port_manager = PortManager()
    rw_file = RWFile()
    check_ports = CheckPort.Port.find_pts_ports()
    ports = CheckPort.Port.check_ports(check_ports)

    parser = argparse.ArgumentParser(description="Serial communication CLI tool.")
    parser.add_argument('action', choices=['send', 'receive', 'check', 'state'], help="Action to perform")
    args = parser.parse_args()
    i = 0

    if args.action == 'send':
        try:
            port = ports[i]
            rw_file.save_ports_to_file(port)
            comx_port = port_manager.get_port_descriptor(port, type=True)
            print(f"Sending on {port}")
            comx_port.write_loop()
        except Exception as e:
            print(f"Error during sending: {e}")

    elif args.action == 'receive':
        try:
            port = ports[i]
            rw_file.save_ports_to_file(port)
            comy1_port = port_manager.get_port_descriptor(port, type=False)
            print(f"Receiving on {port}")
            asyncio.run(comy1_port.run())
        except Exception as e:
            print(f"Error during receiving: {e}")

    elif args.action == 'check':
        baud_rates = [300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000]
        while True:
            choice_ports = get_ports(rw_file)
            choice = input("какой порт обновить хотите? 'q' для выхода  ").strip()
            if choice == 'q':
                return
            else:
                port_name = choice_ports.get(int(choice))
                if port_name:
                    i = 1
                    for baud_rate in baud_rates:
                        print(f"{i}: {baud_rate}")
                        i += 1
                    baudrate = int(input("Enter new baudrate: ").strip())
                    port_manager.update_port_config(port_name, baudrate=baud_rates[baudrate - 1])
                    print(getattr(port_manager.get_port_descriptor(port_name), 'baudrate'))
                else:
                    print(f"Invalid choice")
    elif args.action == 'state':
        asyncio.run(monitor_ports(port_manager, rw_file))
    port_manager.close_all_ports()
    rw_file.clear_ports_file()


def get_ports(rw_file):
    i = 1
    choices = {}
    for port in rw_file.read_port_from_file():
        print(f"{i}: {port.strip()}")
        choices[i] = port.strip()
        i += 1
    return choices


if __name__ == "__main__":
    main()
