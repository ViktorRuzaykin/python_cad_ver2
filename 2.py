import parameters


def list_point_insert(chk_state_list, insert_point_start, distance_profile):
    chk_state_list = [i for i in chk_state_list if i == 1]
    x, y = insert_point_start[0], insert_point_start[1]
    result_point_start = [[x, y, 0]]
    len_state_chk_list = len(chk_state_list)

    def _for_append(len_list, new_x):
        for i in range(1, len_list):
            new_x += distance_profile + parameters.OFFSET_NEW_PROFILE + parameters.WIDTH_BASEMENT
            result_point_start.append([new_x, y, 0])

    if len_state_chk_list == 2:
        _for_append(len_state_chk_list, x)
    if len_state_chk_list == 3:
        _for_append(len_state_chk_list, x)
    if len_state_chk_list == 4:
        _for_append(len_state_chk_list, x)
    print(result_point_start)
    return result_point_start


chk = [1, 1, 0, 1]
in_point = [0, 0, 0]
d = 120
list_point_insert(chk, in_point, d)