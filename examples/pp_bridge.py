from piedmont import Piedmont

pie = Piedmont()


@pie.bridge('test')
def demo(data):
    print(f'> received data:{data}')
    pie.send_pp_connection('test', 'aaa')


@pie.bridge('json')
def returnJson(data):
    pie.send_pp_connection('jsonData', {
        "key": "value"
    })

# @pie.bridge('test')
# def duplicate(data):
#     pass


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
