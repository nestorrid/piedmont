from piedmont import Piedmont
import os

config = os.path.join(os.path.abspath(os.path.curdir), 'config.yaml')
print(config)

pie = Piedmont(config)


@pie.bridge('test')
def demo(data):
    print(f'> received data:{data}')
    pie.send_pp_connection('test', 'aaa')


@pie.bridge('message')
def message_handler(data):
    print(f'> received data:{data}')
    pie.send_pp_connection('Response', 'Response from Bridge App')


@pie.bridge('json')
def returnJson(data):
    pie.send_pp_connection('jsonData', {
        "key": "value"
    })


@pie.serial('KNOB_GEAR_SHIFT')
def gear_shift_handler(data: str):
    pie.send_pp_connection('KNOB_GEAR_SHIFT', data)


@pie.serial('KNOB_ROTATE')
def knob_rotate_handler(data: str):
    pie.send_pp_connection('KNOB_ROTATE', data)


@pie.serial('KNOB_VALUE')
def knob_value_handler(data: str):
    pie.send_pp_connection('KNOB_VALUE', data)


if __name__ == "__main__":

    while True:
        try:
            cmd = input("input message id or 'exit' to quit.\n> ")
            if cmd.lower() == 'exit':
                exit()
            value = input("input a value:\n> ")
            pie.send_pp_connection(cmd, value)
        except KeyboardInterrupt:
            print("Exit.")
            exit()
