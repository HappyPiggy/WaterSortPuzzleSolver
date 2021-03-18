import copy


class SnapShot(object):
    def __init__(self, ori_id, ori_data, target_id, target_data):
        self.original_id = ori_id
        self.original_data = copy.deepcopy(ori_data)
        self.target_id = target_id
        self.target_data = copy.deepcopy(target_data)
