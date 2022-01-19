import datetime
import json
import os


def generate_plan(target_list: list, day_hours_list: list) -> dict:
    """

    :param target_list: 任务列表
    :param day_hours_list: 每日小时列表：代表每天有效的小时数
    """
    plan_dict = {}
    for target in target_list:
        cost_time = target['cost_time']
        target_name = target['target_name']
        if not day_hours_list:
            break
        while cost_time > 0 and day_hours_list:
            day, hours = day_hours_list[0]
            if day not in plan_dict:
                plan_dict[day] = []
            if hours > cost_time:
                day_hours_list[0] = day_hours_list[0][0], hours - cost_time
                cost_time = 0
            elif hours == cost_time:
                day_hours_list = day_hours_list[1:]
                cost_time = 0
            else:
                day_hours_list = day_hours_list[1:]
                cost_time = cost_time - hours
            plan_dict[day].append(target_name)

    return plan_dict


def generate_day_hours_list(
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        day_hours: float) -> list:
    """
    生成每日时间安排
    :param start_time:
    :param end_time:
    :param day_hours:
    :return:
    """
    day_hours_list = []
    while start_time <= end_time:
        # 周末时间翻倍
        day_hours_list.append((
            start_time.strftime('%Y年%m月%d日'),
            day_hours if start_time.weekday() < 6 else day_hours * 2
        ))
        start_time += datetime.timedelta(days=1)
    return day_hours_list


def generate_lc_target_list(tag_map_file):
    """
    生成lc目标列表
    :param tag_map_file:
    """
    lc_target_list = []
    with open(tag_map_file, 'r') as f:
        tag_map = dict(json.loads(f.read()))
    exists_problems = set()
    for tag, problems in tag_map.items():
        for problem in problems:
            if problem['name'] not in exists_problems:
            #     lc_target_list.append({'target_name': problem, 'cost_time': 0.5})
            # else:
                lc_target_list.append({'target_name': problem, 'cost_time': 0.75})
                exists_problems.add(problem['name'])
    return lc_target_list


def generate_xm_target_list(xm_file_path):
    """
    生成XMind目标列表
    :param xm_file_path:
    :return:
    """
    xm_target_list = []
    files = os.listdir(xm_file_path)
    for file in files:
        if not os.path.isdir(file):
            xm_target_list.append({'target_name': file, 'cost_time': 6})
    return xm_target_list


if __name__ == '__main__':

    s_time = datetime.datetime(year=2021, month=6, day=22)
    e_time = datetime.datetime(year=2021, month=9, day=30)
    day_hours_array_1 = generate_day_hours_list(s_time, e_time, 2)
    day_hours_array_2 = generate_day_hours_list(s_time, e_time, 1.5)

    day_arrange_list = []

    day_arrange_dict_1 = generate_plan(generate_lc_target_list('tag_map'), day_hours_array_1)
    day_arrange_dict_2 = generate_plan(generate_xm_target_list('D:\program\knowledge_hierarchy'), day_hours_array_2)
    day_arrange_dict = {}
    for day, arranges in day_arrange_dict_1.items():
        day_arrange_dict[day] = arranges + day_arrange_dict_2.get(day, [])

    with open('day_arrange', 'w') as f:
        for day, arranges in day_arrange_dict.items():
            f.write(day + ': ' + str(arranges) + '\n')


