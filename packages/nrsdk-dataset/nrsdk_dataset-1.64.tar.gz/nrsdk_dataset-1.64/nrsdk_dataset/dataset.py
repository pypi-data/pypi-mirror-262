import datetime
import glob

import mne
import fnmatch

import os
import tkinter as tk

nrsdk_dataset_path = {
    'in': None,
    'out': None
}


def get_subjects():
    print(os.path.join(get_data_path('in'), '**', 'app_record'))
    path_list = glob.glob(os.path.join(get_data_path('in'), '**', 'app_record'), recursive=True)
    subjects = []
    for path in path_list:
        subjects += os.listdir(path)

    subjects = [subject.rsplit('_', 1)[0] for subject in subjects if fnmatch.fnmatch(subject, '*_2???????????')]
    subjects = list(set(subjects))
    return subjects


def get_pkg_span(file, file_list, check_in_hdr_for_file1=False):
    file_pkg_subset = get_file_pkg_subset(file, file_list)
    file_start = get_file_dt(file_pkg_subset[0], check_in_hdr_for_file1=check_in_hdr_for_file1)
    try:
        file_end = get_file_dt(file_pkg_subset[-1], check_in_hdr_for_file1=True, return_dt_end=True)[-1]
    except ValueError as e1:
        if 'invalid literal' in e1.args[0]:
            file_end = get_file_dt(file_pkg_subset[-2], check_in_hdr_for_file1=True, return_dt_end=True)[-1]
        else:
            raise e1

    return file_start, file_end


def get_file_pkg_subset(file, file_list):
    file_name_time = get_file_time_str(file)
    file_pkg_subset = [file1 for file1 in file_list if file_name_time == get_file_time_str(file1)]
    return file_pkg_subset


def get_file_dt(file, check_in_hdr_for_file1=True, return_dt_end=False):
    file_name_time = get_file_time_str(file)
    file_dt = datetime.datetime.strptime(file_name_time, "%Y%m%d%H%M%S").replace(tzinfo=datetime.timezone.utc)
    if check_in_hdr_for_file1:
        raw = mne.io.read_raw_edf(file)
        file_dt = raw.annotations.orig_time.replace(tzinfo=datetime.timezone.utc)
        if return_dt_end:
            return file_dt, file_dt + datetime.timedelta(seconds=raw.times[-1])

    return file_dt


def get_file_pkg_id(file):
    return int(file.split('_')[-1].split('.')[0])


def get_file_time_str(file):
    return os.path.basename(file).split('_')[0]


def check_is_file1(file_name):
    return get_file_pkg_id(file_name) == 1


def get_file_list(animal,
                  start_time=datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc),
                  end_time=datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)):
    path_raw = get_data_path('in'),
    path = os.path.join(path_raw, animal + '*')
    file_list = glob.glob(os.path.join(path, '**', '*_*.edf'), recursive=True)
    file_list.sort(key=lambda x: (get_file_time_str(x), get_file_pkg_id(x)))

    idx_start = 0
    idx_end = 0
    for idx_file, file in enumerate(file_list):
        file_dt = get_file_dt(file, check_in_hdr_for_file1=False)
        if (file_dt <= start_time) & check_is_file1(file):
            idx_start = idx_file
        if file_dt <= end_time:
            idx_end = idx_file

    file_list = file_list[idx_start:idx_end + 1]

    return file_list


def set_path(path=None):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def set_data_path(in_or_out, path=None):
    if path:
        if not os.path.exists(path):
            if in_or_out == 'in':
                assert f"Could not find dataset path: {path}"
            else:
                os.makedirs(path)
    else:
        root = tk.Tk()
        root.withdraw()
        path = tk.filedialog.askdirectory()

    nrsdk_dataset_path[in_or_out] = path

    return path


def get_data_path(in_or_out):
    if not nrsdk_dataset_path[in_or_out]:
        set_data_path(in_or_out)

    return nrsdk_dataset_path[in_or_out]
