def plotPoint(points: list, axis, marker=1, color1=2, color2=5):
    x = points[0]
    y = points[1]
    z = points[2]
    axis.scatter(x, y, z, marker=markerType(marker), color=colorType(color1))
    return


# _____________________________________________________________________________
def plotLine(prevCords, newCords, axis, line=0, marker=1, color1=2, color2=7):
    x_values = [prevCords[0], newCords[0]]
    y_values = [prevCords[1], newCords[1]]
    z_values = [prevCords[2], newCords[2]]

    axis.plot(x_values, y_values, z_values,
                 ls=lineType(line), marker=markerType(marker),
                 color=colorType(color1), markerfacecolor=colorType(color1))
    return


# _____________________________________________________________________________
def lineType(num):
    db = {0: "-",  # solid
          1: "--",  # dashed
          2: "-.",  # dashDot
          3: ":"}  # dotted

    total = len(db)

    if num < total:
        return db[num]
    else:
        try:
            return db[(total % num) - 1]
        except KeyError:
            return db[total - 1]


# _____________________________________________________________________________
def markerType(num):
    db = {0: ".",  # point
          1: "o",   #
          2: ",",  # pixel
          3: "v",  # triDown
          4: "^",  # triUp
          5: "<",  # triLeft
          6: ">",  # triRight
          7: "1",  # tri_Down
          8: "2",  # tri_Up
          9: "3",  # tri_Left
          10: "4",  # tri_Right
          11: "s",  # square
          12: "P",  # pentagon
          13: "*",  # star
          14: "h",  # hexagon1
          15: "H",  # hexagon2
          16: "+",  # plus
          17: "x",  # x
          18: "D",  # diamond
          19: "d",  # thinDiamond
          20: "|",  # vLine
          21: "_"}  # hLine

    total = len(db)
    if num < total:
        return db[num]
    else:
        try:
            return db[(total % num) - 1]
        except KeyError:
            return db[total - 1]


# _____________________________________________________________________________
def colorType(num):
    db = {0: "blue",
          1: "green",
          2: "red",
          3: "cyan",
          4: "magenta",
          5: "yellow",
          6: "black",
          7: "white"}

    total = len(db)
    if num < total:
        return db[num]
    else:
        try:
            return db[(total % num) - 1]
        except KeyError:
            return db[total - 1]


# _____________________________________________________________________________
def plotClose():
    return