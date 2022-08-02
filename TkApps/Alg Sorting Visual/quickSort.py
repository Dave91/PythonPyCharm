import time


def partition(data, head, tail, draw_data, time_tick):
    border = head
    pivot = data[tail]

    draw_data(data, get_color_array(len(data), head, tail, border, border))
    time.sleep(time_tick)

    for j in range(head, tail):
        if data[j] < pivot:
            draw_data(data, get_color_array(len(data), head, tail, border, j, True))
            time.sleep(time_tick)

            data[border], data[j] = data[j], data[border]
            border += 1

        draw_data(data, get_color_array(len(data), head, tail, border, j))
        time.sleep(time_tick)

    # swap pivot with border value
    draw_data(data, get_color_array(len(data), head, tail, border, tail, True))
    time.sleep(time_tick)

    data[border], data[tail] = data[tail], data[border]

    return border


def quick_sort(data, head, tail, draw_data, time_tick):
    if head < tail:
        partition_id_x = partition(data, head, tail, draw_data, time_tick)

        # LEFT PARTITION
        quick_sort(data, head, partition_id_x - 1, draw_data, time_tick)

        # RIGHT PARTITION
        quick_sort(data, partition_id_x + 1, tail, draw_data, time_tick)


def get_color_array(data_len, head, tail, border, curr_id_x, is_swapping=False):
    color_array = []
    for i in range(data_len):
        # base coloring
        if head <= i <= tail:
            color_array.append('gray')
        else:
            color_array.append('white')

        if i == tail:
            color_array[i] = 'blue'
        elif i == border:
            color_array[i] = 'red'
        elif i == curr_id_x:
            color_array[i] = 'yellow'

        if is_swapping:
            if i == border or i == curr_id_x:
                color_array[i] = 'green'

    return color_array
