# -*- coding:utf-8 -*-
def submit(result, testfile, output):
    f = open(testfile)
    r = open(result)
    o = open(output, "w")
    l1 = f.readline()
    print >> o, "id,click"
    while True:
        l1 = f.readline()
        l2 = r.readline().strip()
        if not l1:
            break
        print >> o, l1.split(',')[0] + "," + l2
    f.close()
    r.close()
    o.close()


submit("../fm_test_result", "../test", "../submission")
