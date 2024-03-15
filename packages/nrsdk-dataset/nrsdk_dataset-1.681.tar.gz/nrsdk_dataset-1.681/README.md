# Installation
```shell
pip install nrsdk-dataset
```


# Getting started

```python
import os
import nrsdk_dataset as nrd
import datetime

# Set dataset and output path, replace following <path>
nrd.set_data_path('in', r'<your_dataset_path_above_"app_record">')
nrd.set_data_path('out', r'<output_saving_path>')

# Visualize the dataset across days
animals = os.listdir(nrd.get_data_path('out'))
print(animals)

animal = animals[0]
nrd.viz_dataset(
    animal,
    start_time=datetime.datetime(2024, 2, 26, tzinfo=datetime.timezone.utc)
)
```

![dataset](20240226-20240303.png)

```python
# Slice data according time span
nrd.slice_data_within(
    animal=animal,
    start_time=datetime.datetime(2024, 2, 27, 15, tzinfo=datetime.timezone.utc),
    end_time=datetime.datetime(2024, 2, 27, 17, tzinfo=datetime.timezone.utc)
)

# Slice circadian data
nrd.slice_data_within_circadian(
    animal=animal,
    date=datetime.datetime(2024, 2, 27, tzinfo=datetime.timezone.utc),
)

# Auto-slice data across multiple days
nrd.slice_multidays(
    animal_list=animals,
    num_days=2,
    date0=datetime.datetime(2024, 2, 28, tzinfo=datetime.timezone.utc)
)

# Get sliced MNE Raw object lasting 24h
raw = nrd.get_data_on(animal=animal, date=datetime.datetime(2024, 1, 7, tzinfo=datetime.timezone.utc))
```