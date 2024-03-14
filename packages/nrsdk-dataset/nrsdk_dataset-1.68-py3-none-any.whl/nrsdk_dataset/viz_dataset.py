import datetime
import os

import matplotlib.pyplot as plt

from nrsdk_dataset import get_file_list, set_path, get_pkg_span, check_is_file1, get_data_path
from matplotlib import colormaps


def viz_dataset(animal,
                start_time=datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc),
                end_time=datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)):
    path_out = get_data_path('out')

    def init_layout(start_time, time_d, pc_names):
        total_days = max(time_d) - min(time_d)
        plt.figure(figsize=(12, max([total_days / 5, 2])))

        plt.yticks(range(min(time_d), max(time_d) + 1), minor=True)
        plt.yticks(range(min(time_d), max(time_d) + 1, 3),
                   [(start_time + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in
                    range(min(time_d), max(time_d) + 1, 3)])

        plt.grid(which="major")
        plt.grid(which="minor")
        num_xtick = 6
        plt.xticks(range(0, 60 * 24, int((24 / (num_xtick)) * 60)),
                   [f'{str((start_time + datetime.timedelta(hours=i * (24 / (num_xtick)))).hour)}:00' for i in
                    range(num_xtick)])
        plt.ylim([min(time_d) - 1, max(time_d) + 1])
        plt.xlim([0, 60 * 24])
        plt.gca().invert_yaxis()

        for i in range(len(pc_names)):
            plt.broken_barh([(0, 10)], (-5 - i - 0.3, 0.6), facecolors=colormap[i], label=pc_names[i])

        plt.legend(title='PC name', framealpha=0.5, bbox_to_anchor=(1.02, 0), loc=3, borderaxespad=0)

    # %%
    def plot_blocks(time_d, time_min, duration_min, pc_names):
        unique_pc_names = list(set(pc_names))
        init_layout(start_time,
                    time_d,
                    unique_pc_names)
        for i in range(len(time_min)):
            plt.broken_barh([(time_min[i], duration_min[i])], (time_d[i] - 0.4, 0.8),
                            facecolors=colormap[unique_pc_names.index(pc_names[i])], zorder=10)
        total_days = max(time_d) - min(time_d)
        plt.title(f'{total_days:d} days: in total')

        fig_name = f'{(start_time + datetime.timedelta(days=min(time_d))).strftime("%Y%m%d")}-{(start_time + datetime.timedelta(days=max(time_d))).strftime("%Y%m%d")}.png'
        plt.savefig(os.path.join(set_path(os.path.join(path_out, animal, 'dataset_viz')), fig_name))

    if start_time.hour != 7:
        start_time = start_time + datetime.timedelta(hours=7)

    file_list = get_file_list(animal,
                              start_time=start_time,
                              end_time=end_time
                              )
    pc_names = list(set([file.split('\\Backup\\')[1].split('\\')[0] for file in file_list]))
    colormap = colormaps.get_cmap('tab10').colors

    time_d = []
    time_min = []
    duration_min = []
    pc_names = []

    for file in file_list:

        if check_is_file1(file):
            start_time_pkg, end_time_pkg = get_pkg_span(file, file_list)
        else:
            continue

        time_from_start_time = (start_time_pkg - start_time).days * 24 * 60 * 60 + (
                start_time_pkg - start_time).seconds
        time_duration_sec = (end_time_pkg - start_time_pkg).total_seconds()

        # when data started before spanning of interest
        if start_time_pkg < start_time:
            time_duration_sec = time_duration_sec + time_from_start_time
            time_from_start_time = 0
            if time_duration_sec < 0:
                continue

        # add data segments
        time_d.append(int(time_from_start_time / (3600 * 24)))
        time_min.append(int((time_from_start_time - time_d[-1] * 3600 * 24) / 60))
        duration_min.append(int(time_duration_sec / 60))
        pc_names.append(file.split('\\Backup\\')[1].split('\\')[0])

        # if data interval > 5 days
        if len(time_d) > 3:
            if time_d[-1] - time_d[-2] > 3:
                plot_blocks(time_d[:-1], time_min[:-1], duration_min[:-1], pc_names[:-1])
                time_d = time_d[-1:]
                time_min = time_min[-1:]
                duration_min = duration_min[-1:]
                pc_names = pc_names[-1:]

        # when data spanned 7:00
        if time_min[-1] + duration_min[-1] > 60 * 24:
            time_d.append(time_d[-1] + 1)
            time_min.append(0)
            duration_min.append(time_min[-2] + duration_min[-1] - 60 * 24)
            duration_min[-2] = 60 * 24 - time_min[-2]
            pc_names.append(pc_names[-1])

    plot_blocks(time_d, time_min, duration_min, pc_names)
