f = open("perms2.list", "w")

r1 = open("split1.list", "r")
r2 = open("split2.list", "r")

read1 = True
r1Empty = False
r2Empty = False
while(True):
    print "hit1"
    if(r1Empty and r2Empty):
        break;
    if read1:
        l = r1.readline()
        if(l!=''):
            f.write(l)
        else:
            r1Empty= True
        read1 = False
    else:
        l = r2.readline()
        if(l!=''):
            f.write(l)
        else:
            r2Empty = True
        read1 = True


f.close()
r1.close()
r2.close()
