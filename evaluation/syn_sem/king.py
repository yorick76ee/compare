import multiprocessing
import os
import time

#models = ["hidden", "lbl", "senna"]
models = ["ivlblskip", "ivlblcbow"]

def func(msg, vec_dir, ret_dir):
    arg = './compute-accuracy-txt %s/%s 0 < questions-words.txt > %s/%s' % (vec_dir, msg, ret_dir, msg)
    print arg
    os.system(arg)


if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=16)

    for model in models:
        vec_dir = "vec_%s" % model
        ret_dir = "ret_king_%s" % model

        if not os.path.exists(ret_dir):
            os.makedirs(ret_dir)

        for lists in os.listdir(vec_dir):
            if not os.path.exists(os.path.join(ret_dir, lists)):
                x = lists.replace('.txt','').replace('.bz2','').split('_')
                #if int(x[-1]) != 1 and int(x[-1]) % 5 != 0:
                #   continue
                #if not "v50" in lists:
                #    continue
                print model, lists
                if int(x[-1]) > 10 and "10m" in lists and int(x[-1]) % 100 != 0:
                    continue
                if int(x[-1]) > 10 and "100m" in lists and int(x[-1]) % 10 != 0:
                    continue
                
                pool.apply_async(func, (lists, vec_dir, ret_dir, ))
    pool.close()
    pool.join()
    print "Sub-process(es) done."
    
    
