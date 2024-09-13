from app.mongo_dal.identity_dal import IdentityDAL
from app.mongo_dal.object_dal import ObjectDAL
import numpy as np
from datetime import datetime

object_dal = ObjectDAL()
identity_dal = IdentityDAL()

item = identity_dal.find_all_item()

total_hs = []
for hs in item:
    if hs["branch_id"] == "7fe24a89-8007-4541-b6b7-4f1582896861":
        total_hs.append(hs)
print(len(total_hs))

item = object_dal.find_all_item()

# Filter item item["have_new_face"] is True and sort time.
new_item = []
list_time = []
for i in range(len(item)):
    hs = item[i]
    date_time = hs["created_at"]
    seconds = date_time.timestamp()
    if hs.get("identity_name") is not None:
        new_item.append(item[i])
        list_time.append(seconds)
list_index_sort = np.argsort(np.array(list_time))[::-1]
item = np.array(new_item)[list_index_sort]

branch_id = "7fe24a89-8007-4541-b6b7-4f1582896861"
if branch_id is not None:
    new_item = []
    for hs in item:
        hs_data = identity_dal.find_by_id(hs["identity"])
        if hs_data is not None and hs_data.get("branch_id") is not None and (hs_data["branch_id"] == branch_id):
            new_item.append(hs)
    item = new_item


# format_time = "%Y-%m-%dT%H:%M:%S.%fZ" # time utc
# format_time = '%Y-%m-%dT%H:%M:%S%z'  # time zone
format_time = '%Y-%m-%dT%H:%M:%S'  # time zone

# for i in range(4, 9):
from_date = "2022-04-0" + str(5) + "T00:00:00"
from_date_dt = datetime.strptime(from_date, format_time)
print("time_dt: ", from_date_dt)

# Convert datetime to second time
from_date_s = from_date_dt.timestamp()

new_item = []
for i in range(len(item)):
    hs = item[i]
    date_time = hs["created_at"]
    # print(date_time)
    seconds = date_time.timestamp()
    if seconds <= from_date_s + 86400 and (seconds >= from_date_s):
        new_item.append(hs)
item = new_item
print(len(item))
print("{}/{}".format(len(item), len(total_hs)))
