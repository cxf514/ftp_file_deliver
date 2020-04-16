"""
    ftp 文件传输客户端
"""
from socket import socket
import sys
import os

ADDR = ("127.0.0.1", 8890)
book_list = []
book_code = []
dir = "/level2/文件传输/ftp文件传输client"
my_file = os.listdir(dir)
# 获取txt文件
for i in my_file:
    if ".txt" not in i:
        my_file.remove(i)


def fun(s):
    while True:
        choose = int(input("\n输入1 查看书籍列表\n输入2 下载书籍"
                           "\n输入3 上传书籍\n输入4 退出\n\n"))
        if choose == 1:
            choose_1(s)
        elif choose == 2:
            choose_2(s)
        elif choose == 3:
            choose_3(s)


def choose_1(s):
    global book_list, book_code
    msg = f"C 1"
    s.send(msg.encode())
    data = s.recv(1024)
    book_list = data.decode().split("$%$")
    print("书单")
    a = 1
    for i in book_list:
        book_code.append(a)
        print(f"{a}:{i}")
        a += 1


def choose_2(s):
    while True:
        code = int(input("输入需要下载的图书编号"))
        print(book_code)
        if code in book_code:
            msg = f"C 2 {code}"
            s.send(msg.encode())
            data = s.recv(1024)
            f = open(f"{book_list[code]}", "wb")
            f.write(data)
            f.close()
            break


def choose_3(s):
    a = 1
    for i in my_file:
        print(f"{a}:{i}")
        a += 1
    while True:
        num = int(input("输入想要上传的文件编号"))
        if num in range(1, len(my_file) + 1):
            msg = f"C 3 {my_file[num - 1]}"
            s.send(msg.encode())
            data = s.recv(1024)
            if data.decode() == "ok":
                f = open(f"{my_file[num-1]}", "rb")
                while True:
                    msg = f.read(1024)
                    if msg:
                        s.send(msg)
                    else:
                        break
                f.close()
                break


def login(s):
    while True:
        try:
            usr = input("输入您的账号")
            code = input("输入您的密码")
            msg = f"L {usr}:{code}"
        except:
            msg = "quit"
        if msg != "quit":
            s.send(msg.encode())
            reply = s.recv(100).decode()
            if reply == "pass":
                return reply
            else:
                print(reply)
        else:
            sys.exit("客户端退出")


def main():
    s = socket()
    s.connect(ADDR)
    if login(s) == "pass":
        fun(s)


if __name__ == "__main__":
    main()
