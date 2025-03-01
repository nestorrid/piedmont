import serial

PORT = "/dev/tty.usbmodem144201"
BAUDRATE = 115200

if __name__ == "__main__":
    try:
        # 打开串口
        ser = serial.Serial(PORT, BAUDRATE, timeout=1)
        print(f"Serial port {PORT} opened with baudrate {BAUDRATE}")

        while True:
            # 读取串口数据
            data = ser.readline()
            if data:
                try:
                    # 将接收到的字节数据解码为字符串
                    message = data.decode('utf-8').strip()
                    print(f"Received from Arduino: {message}")
                except UnicodeDecodeError:
                    print("Received data could not be decoded as UTF-8")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt as e:
        print(f"User interrupted.")
    finally:
        if 'ser' in locals() and ser.is_open:
            # 关闭串口
            ser.close()
            print(f"Serial port {PORT} closed")
