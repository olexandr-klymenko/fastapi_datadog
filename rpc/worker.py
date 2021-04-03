import json
import os

from redisrpc import RedisRPC


def calc_square(response):
    power_of_number = json.loads(response)["key"] ** 2
    return power_of_number  # sent to client


if __name__ == "__main__":
    rpc = RedisRPC(os.getenv("REDISRPC_CHANNEL"))
    rpc.register(calc_square, "rpc")
    rpc.listen()
