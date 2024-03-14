# Installation
```shell
pip install nrsdk-dataset
```


# Getting started

```python
import os
import nrsdk_dataset as nrd
import datetime

# Set dataset and output path
nrd.set_data_path('in', r'<your_dataset_path_listing_devices>')
nrd.set_data_path('out', r'<your_output_path_listing_subjects>')

# Visualize the dataset across days
animals = os.listdir(nrd.get_data_path('out'))
print(animals)

animal = animals[0]
nrd.viz_dataset(
    animal,
    start_time=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc)
)

# Slice data according time span
nrd.slice_data_within(
    animal=animal,
    start_time=datetime.datetime(2024, 1, 7, 15, tzinfo=datetime.timezone.utc),
    end_time = datetime.datetime(2024, 1, 7, 17, tzinfo=datetime.timezone.utc)
)

# Slice circadian data
nrd.slice_data_within_circadian(
    animal=animal,
    date=datetime.datetime(2024, 1, 7, tzinfo=datetime.timezone.utc),
)

# Auto-slice data across multiple days
nrd.slice_multidays(
    animal_list=animals,
    num_days=7,
    date0=datetime.datetime(2024, 1, 7, tzinfo=datetime.timezone.utc)
)

# Get MNE Raw object lasting 24h
raw = nrd.get_data_on(animal=animal, date=datetime.datetime(2024, 1, 7, tzinfo=datetime.timezone.utc))
```