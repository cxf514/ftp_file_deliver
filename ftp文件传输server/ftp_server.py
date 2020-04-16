"""
    文件传输ftp服务器
"""
from socket import socket
from multiprocessing import Process
from signal import *
import os
import sys

ADDR = ("127.0.0.1", 8890)
usr = {"cxf": "67111630"}
dir = "/level2/文件传输/ftp文件传输server"
book_list = os.listdir(dir)
# 获取txt文件
for i in book_list:
    if ".txt" not in i:
        book_list.remove(i)


def identify(ls, require):
    name = require[1].split(":")[0]
    code = require[1].split(":")[1]
    for i in usr:
        if i == name and usr[i] == code:
            ls.send(b"pass")
        elif i != name:
            ls.send("账号不存在".encode())
        elif i == name and usr[i] != code:
            ls.send("密码错误".encode())


def deliver_book_list(ls):
    msg = "$%$".join(book_list)
    ls.send(msg.encode())


def download(ls, code):
    f = open(dir + "/" + book_list[int(code)], "rb")
    while True:
        msg = f.read(1024)
        if msg:
            ls.send(msg)
        else:
            break


def upload(ls, file):
    if file not in book_list:
        book_list.append(file)
        ls.send(b"ok")
        data = ls.recv(1024)
        f = open(file, "wb")
        f.write(data)
        f.close()


def function(ls):
    while True:
        data = ls.recv(50)
        require = data.decode().split(" ", 1)
        if require[0] == "L":
            identify(ls, require)
        elif require[0] == "C":
            if require[1] == "1":
                deliver_book_list(ls)
            elif require[1].split(" ")[0] == "2":
                download(ls, require[1].split(" ")[1])
            elif require[1].split(" ")[0] == "3":
                upload(ls, require[1].split(" ")[1])


def main():
    s = socket()
    s.bind(ADDR)
    s.listen(10)
    # 处理僵尸进程
    signal(SIGCHLD, SIG_IGN)

    print("Listen the port 8888")

    # 客户端连接
    while True:
        try:
            ls, address = s.accept()
            print(f"连接了{address[0]}客户端")
        except:
            sys.exit(f"服务断开")
        p = Process(target=function, args=(ls,))
        p.daemon = True
        p.start()


if __name__ == "__main__":
    main()
