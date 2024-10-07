import serial
import asyncio


class InitPort:
    def __init__(self, port: str, baudrate: int = 9600, bytesize: int = 8, parity: str = 'N', stopbits: int = 1,
                 timeout: float = None, xonxoff: bool = False, rtscts: bool = False, type: bool = True):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self.running = True
        self.serial_connection = None
        self.type = type

        self._initialize_port()

    def _initialize_port(self):
        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                parity=self.parity,
                stopbits=self.stopbits,
                timeout=self.timeout,
                xonxoff=self.xonxoff,
                rtscts=self.rtscts
            )
            print(f"Порт {self.port} успешно инициализирован.")
        except Exception as e:
            print(f"Ошибка при инициализации порта {self.port}: {e}")
            self.serial_connection = None

    def close(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print(f"Порт {self.port} закрыт.")

    def is_open(self) -> bool:
        return self.serial_connection and self.serial_connection.is_open

    def write(self, data: bytes):
        if self.is_open():
            self.serial_connection.write(data)
            print(f"Written data: {data}")
            self.serial_connection.flush()
        else:
            print("Порт не открыт для записи.")

    async def write_loop(self, data):
        if not self.is_open():
            print("Порт не открыт.")
            return False

        try:
            self.write(data.encode("utf-8"))
            print(f"Отправлено данных: {data}")
            return True
        except Exception as e:
            print(f"Ошибка при отправке данных: {e}")
            return False

    def read(self, size: int = 1) -> bytes:
        if self.is_open():
            data = self.serial_connection.read(size)
            print(f"Read data: {data}")
            return data
        else:
            print("Порт не открыт для чтения.")
            return b''

    async def check_input(self):
        while self.running:
            user_input = await asyncio.get_event_loop().run_in_executor(None, input)
            if user_input == 'q':
                print("Прервано пользователем.")
                self.running = False

    async def read_loop(self):
        if not self.is_open():
            print("Порт не открыт.")
            return

        print("Начало чтения данных. нажмите 'q' чтобы выйти")

        try:
            while self.running:
                try:
                    data = self.read(100)
                    if data:
                        print(f"Полученные данные: {data}, {len(data)} байт")
                except Exception as e:
                    print(f"Ошибка при чтении данных: {e}")
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            print("Чтение отменено.")
        except Exception as e:
            print(f"Ошибка при выполнении read_loop: {e}")
        except KeyboardInterrupt:
            print("Прервано пользователем.")
        finally:
            self.close()

    async def run(self):
        await asyncio.gather(self.read_loop(), self.check_input())

    async def real_read(self):
        await self.read_loop()

    def apply_new_settings(self, **kwargs):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()

        for key, value in kwargs.items():
            setattr(self.serial_connection, key, value)

        self.serial_connection.open()

    def __del__(self):
        self.close()
