'''
Copyright (c) 2024 by HIL Group
Author: notmmao@gmail.com
Date: 2024-01-08 14:54:04
LastEditors: notmmao@gmail.com
LastEditTime: 2024-03-03 14:26:13
Description: gp-bench-agent的入口文件

==========  =============  ================
When        Who            What and why
==========  =============  ================
2024-01-08  notmmao        Created
2024-01-09  notmmao        add: logger, git.needs_pull
==========  =============  ================
'''
import os
import sys
import argparse
import uvicorn
from loguru import logger
from .server import Agent


def main():
    parser = argparse.ArgumentParser("bench_agent")
    parser.add_argument("-p", "--port", type=int, default=8000)
    parser.add_argument("-i", "--ip", default="127.0.0.1")
    parser.add_argument("-u", "--update", action="store_true")
    parser.add_argument("-l", "--logger", action="store_true")
    args = parser.parse_args()
    if args.logger:
        logger.enable("gp.bench")

    ip, port = args.ip, args.port
    server = Agent()
    uvicorn.run(server.app, host=ip, port=port)


if __name__ == '__main__':
    main()
