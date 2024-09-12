from typing import List
import os
import subprocess


class Port:

    @staticmethod
    def find_pts_ports() -> List[str]:
        pts_dir = "/dev/pts"
        if os.path.exists(pts_dir):
            pts_ports = [os.path.join(pts_dir, f) for f in os.listdir(pts_dir) if f.isdigit()]
            return pts_ports
        else:
            return []

    @staticmethod
    def __is_created_by_socat(port_name: str) -> bool:
        command = ['lsof', port_name]

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            output = result.stdout

            lines = output.splitlines()
            num_lines = len(lines)

            for line in lines:
                if 'socat' in line and num_lines==2:
                    return True
            return False
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении lsof: {e}")
            return False

    @staticmethod
    def check_ports(ports: List[str]) -> List[str]:
        socat_ports = []
        for port in ports:
            if Port.__is_created_by_socat(port):
                socat_ports.append(port)
        return socat_ports
