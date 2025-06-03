from operator import index

from pandas.io.formats.info import frame_see_also_sub

import LD_CL_Calc as ldcalc
import numpy as np
import matplotlib.pyplot as plt

"""x_testlist = ldcalc.Calc_LD_M()[0]
y_testlist = ldcalc.Calc_LD_M()[1]

#x_testlist = [0, 1, 2, 3, 4, 5, 6]
#y_testlist = [0, 4, 6, 6, 5, None, None]"""


def validate_list(list): #returns length of list which is actually valid
    num_flag:bool = False
    none_flag:bool = False
    valid_flag:bool = False
    semi_valid_flag:bool = False
    invalid_flag:bool = False
    list_index = -1

    for wert in list:
        list_index = list_index + 1
        if wert == None:
            none_flag = True
            break
        else:
            num_flag = True

    if none_flag:
        if list_index + 1 >= len(list):
            valid_flag = False
            semi_valid_flag = True
        else:
            for n in range(list_index + 1, len(list), 1):
                if list[n] != None or num_flag == False:
                    valid_flag = False
                    semi_valid_flag = False
                else:
                    valid_flag = False
                    semi_valid_flag = True
    else:
        valid_flag = True

    if valid_flag:
        if len(list) > 0:
            print("LIST VALIDATION CHECK: Valid list.")
        else:
            print("LIST VALIDATION CHECK: Empty List.")
        return len(list)
    elif semi_valid_flag:
        print("LIST VALIDATION CHECK: Semi valid list. 'None' found at the end of list, starting with index: ", list_index)
        return list_index
    else:
        print("LIST VALIDATION CHECK: Invalid list. 'None' found inbetween numbers!")
        return list_index

def get_k_d(x0, y0, x1, y1):
    k = (y1 - y0)/(x1 - x0)
    d = y1 - x1 * k
    return k, d

def find_boundary_x(x_list, list_length, x):
    x_low = 0
    x_high = 0
    list_pos = 0

    x_list_len = list_length

    if x < x_list[0] or x > x_list[x_list_len - 1]:
        x_low = None
        x_high = None
        list_pos = None

    for i in range (0, x_list_len - 1, 1):
        if x >= x_list[i] and x <= x_list[i+1]:
            x_low = x_list[i]
            x_high = x_list[i+1]
            list_pos = i
            break

    return list_pos, x_low, x_high

def calc_k_d_values_for_list(x_list, y_list):
    x_list_length = len(x_list)
    y_list_length = len(y_list)
    max_list_length = x_list_length

    if y_list_length > x_list_length:
        max_list_length = y_list_length

    k_list = []
    d_list = []

    for i in range(0, max_list_length-1, 1):
            k_list.append(get_k_d(x_list[i], y_list[i], x_list[i + 1], y_list[i + 1])[0])
            d_list.append(get_k_d(x_list[i], y_list[i], x_list[i + 1], y_list[i + 1])[1])

    return k_list, d_list

def interpolator(x_list, y_list, x):
    valid_x_list_length = validate_list(x_list)
    valid_y_list_length = validate_list(y_list)
    max_list_length = valid_x_list_length

    if valid_x_list_length == 0:
        return print("INTERPOLATOR MSG: Invalid x-List!")
    elif valid_y_list_length == 0:
        return print("INTERPOLATOR MSG: Invalid y-List!")

    if valid_y_list_length > valid_x_list_length:
        max_list_length = valid_y_list_length

    if x > x_list[valid_x_list_length - 1]:
        print("INTERPOLATOR MSG: x-value greater than greatest x-list-value!")
        return None
    elif x < x_list[0]:
        print("INTERPOLATOR MSG: x-value smaller than smallest x-list-value!")
        return None

    x_low_index = find_boundary_x(x_list, max_list_length, x)[0]
    k = get_k_d(x_list[x_low_index], y_list[x_low_index], x_list[x_low_index + 1], y_list[x_low_index + 1])[0]
    d = get_k_d(x_list[x_low_index], y_list[x_low_index], x_list[x_low_index + 1], y_list[x_low_index + 1])[1]
    y = k * x + d

    return y

"""print("\nInput xlist: ", x_testlist)
print("\nInput ylist: ", y_testlist)

#print("Valid x-list length: ", validate_list(x_testlist))
#print("Valid y-list length: ", validate_list(y_testlist))

x = np.array(x_testlist)
y = np.array(y_testlist)
plt.plot(x,y)
xtest = 0.616
ytest = interpolator(x_testlist, y_testlist, xtest)
plt.scatter(xtest, ytest, color="red")
plt.show()"""