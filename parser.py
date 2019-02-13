with open("fedpapers.txt", "r") as f:
    tmp = []
    i = 1
    for line in f:
        if "FEDERALIST" not in line:
            tmp.append(line)
        else:
            new_file = open('%d.txt' %i, 'w')
            new_file.write(''.join(tmp))
            new_file.close()
            i += 1
            tmp = []
