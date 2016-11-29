import multiprocessing
import pickle
from p17_nest_gateway import NestProcess

p00_queue = multiprocessing.Queue(-1)
p17_queue = multiprocessing.Queue(-1)
p17 = NestProcess(name="p17_nest_gateway", msgin=p17_queue, msgout=p00_queue)

pickle.dumps(p17)