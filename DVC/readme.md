HƯỚNG DẪN SỬ DỤNG DVC ĐỂ QUẢN LÝ DATASET	1
Hướng dẫn init dvc cho source mới	3
Instal dependencies	3
Init dvc	3
Cấu hình storage s3	3
Thêm dataset & push dvc	3
Hướng dẫn clone source dataset	3
Hướng dẫn cấu hình dvc để pull raw data	4
Hướng dẫn chuyển sang 1 phiên bản dataset khác để train	4
Hướng dẫn trả về phiên bản trước đó của dataset	5
Hướng dẫn push 1 phiên bản dataset mới	5

Hướng dẫn init dvc cho source mới

## Instal dependencies


`pip install dvc dvc-s3`


## Init dvc

`dvc init`



## Cấu hình storage s3
Lưu ý: cần tạo bucket trước trên s3, format bucket cần có prefix dataset ở đầu: vd: “dataset-head", “dataset-traffic-light”, “dataset-objects" ….

`dvc remote add -d s3_bucket s3://<bucket_name>
dvc remote modify s3_bucket endpointurl http://192.168.105.146:9000
dvc remote modify --local s3_bucket access_key_id 'your_access_key'
dvc remote modify --local s3_bucket secret_access_key 'your_access_secret'`


## Thêm dataset & push dvc

`dvc add <folder or file>`

follow theo hướng dẫn để add metadata vào git

`dvc push`

## Hướng dẫn clone source dataset
Các dataset được lưu tập trung tại https://repo.oryza.vn/oryza/dataset
Nếu bạn chưa có quyền truy cập, liên hệ với leader để được cấp quyền

Lệnh để clone (VD source head-person)

`git clone ssh://git@repo.oryza.vn:2222/oryza/dataset/head-person.git`



## Hướng dẫn cấu hình dvc để pull raw data

Data được lưu trên s3 storage (minio) và cấu hình thông qua dvc, bạn có thể xem thông tin bucket ở .dvc/config


[core]
    remote = s3_bucket
['remote "s3_bucket"']
    url = s3://dataset-head-person
    endpointurl = http://192.168.105.146:9000



Khi xem thông tin, bạn sẽ xem được remotename (vd trường hợp này là: s3_bucket)
Để kéo dữ liệu từ dvc, đầu tiên cần cấu hình credential để có thể tải

`pip install dvc dvc-s3`

`dvc remote modify --local s3_bucket access_key_id ‘your_access_key’
dvc remote modify --local s3_bucket secret_access_key ‘your_secret_key'`


Sau đó thực hiện pull về

`dvc pull`



## Hướng dẫn chuyển sang 1 phiên bản dataset khác để train


`git checkout <...>
dvc checkout
`

## Hướng dẫn trả về phiên bản trước đó của dataset

`git checkout HEAD~1 data/data.xml.dvc
dvc checkout`


Hướng dẫn push 1 phiên bản dataset mới
Dataset sẽ gắn liền với metadata trên git, mỗi lần khi có dữ liệu mới (có thay đổi), thực hiện các bước:

`dvc status
dvc add
dvc push`

Ví dụ:

`$ dvc status`
images.dvc:
	changed outs:
		modified:           images

`$ dvc add images`

100% Adding...|███████████████████████████████|1/1 [00:03,  3.97s/file]

To track the changes with git, run:

	git add images.dvc

To enable auto staging, run:

	dvc config core.autostage true


`$ git add images.dvc
$ git commit -m “Update data”
$ git push origin master`

`$ dvc push`



