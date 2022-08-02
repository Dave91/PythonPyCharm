import time


def merge_sort(data, draw_data, time_tick):
    merge_sort_alg(data, 0, len(data) - 1, draw_data, time_tick)


def merge_sort_alg(data, left, right, draw_data, time_tick):
    if left < right:
        middle = (left + right) // 2
        merge_sort_alg(data, left, middle, draw_data, time_tick)
        merge_sort_alg(data, middle+1, right, draw_data, time_tick)
        merge(data, left, middle, right, draw_data, time_tick)


def merge(data, left, middle, right, draw_data, time_tick):
    draw_data(data, get_color_array(len(data), left, middle, right))
    time.sleep(time_tick)

    left_part = data[left:middle+1]
    right_part = data[middle+1: right+1]

    left_id_x = right_id_x = 0

    for dataIdx in range(left, right+1):
        if left_id_x < len(left_part) and right_id_x < len(right_part):
            if left_part[left_id_x] <= right_part[right_id_x]:
                data[dataIdx] = left_part[left_id_x]
                left_id_x += 1
            else:
                data[dataIdx] = right_part[right_id_x]
                right_id_x += 1

        elif left_id_x < len(left_part):
            data[dataIdx] = left_part[left_id_x]
            left_id_x += 1
        else:
            data[dataIdx] = right_part[right_id_x]
            right_id_x += 1

    draw_data(data, ["green" if left <= x <= right else "white" for x in range(len(data))])
    time.sleep(time_tick)


def get_color_array(leght, left, middle, right):
    color_array = []

    for i in range(leght):
        if left <= i <= right:
            if left <= i <= middle:
                color_array.append("yellow")
            else:
                color_array.append("pink")
        else:
            color_array.append("white")

    return color_array
