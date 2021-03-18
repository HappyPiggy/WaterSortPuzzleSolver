# coding=utf-8


class StepItem(object):
    def __init__(self, ori_glass, tar_glass):
        self.original_glass = ori_glass
        self.target_glass = tar_glass

    def can_pour_in_out(self):
        if self.original_glass.can_pour_out():
            out_color = self.original_glass.get_color_by_index()
            if self.target_glass.can_pour_in(out_color.id) and self.target_glass.empty_count >= out_color.count:
                if self.original_glass.is_single_color() and self.target_glass.is_empty():
                    return False
                else:
                    return True
        return False

    def __repr__(self):
        return '{0} into {1}'.format(self.original_glass.id, self.target_glass.id)

    def evaluate(self, grass_list):
        score = 0
        colors = self.original_glass.get_colors()
        for idx, c in enumerate(colors.get_all()):
            for g in grass_list:
                if self.original_glass.id == g.id:
                    continue
                #  当前颜色所处层 的分数
                color_index = self.original_glass.max_count - 1 - idx
                score += (pow(2, color_index) * c.count * color_index)

                #  目标颜色所处层 的分数
                target_index = g.get_index_by_color_id(c.id)
                score += pow(2, g.max_count - 1 - target_index)

                score += idx

        target_color = self.target_glass.get_color_by_index()
        out_color = self.original_glass.get_color_by_index()

        target_count = target_color.count if target_color else 0
        out_count = out_color.count if out_color else 0
        if target_count + out_count == self.target_glass.max_count:
            score += 10

        return score


def get_steps_rank(grass_list):
    from main import SHOW_DETAIL_LOG

    steps = list()
    for g1 in grass_list:
        is_empty = False
        for g2 in grass_list:
            if g1.id == g2.id or g1.is_complete() or g2.is_complete():
                continue
            if is_empty and g2.is_empty():
                continue
            if g2.is_empty():
                is_empty = True

            step = StepItem(g1, g2)
            if step.can_pour_in_out():
                steps.append(step)

    ordered_steps = dict()
    for s in steps:
        score = s.evaluate(grass_list)
        ordered_steps[s] = score
    #     if SHOW_DETAIL_LOG:
    #         print '{0} into {1}, score:{2}'.format(s.original_glass.id, s.target_glass.id, score)
    # if SHOW_DETAIL_LOG:
    #     print '-'*30

    step_rank = sorted(ordered_steps.items(), key=lambda item: -item[1])
    from Utils import Stack
    step_stack = Stack()
    for s in step_rank:
        step_stack.push(s[0])

    return step_stack

