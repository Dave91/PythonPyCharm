import time


def bubble_sort(data, draw_data, time_tick):
    for _ in range(len(data)-1):
        for j in range(len(data)-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                draw_data(data, ['green' if x == j or x == j + 1 else 'red' for x in range(len(data))])
                time.sleep(time_tick)
    draw_data(data, ['green' for x in range(len(data))])
