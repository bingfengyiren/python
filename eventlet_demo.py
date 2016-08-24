#-*-coding:utf-8-*-
'''
author:cuiming
date:2016/08/23
'''
import eventlet
import redis
from multiprocessing import Pool
redis = eventlet.import_patched("redis")

gpool = eventlet.GreenPool(10000)

def get_w2v():
    file = "vector.txt"
    lineIdx = 0
    w2v = {}
    t = 0
    for line in open(file, "r"):
        if lineIdx == 0 or lineIdx == 1:
            lineIdx += 1
            continue

        lst = line.split(" ")
        word = lst[0]
        vec = [float(x.strip("\n")) for x in lst[1:-1]]
        w2v[word] = vec
        t += 1
    return w2v

conn_pool = redis.ConnectionPool(max_connections=100, host="172.16._._", port=10531, db=5)
def mps(block):
    def f(word,vec):
        rds = redis.Redis(connection_pool=conn_pool)
        pl = rds.pipeline(transaction=False)
        for v in vec:
            pl.rpush(word,v)
        return pl.execute()

    pile = eventlet.GreenPile(gpool)
    for w_v in block:
        pile.spawn(f,w_v[0],w_v[1])

    for _ in pile:
        pass

def push_to_redis_p(w2v):
    pool = Pool(processes=12)
    size = 1000
    block = []
    total = len(w2v)
    idx = 0
    for word,vec in w2v.items():
        block.append([word,vec])
        idx += 1
        if len(block) >= size or idx == total - 1:
            pool.apply_async(mps,(block,))
            block = []
    pool.close()
    pool.join()

w2v = get_w2v()
push_to_redis_p(w2v)
