
# On PPM and PGM formats see http://paulbourke.net/dataformats/ppm/
# On convolution operation see https://youtu.be/KiftWz544_8
# To view .pgm and .ppm files, you can use IrfanView, see https://www.irfanview.com/
# To check whether your outputs are the same as ours, you can use the same techniques as in Homework 2, or you can write your own code.

filename = input()
operation = int(input())


def img_printer(img):
    row = len(img)
    col = len(img[0])
    cha = len(img[0][0])
    for i in range(row):
        for j in range(col):
            for k in range(cha):
                print(img[i][j][k], end=" ")
            print("\t|", end=" ")
        print()


# DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE
def img_list(fname):
    fh = open(fname,"r")
    file_type = fh.readline()
    dimensions = fh.readline().split()
    resolution = fh.readline()
    row_n,col_n = int(dimensions[1]),int(dimensions[0])
    remaining = fh.read().strip().split()
    fh.close()
    if file_type.strip() == "P3":
        nested_img_list = [[[0,0,0] for i in range(col_n)] for j in range(row_n)]
        next = 0
        for r in range(row_n):
            for c in range(col_n):
                for p in range(3):
                    nested_img_list[r][c][p] = int(remaining[next])
                    next += 1
    elif file_type.strip() == "P2":
        nested_img_list = [[0 for i in range(col_n)] for j in range(row_n)]
        next = 0
        for r in range(row_n):
            for c in range(col_n):
                nested_img_list[r][c] =int(remaining[next])
                next += 1
    return nested_img_list

img = img_list(filename)
r_n,c_n = len(img),len(img[0])

checked = [[False for temp1 in range(c_n)]for temp2 in range(r_n)]
applied = [[False for temp1 in range(c_n)]for temp2 in range(r_n)]
#functions for operation 1
def rec_average_finder(img,row_i,col_i):
    global checked
    if (0>row_i or row_i>=len(img)) or (0>col_i or col_i>=len(img[0])): return [0,0]
    if img[row_i][col_i] == 0 or checked[row_i][col_i] == True: return [0,0]
    checked[row_i][col_i] = True
    neighs = [[-1,0],[0,-1],[+1,0],[0,+1]]
    number = 1
    total = img[row_i][col_i]
    for neigh in neighs:
        rec_lst = rec_average_finder(img,row_i+neigh[0],col_i+neigh[1])
        if not rec_lst == [0, 0]:
            total += rec_lst[0]
            number += rec_lst[1]
    return [total,number,total//number]

def apply_average_finder(img):
    global checked
    soln_lst = []
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i][j] == 0 or checked[i][j] == True: continue
            average = rec_average_finder(img,i,j)[2]
            soln_lst.append(average)
    return soln_lst

def rec_average_placer(img,row_i,col_i,average):
    global applied
    global colored_img
    if (0>row_i or row_i>=len(img)) or (0>col_i or col_i>=len(img[0])): return
    if img[row_i][col_i] == 0 or applied[row_i][col_i] == True: return
    applied[row_i][col_i] = True
    neighs = [[-1,0],[0,-1],[+1,0],[0,+1]]
    for neigh in neighs:
        rec_average_placer(img,row_i+neigh[0],col_i+neigh[1],average)
        colored_img[row_i][col_i] = average

if operation == 1:
    colored_img = [[0 for i in range(c_n)] for j in range(r_n)]
    average_lst = apply_average_finder(img)
    next_average = 0
    for r in range(r_n):
        for c in range(c_n):
            if img[r][c] == 0 or applied[r][c] == True:
                continue
            rec_average_placer(img,r,c,average_lst[next_average])
            next_average += 1
    colored_img = [[[i1] for i1 in rows] for rows in colored_img]
    img_printer(colored_img)

elif operation == 2:
    filter_name = input()
    stride = int(input())
    filter_h = open(filter_name,"r")
    filter_content = filter_h.read().split()
    f_len = int(len(filter_content)**(1/2))
    filter_lst = [[0 for temp5 in range(f_len)] for temp6 in range(f_len)]
    next_f = 0
    for i in range(f_len):
        for j in range(f_len):
            filter_lst[i][j] = float(filter_content[next_f])
            next_f += 1
    filtered_img = [[[0, 0, 0] for temp7 in range((c_n-f_len+1)//stride)] for temp8 in range((r_n-f_len+1)//stride)]
    # functions for operation 2
    #print(len(filtered_img),len(filtered_img[0]))
    def rec_convolution(img, filter, stride, row_i=0, col_i=0):
        global filtered_img
        fil_len = len(filter)
        row_len = len(img)
        col_len = len(img[0])
        if col_i + fil_len > col_len: return -1
        if row_i + fil_len > row_len: return
        pixels = [0, 1, 2]
        neighs = []
        for r_i in range(fil_len):
            for c_i in range(fil_len):
                neighs.append([r_i, c_i])
        new_pixel = []
        for pixel in pixels:
            total = 0
            for neigh in neighs:
                total += filter[neigh[0]][neigh[1]] * img[row_i + neigh[0]][col_i + neigh[1]][pixel]
            if total < 0:
                total = 0
            elif total > 255:
                total = 255
            new_pixel.append(int(total))
        filtered_img[row_i // stride][col_i // stride] = new_pixel
        rem_problem = rec_convolution(img,filter,stride,row_i,col_i+stride)
        if rem_problem == -1:
            rec_convolution(img, filter, stride, row_i+stride, 0)

    rec_convolution(img, filter_lst, stride, 0, 0)
    img_printer(filtered_img)
# DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE

