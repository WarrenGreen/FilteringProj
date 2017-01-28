
f = open("perms2.list", "r")

w1 = open("split1.list", "w")
w2 = open("split2.list", "w")

write1 = True
for l in f:
    if write1:
        w1.write(l)
        write1 = False
    else:
        w2.write(l)
        write1 = True

f.close()
w1.close()
w2.close()
