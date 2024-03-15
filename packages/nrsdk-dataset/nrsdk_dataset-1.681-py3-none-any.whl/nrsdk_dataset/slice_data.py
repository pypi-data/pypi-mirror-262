import datetime

import mne
import numpy as np

import os
import time

from nrsdk_dataset import get_file_list, check_is_file1, set_path, get_data_path


def acc_to_locomotion(acc):
    loco = np.std(np.concatenate([np.zeros((3, 1)), np.diff(acc)], axis=1), axis=0).reshape(1, -1)
    return loco


def reorder_channel_types(raw, montage='standard_1020'):
    chan_order = mne.channels.make_standard_montage(montage).ch_names
    chan_eeg = [raw.ch_names[i] for i in mne.pick_types(raw.info, eeg=True).astype('int')]
    chan_emg = [raw.ch_names[i] for i in mne.pick_types(raw.info, emg=True).astype('int')]
    chan_eog = [raw.ch_names[i] for i in mne.pick_types(raw.info, eog=True).astype('int')]
    chan_ecg = [raw.ch_names[i] for i in mne.pick_types(raw.info, ecg=True).astype('int')]
    chan_bio = [raw.ch_names[i] for i in mne.pick_types(raw.info, bio=True).astype('int')]
    chan_eeg = [chan for chan in chan_order if chan in chan_eeg]
    chan_order = chan_eeg + chan_emg + chan_eog + chan_ecg + chan_bio
    raw.reorder_channels(chan_order)
    return raw


def slice_data_within_circadian(date, animal, **kwargs):

    start_time = date.replace(hour=7, minute=0, second=0)
    end_time = start_time + datetime.timedelta(days=1)
    raw = slice_data_within(start_time, end_time, animal, **kwargs)

    return raw


def slice_data_within(start_time, end_time, animal,
                      bipolar_ref_arg=None, sf=None, resample=False):
    T0 = time.time()

    path_in = get_data_path('in')
    path_out = get_data_path('out')

    file_list = get_file_list(animal, start_time=start_time, end_time=end_time)

    assert file_list, "No data in selected duration! "

    raw_list = []
    for file in file_list:
        try:
            raw = mne.io.read_raw_edf(file, preload=False, units='uV', infer_types=True, verbose=False)
        except ValueError as e1:
            if 'invalid literal' in e1.args[0]:
                continue
            raise e1

        start_time_file = raw.annotations.orig_time
        end_time_file = start_time_file + datetime.timedelta(seconds=raw.times[-1])
        if end_time_file < start_time:
            continue
        elif start_time_file > end_time:
            break
        else:
            raw.check_is_file1 = check_is_file1(file)
            raw_list.append(raw)

    assert raw_list, "No data in selected duration! "

    if sf is None:
        sf = min(raw.info['sfreq'] for raw in raw_list)

    if resample:
        for idx_raw, raw in enumerate(raw_list):
            if not raw.info['sfreq'] == sf:
                is_first_file = raw.check_is_file1
                raw_list[idx_raw] = raw.copy().resample(sf)
                raw_list[idx_raw].is_first_file = is_first_file
    else:
        raw_list = [raw for raw in raw_list if raw.info['sfreq'] == sf]

    data = np.zeros((len(raw.ch_names), int(sf * (end_time - start_time).total_seconds()) + 1))
    # data[:] = np.nan
    for raw in raw_list:

        if raw.check_is_file1 or ('idx_whole_start' not in locals()):
            start_time_file = raw.annotations.orig_time
            idx_whole_start = int((start_time_file - start_time).total_seconds() * sf)
        else:
            idx_whole_start += data_len

        data_len = raw.n_times
        if idx_whole_start + data_len < 0:
            continue
        flag_overlap = (0 <= np.arange(idx_whole_start, idx_whole_start + data_len, 1)) \
                       & (np.arange(idx_whole_start, idx_whole_start + data_len, 1) < data.shape[1])

        raw_data = mne.io.read_raw_edf(raw.filenames[0], infer_types=True, verbose=False)

        if resample:
            raw_data = raw_data.resample(sf)

        data[:, max(0, idx_whole_start):min(idx_whole_start + data_len, data.shape[1])] = \
            raw_data.get_data()[:, flag_overlap]

    new_chan_names = raw.ch_names
    new_chan_types = raw.get_channel_types()

    if 'X' in new_chan_names:
        loco = acc_to_locomotion(data[-3:, :])
        data = np.concatenate([data[:-3, :], loco], axis=0)
        new_chan_names = [chan for chan in raw.ch_names if chan not in ['X', 'Y', 'Z']] + ['Locomotion']
        new_chan_types = [new_chan_types[i] for i, chan in enumerate(raw.ch_names) if chan not in ['X', 'Y', 'Z']] + [
            'bio']

    info = mne.create_info(ch_names=new_chan_names, sfreq=sf, ch_types=new_chan_types, verbose=False)
    raw = mne.io.RawArray(data, info, verbose=False)
    raw.set_meas_date(start_time)

    # Bipolar ref
    chan_anode = [chan for chan in raw.ch_names if '+' in chan]
    chan_cathode = [chan for chan in raw.ch_names if '-' in chan]
    if chan_anode:
        chan_bipolar = [chan[:-1] for chan in chan_anode]
        chan_bipolar_type = [raw.get_channel_types()[i] for i, chan in enumerate(raw.ch_names) if chan in chan_anode]
        raw = mne.set_bipolar_reference(raw, anode=chan_anode, cathode=chan_cathode, ch_name=chan_bipolar)

    T1 = time.time()
    print(f'Import data spending {T1 - T0:.2f} sec. ')

    return raw


def slice_multidays(animal_list=None, date0=None, num_days=1, reverse=True,
                    **kwargs
                    ):
    """多天原始数据的预处理
    从date0开始，往前回溯num_days天，拼接每天原始的数据，并对每天的数据进行后续处理....
    :param animal_list: 编号列表
    :param flag_slice: 转为fif raw文件
    :returns: None
    """

    if not animal_list:
        animal_list = os.listdir(get_data_path('out'))

    if not date0:
        date0 = datetime.datetime(datetime.datetime.today().year,
                                  datetime.datetime.today().month,
                                  datetime.datetime.today().day,
                                  tzinfo=datetime.timezone.utc) - datetime.timedelta(days=1)

    day_range = list(range(num_days))
    if reverse:
        day_range = [-idx_day for idx_day in day_range]

    for idx_day in day_range:
        for animal in animal_list:
            date = date0 + datetime.timedelta(days=idx_day)
            try:
                T0 = time.time()

                path_animal = set_path(os.path.join(get_data_path('out'), animal))
                path_raw = os.path.join(path_animal, 'raw')

                datestr = f'{date.strftime("%Y-%m-%d")}'
                print('\n-------------------------')
                print(f'TFA for date {datestr}')

                raw = slice_data_within_circadian(date, animal, **kwargs)
                raw.set_montage('standard_1020', match_case=False, on_missing='warn')
                raw = reorder_channel_types(raw)
                raw.save(os.path.join(set_path(path_raw), datestr) + '_raw.fif', overwrite=True, split_size='0.5GB')

            except AssertionError as e:
                if 'No data' in e.args[0]:
                    print(f"For {animal}: no data on {date.strftime('%Y-%m-%d')}")
                    continue
                else:
                    raise e


def get_data_on(date, animal, process='raw', **kwargs):
    """Get data from ctfg process file saving in fif

    Parameters
    ----------
    process:
    'raw' | 'ica'

    Returns
    -------
    data : instance of ICA / Raw
    """
    path = get_data_path('out')
    datestr = f'{date.strftime("%Y-%m-%d")}'
    filename = os.path.join(path, animal, process, datestr) + f'_{process}.fif'
    if process == 'raw':
        data = mne.io.read_raw_fif(filename, **kwargs)
    elif process == 'ica':
        data = mne.preprocessing.read_ica(filename, **kwargs)
    else:
        assert "Unknown Process"
    return data