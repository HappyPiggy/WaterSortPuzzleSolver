# coding=utf-8
from Utils import Stack
from Color import Color
from Glass import Glass, GLASS_MAX_SIZE
from solver import get_steps_rank
from SnapShot import SnapShot
import time

SHOW_DETAIL_LOG = False


def check_win(glass_list):
    is_win = True
    for glass in glass_list:
        if glass.is_empty() or glass.is_complete():
            continue
        is_win = False
        break
    return is_win


def glass_pour_to(original_glass_id, target_glass_id):
    global glass_dict
    original_glass = glass_dict[original_glass_id]
    target_glass = glass_dict[target_glass_id]

    global history
    pour_color = original_glass.get_color_by_index()
    if pour_color is not None:
        pour_in_count = min(target_glass.empty_count, pour_color.count)
        snap = make_snap_shot(original_glass, target_glass)
        in_success = target_glass.pour_in(pour_color.id, pour_color.count)
        if in_success:
            original_glass.pour_out(pour_in_count)
            if SHOW_DETAIL_LOG:
                print '{0} into {1}'.format(original_glass.id, target_glass.id)
            history.push(snap)
            return True
    return False


def check_glass_valid(glass_list):
    color_dict = dict()
    for g in glass_list:
        for c in g.get_colors().get_all():
            if c.id not in color_dict.keys():
                color_dict[c.id] = 0
            color_dict[c.id] += c.count
    for key in color_dict.keys():
        count = color_dict[key]
        if count != GLASS_MAX_SIZE:
            print 'color_id:{0} count={1} is valid'.format(key, count)
            return False
    return True


def revert():
    global history
    if history.size <= 0:
        return
    snap = history.pop()
    if SHOW_DETAIL_LOG:
        print 'revert glass{0} into glass{1}'.format(snap.original_data.id, snap.target_data.id)

    global glass_dict
    glass_dict[snap.original_id] = snap.original_data
    glass_dict[snap.target_id] = snap.target_data


def make_snap_shot(ori_glass, tar_glass):
    snap = SnapShot(
        ori_glass.id, ori_glass,
        tar_glass.id, tar_glass
    )
    return snap


def search_steps():
    global glass_dict
    steps_rank = get_steps_rank(glass_dict.values())
    if steps_rank.is_empty():
        return False
    step_stack = Stack()
    step_stack.push(steps_rank)

    total_bit = step_stack.stack[0].size
    old_bit = -1
    while not step_stack.is_empty():
        count = ''
        new_bit = step_stack.stack[0].size
        if new_bit != old_bit:
            old_bit = new_bit
            print 'calculating... {:.2f}%'.format(100.0 * (total_bit - new_bit) / total_bit)

        cur_steps = step_stack.get_top()
        if cur_steps.is_empty():
            step_stack.pop()
            revert()

        while not cur_steps.is_empty():
            step = cur_steps.pop()
            pour_res = glass_pour_to(step.original_glass.id, step.target_glass.id)
            if not pour_res:
                print 'pour fail', step.original_glass.id, step.target_glass.id
                return False

            if check_win(glass_dict.values()):
                return True

            steps_rank = get_steps_rank(glass_dict.values())
            if not steps_rank.is_empty():
                step_stack.push(steps_rank)
                break
            else:
                revert()
            if cur_steps.is_empty():
                step_stack.pop()
                revert()

    return False


glass_dict = dict()
history = Stack()


def create_glass(colors):
    global glass_dict
    glass = Glass()
    glass.set_colors(Stack(colors))
    glass_dict[glass.id] = glass


if __name__ == '__main__':
    create_glass([Color(1, 2), Color(2), Color(3)])
    create_glass([Color(4), Color(5), Color(6), Color(7)])
    create_glass([Color(8), Color(9), Color(7), Color(10)])
    create_glass([Color(10), Color(9), Color(6), Color(10)])
    create_glass([Color(3), Color(11), Color(9), Color(2)])
    create_glass([Color(2), Color(8), Color(2), Color(11)])
    create_glass([Color(12), Color(9), Color(7), Color(8)])
    create_glass([Color(12), Color(6), Color(7), Color(12)])
    create_glass([Color(3), Color(1), Color(4), Color(5)])
    create_glass([Color(5), Color(4), Color(11), Color(8)])
    create_glass([Color(3), Color(12), Color(11), Color(4)])
    create_glass([Color(10), Color(6), Color(1), Color(5)])

    create_glass([])
    create_glass([])

    valid = check_glass_valid(glass_dict.values())
    if valid:
        start = time.clock()
        is_all_complete = search_steps()
        end = time.clock()

        cost = end - start
        print '\nall complete:{0}, step:{1}, cost_time:{2} sec'.format(is_all_complete, history.size, cost)
        for s in history.stack:
            print '{0} to {1}'.format(s.original_id, s.target_id)

        for g in glass_dict.values():
            g.show()





