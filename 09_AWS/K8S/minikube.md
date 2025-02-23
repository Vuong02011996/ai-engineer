# Setup 
+ Docker
+ kubectl
+ minikube : one cluster can run in local machine to practice with K8S. Cluster ban đầu này sẽ có namespace kube-system 
và master node(control-plane).
# Architecture
+ Cluster
  + Master Node(Control Plane)
    + ETCD : 1 Database kiểu key-value , là một data storage lưu tất cả thông tin ứng dụng(Pods) trên Worker node .
    + Scheduler : Kết nối với API server và ETCD để chọn Worker Node nào có thể triển khai ứng dụng.(không kết nối trực tiếp Worker Node)
    + API server : nhận yêu cầu từ admin kết nối Master Node vs Worker Node 
    + Control Manager : kết nối với API server để làm việc với các Worker Node như replicate , ...
    + Cloud Manager: làm việc với các cloud Provider như AWS, GCP, ...
    + Tất cả các thành phần trên đều là container runtime.
  + Worker Node(Data Plane)
    + 1 Node chứa nhiều Pods 
    + 1 Pods chứa 1 hoặc nhiều container runtime.
    + Kubelet: thuyền trưởng của một Worker Node , quản lý các Pods và giao tiếp với Master Node qua API server 
    + Kube-proxy: Giao tiếp giữa các Pods trong một Worker Node.
  + `1 Cluster có thể có 1 hoặc nhiều Master Node và Worker Node.`
  

## Ràng buộc về Version: 
  + kubelet vs api-server
  + api-server giữa các Master Node 
  + https://kubernetes.io/releases/version-skew-policy/

+ `kubectl api-resources` liệt kê tất cả tài nguyên trên k8s và version(có trong file manifest)
# Practice
## Command 
### Get 
+ Pods : `kubectl get pods | po`
+ Replicaset : `kubectl get replicaset | rs`
+ Deployment : `kubectl get deployment | deploy`
+ Service : `kubectl get service | svc`

### Edit 
+ Pods : `kubectl edit pods ten_pods`
+ Replicaset : `kubectl edit rs ten_rs(rs3)`
+ Deployment : `kubectl edit deploy ten_deploy`
+ Service : `kubectl edit svc ten_service`

### Delete 
+ Pods : `kubectl delete pods ten_pods`
+ Replicaset : `kubectl delete rs ten_rs(rs3)`
+ Deployment : `kubectl delete deploy ten_deploy`
+ Service : `kubectl delete svc ten_service`
### Describe 
+ Pods : `kubectl describe pods ten_pods`
+ Replicaset : `kubectl describe rs ten_rs(rs3)`
+ Deployment : `kubectl describe deploy ten_deploy`
+ Service : `kubectl describe svc ten_deploy`
### Expose to service 
+ Pods : `kubectl expose pods ten_pods --port=8080 --name=service-deployment --type=NodePort`
+ Replicaset : `kubectl expose rs ten_rs(rs3) --port=8080 --name=service-deployment --type=NodePort`
+ Deployment : `kubectl expose deploy ten_deploy --port=8080 --name=service-deployment --type=NodePort`
+ `**Expose xong mới có svc**`

## Truy xuất từ bên ngoài vào service trong cluster
+ Mỗi Master Node hay Worker Node chỉ có IP private(internal ), Do đó bên ngoài không thể truy xuất vào service thông qua 
IP:Port . Trong Minikube có hỗ trợ expose để truy xuất từ bên ngoài bằng lệnh
  ``` minikube service service1 --url ``` (service # svc(minikube only using service), service1 tên service) 
  **Việc này trong EKS ta không cần làm**.
  
+ You are using the QEMU driver without a dedicated network, which doesn't support `minikube service` & `minikube tunnel` commands.
  + Error Because minikube start with driver QEMU .
  + minikube delete 
  + minikube start --driver docker 
## Pods
+ Một Node là một máy chủ(VMS, AWS...), chiếm một địa chỉ IP 
+ Pods là một đơn vị triển khai, một dịch vụ cũng có một IP 
+ Bên trong Pods là một hoặc nhiều container, mỗi container sẽ có một Port.
  
+ Mỗi Pods sẽ được cấp 1 bộ nhớ, CPU nhất định nên khi dịch vụ yêu cầu nhiều tài nguyên hơn, K8S sẽ giản nở theo chiều ngang 
tức là tạo ra những Pods khác tương tự chớ không phìm to tài nguyên một Pods. Thậm chí mở rộng Pods qua những Node khác, 
  đến khi hết Node(máy chủ) sẽ có cơ chế tạo ra nhiều Node khác.
  
+ Một Pods có thế chứa nhiều container vs các chức năng riêng biệt hỗ trợ nhau, khi đó các container sẽ kết nối rất nhanh trong 
một Pods vì mạng local, Nhưng nhược điểm là khi giản nở Pods ta phải giản nở tất cả các container trong Pods.
  
+ Command 
```
kubectl get pods 
# app1 tên app 
kubectl run app1 --image=vietaws/eks:v1
kubectl describe pods app1

# Khi có update ở image vietaws/eks:v1 ta run apps ở lệnh trên sẽ không lấy image đã update, lấy image đã download ở local do 
đó ta dùng thêm cờ sau:
kubectl run app1 --image=vietaws/eks:v1 --image-pull-policy Always 
```
## Expose  
+ Có thể expose một Pods, Replicate Set hoặc Deployment thành service.
+ Có các cách expose như : `ClusterIP, NodePort , LoadBalance `
+ ` kubectl expose --help`
    `Possible resources include (case insensitive):
     pod (po), service (svc), replicationcontroller (rc), deployment (deploy), replicaset (rs)`

  
### NodePort Services
+ Khi user bên ngoài cluster muốn kết nối vào container trong Pods phải đi qua hai IP 
  + IP của máy chủ Node (Tất cả IP của Master Node hay Worker Node IP đều là private không phải public )
  + IP của Pods
  
+ Mỗi Pods cũng có một Port riêng, trong K8s muốn export một Pods ra bên ngoài sử dụng có hai kĩ thuật (Services)
  + NodePort : export thông qua IP:Port (Port 30000 -> 32767)
  + LoadBalancer 
  + Cluster IP.
  
+ Command 
```
kubectl get services (svc)
```
### Create một service cho Pods app1 bằng NodePort services 
kubectl expose pods app1 --port=8081 --target-port=8080 --name=service1 --type=NodePort  

+ --port=8081: Port của service ra bên ngoài ánh xạ qua port của container 
+ --target-port=8080: Port của container 
+ --name=service1: tên services 

`kubectl describe svc service1 `


+ Xem thông tin node , chi tiết một node 
```
 kubectl get nodes
 kubectl get nodes -o wide  -o: output 
```

## Other 
### Logs Pods, container trong Pods
+ Logs trong ứng dụng (print - python, console.log - node.js, ...) sẽ được lưu trong Pods (giống docker )
+ Để xem logs một Pods , app1 tên Pods 
  ``` kubectl logs app1```
 
+ Xem logs realtime -f (follow)
``` kubectl logs app1 -f```
  
+ Nếu một Pods có nhiều container phải chỉ rõ tên container , tên container đọc ở  `kubectl describe pods app1`
``` kubectl logs app1 -c tên_container ```

### Kiểm tra bên trong Pods, Container trên K8S 
+ Chui vào container và kiểm tra file/folder 
``` kubectl exec -it app1 -- ls  ->  kubectl exec -it app1 -c tên_c ontainer-- ls : nếu có nhiều container trong Pods```
+ Chui vào trong Pods và kiểm tra thông tin file Dockerfile
``` kubectl exec -it app1 -- cat Dockerfile ```
+ Chui vào terminal Pods và thực hiện lệnh :
``` kubectl exec -it app1 -- sh ```
  

### Imperative vs Declarative
+ Imperative: Sử dụng từng lệnh trên terminal - nhanh, trực quan nhưng với hàng trăm Pods ứng dụng thì mất công...
+ Declarative: Sử dụng chỉ dẫn manifest như file .yaml để thực hiện công việc.(recommended)
  + https://kubernetes.io/docs/concepts/workloads/pods/#using-pods
+ Command 
``` kubectl apply -f ten_file_manifest.yaml```
### K8s Manifest 101 | Cấu trúc YAML file và cách sử dụng
+ key value pair 
+ Dictionary 
+ Array / List
+ Literal style | 
...
+ https://spacelift.io/blog/yaml#basic-yaml-syntax
  
## ReplicaSet
+ Vấn đề khi một Pods bị chết hoặc quản lí nhiều Pods trên nhiều Nodes 
+ Replicaset: Tôi muốn chạy một nhóm các Pods(có định nghĩa số lượng cụ thể) , Khi một Pods ở bất kì Node nào bị lỗi 
thì sẽ tự động tạo ra một Pods khác để đảm bảo số lượng Pods trong một nhóm.
  
+ ReplicaSet không có Imperative.
+ https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/
+ Mỗi Pods có thể có n Labels. Labels là cở sở để nhóm các Pods lại có thể cùng một thuộc tính nào đó thông qua Selector.
+ Template: là trường chứa thông tin một Pods (metadata, spec) 

+ Kiểm tra các replicaset đang chạy 
``` kubectl get rs```
  
+ Run 1 replicaset
``` kubectl apply -f tên_file_rs.yaml```

+ Kiểm tra thông tin 1 replicaset
``` kubectl describe rs ten_replicaset(rs3) ``` ten_replicaset lấy từ ``` kubectl get rs```

+ Kiểm tra các pods đang chạy với rs: ``` kubectl get pods ```

+ Thử xóa 1 pods chạy trong rs: ``` kubectl delete pod tên_pod```. Khi ```kubectl gets pod``` sẽ thấy một pod mới tự động sinh ra 
thay thế cho pods đã xóa. Trong k8s rs(ví dụ 3 pods), khi rs thấy một pods đã chạy với labels được group thì nó chỉ tự động tạo ra 2 pods để
   đảm bảo số lượng là 3.

  + Cơ chế làm việc RS
    + Xóa rs: ``` kubectl delete rs ten_rs(rs3)``` check ``` kubectl get rs```
    + Tạo một pods có labels app3 bằng manual: kubectl run app3-manual --image=vietaws/eks:v1 --labels="app=app3,env=prod"
    + Khi run ``` kubectl apply -f rs3.yaml``` sẽ chỉ có 3 pods được tạo vì đã có một pods labels là app3 đã chạy.
    + DO ĐÓ: khi đặt labels cho Pods phải rõ ràng để replicaset group nhầm các pods.

+ Tất cả các tài nguyên trên K8s đều có labels (pods, replicaset, ...) labels để nhóm các tài nguyên theo chúng ta mong muốn.

### Expose Pods ReplicaSet ra service Imperative Way
+ ``` kubectl expose rs rs3 --port=8082 --name=service3 --type=NodePort ``` (rs == replicasets.apps)
+ Check ``` kubectl get svc ```
+ Trick minikube external IP of Node to access from outside: ``` minikube service service3 --url ```

### Expose NodePort ReplicaSet K8s Declarative Way
+ https://kubernetes.io/docs/concepts/services-networking/service/#nodeport-custom-port

### Edit ReplicaSet và Giới Thiệu Deployment
+ Khi update một ứng dụng , version của image thay đổi, ta edit trong replicaset khá mất công, phải xóa tất cả các pods, sau đó 
run lại replicaset thì mới update được ứng dụng trong Pods
  
+ Do đó ta cần một Object khác là Deployment.

## 20-40 Deployment 
### Create deployment 
+ ```kubectl get pods/rs/svc``` make sure all resource is empty 
+ Imperative:
  + kubectl create deploy --help (Aliases deployment | deploy)
  + ```kubectl create deploy app1-deploy --image vietaws/eks:v1 --port 8080``` (--port 8080 port của app chạy trong container)

+ Declarative:
  + https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
  + `kubectl apply -f deployments.yaml`
  
### Scale deployment(giản nở Pods bằng thủ công (Pods tạo bằng deployment))
  + Đối với scale thì pods tạo ra sẽ nằm trong một nhóm replicaset.
  + Imperative:
    + `kubectl scale --current-replicas=1 --replicas=2 deployment/app1-deploy`: app1-deploy - tên deployment 
    + Check : `kubectl get rs` -> see 2 replicaset of pods app1-deploy and kubectl get pods -> see 2 pod 
    + Check info pods scale(version image/container app): `kubectl describe pods ten_pods ` 
    
  
  + Scale down from 2pods -> 1pods: `kubectl scale --replicas=1 deployment/app1-deploy`

### Service 1 deployments by Node Port 
  `  # Create a service for an nginx deployment, which serves on port 80 and connects to the containers on port 8000
  kubectl expose deployment nginx --port=80 --target-port=8000
  `
  + Imperative: 
    + `kubectl expose deploy app-deployment --port=8080 --name=service-deployment --type=NodePort`
      + 8080: port container run app
      + nginx-deployment: name deployment in file yaml (get name from `kubectl get deploy` not use _, ... in name)
  + Declarative:
    + 
  
### Thay đổi version code của app(container)
+ `kubectl set image --help`
+ `kubectl set image deploy app-deployment simple-app=vietaws/eks:v3`
  + app-deployment: tên deployment 
  + simple-app: tên container cần update 
  + vietaws/eks:v3: version mới cho app/container
  
+ Check: kubectl get rs -> có hai nhóm rs, một mới một cũ.
+ Khi chúng ta sửa deployment(thay đổi version app), thì k8s sẽ tạo ra một replicate set mới chạy pods mới với 
version app mới, nhưng vẫn giữ toàn bộ replicate set cũ, chúng chỉ terminal (tắt) các pods đang chạy của version cũ.
  
### Rollout/Rollback Deployment Kubernetes
+ Deploy lại replicate set với app version cũ (vì app version mới có lỗi hoặc không ưng ý)
+ Step: 
  + Show all version của app: `kubectl rollout history deploy app-deployment`
  + Xem chi tiết bên trong mỗi version thay đổi gì: `kubectl rollout history deploy app-deployment --revision=1`
  + Deploy sang pre-version : `kubectl rollout undo deploy app-deployment`
  + Deploy một version nào đó: `kubectl rollout undo deploy app-deployment --to-revision=2`

+ https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/
  + `kubectl rollout history deploy app-deployment` - View history edit image in app/container
  + `kubectl rollout history deploy app-deployment --revision=1` -  Show the info version 1
  + `kubectl rollout status deploy app-deployment` -  Show the status of the rollout
  
+ Rollback :
```
# Roll back to the previous deployment
kubectl rollout undo deploy app-deployment

# Roll back to deploy revision 3
kubectl rollout undo deploy app-deployment --to-revision=2

# Roll back to the previous deployment with dry-run
kubectl rollout undo --dry-run=server deployment/abc
```
###  Pause & Resume(Unpause) Deployment
+ Rollout, Rollback ta chỉ sửa version image rồi deploy lại.
+ Khi ta muốn sửa nhiều cái cùng một lúc ta cần dùng tính năng  Pause & Resume Deployment.
+ Ví dụ ta muốn rollout verion image khác + giới hạn cpu, ram của con pods này.
+ Step:
  + rollout - chuyển sang deployment version muốn deploy 
  + pause deployment (tạm dừng deployment mới đang muốn thay đổi - version hiện tại vẫn đang chạy)
  + change version image, resources (`kubectl set resources --help `): thay đổi thông tin verrion mới
  + resume deployment.(chạy deployment mới, sẽ tắt version hiện tại đang chạy và chạy cái mới)

### Change Cause on Deployment Revision
+ `kubectl rollout history deploy app-deployment` : không xem được chi tiết mỗi version rollout ta thay đổi gì.
+ Phải dùng : `kubectl rollout history deploy app-deployment --revision=1`, vào từng vision xem
+ annotation: chứa các thuộc tính của một tài nguyên trên k8s 
+ Dùng kubecrl annotate : https://kubernetes.io/docs/reference/kubectl/generated/kubectl_annotate/
### Recreate vs RollingUpdate Deployment Strategies
+ https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-update-deployment
+ Các chiến lược update của deployment 
+ Recreate: tất cả các pods hiện tại sẽ được xóa đi trước khi tạo cái mới.(không cần dư tài nguyên cho pods)
+ RollingUpdate - production: tạo ra các pods mới chạy được thay thế pods cũ rồi mới xóa cũ. (cần tài nguyên nhiều) 
  + Max Unavailable: cho phép bao nhiêu pods unavailable
  + Max Surge: tạo ra bao nhiêu con pods mới oke mới xóa con cũ.
  + `Hai giá trị này quan trọng trong deploy tương quan về thời gian rollout và tài nguyên cũng cấp `
  
### Progress Deadline Seconds
+ Lỗi trong quá trình deploy: không đủ tài nguyên worker node, permission(download container aws, ecr, ..),
+ Dùng `kubectl patch` để set thời gian bung ra lỗi cho deployment. 
+ Check lỗi  `kubectl describe deploy app-deployment` in line `Progressing    True    NewReplicaSetAvailable`

### Restart Deployment
+ Sẽ tạo một replicate set mới nhưng vẫn không thay đổi gì version trong các pods.

## Service 
+ Các loại service trên K8S: `ClusterIP vs NodePort vs LoadBalancer vs ExternalName`
+ `kube-proxy(bảng định tuyến)`: một con pods đặc biệt có ở tất cả các Node dùng để lưu trữ thông tin IP, port các pods, container trong Node.
+ Mỗi pods sẽ có một địa chỉ IP để các dịch vụ khác truy xuất vào, do đo khi ta deployment hay replicate set sẽ có rất 
nhiều pods tương tự sinh ra thay thế pods cũ, ta không thể thay đổi IP của con pods liên tục như vậy. Do đó `Service` sinh ra để 
  cố định IP cho một con pods và theo nó suốt đời dù nó giản nở vẫn luôn giữ IP đó. Service tổng hợp các pods thành một nhóm để 
  chung IP.
  
+ Trong service cũng là một pods đặc biệt trong woker node đã có sẵn cơ chế load balance. Các loại service:
  + ClusterIP: mặc định và private : Dùng để kết nối các pods trong một Node (như pods app vs pods database), Ví dụ ta dùng 
    cluster IP cho database thì những user bên ngoài không thể truy xuất vào, chỉ có pods khác trong node mới truy xuất được.
  + NodePort: Public dùng để user truy xuất vào các pods/app bên trong Node bg IP Node: Port Node.(Port tu 30000 -> 32676 )
  + LoadBalancer: Trong qua trinh deploy se co rất nhiều Node tạo ra và xóa đi, do đó ta không thể nhớ tất cả IP của Node để 
  dùng NodePort. Loadbalancer dùng DNS, một tên chung. Khi bạn tọa service loại là LoadBalancer thì nó sẽ kết hợp với các 
    cloud Provider(alb-aws) để tạo ra một domain nào đấy , tên miền này sẽ tự routing các Node luôn nên ta không cần phải nhớ địa 
    chỉ IP.

### Demo Services | ClusterIP vs NodePort vs LoadBalancing
#### ClusterIP
+ `kubectl apply -f clusterIP.yaml`
+ Tạo một pods label app1: `kubectl run pod1 --image=vietaws/eks:v1 --port=8080 -l="app=app1,env=demo"` 
+ Với label là app=app1 thì service sẽ tự động map với những pods có label app=app1, và tạo ra các IP tương ứng.
+ Check 
  + get ip service : `kubectl describe svc clusterip-svc` check endpoint
  + Chui vào container get ip  ifconfig : `kubectl exec -it pod1 -- sh` cùng IP với endpoiner ở trên là OKE.
#### NodePort 
+ `kubectl apply -f node_port.yaml `
+ `kubectl get svc`
+ `minikube service nodeport-svc --url`
#### LoadBalancer 
+ Phải có cloud Provider mới deploy được.minikube không hỗ trợ.
+ Bản chất LoadBalancer cũng là nodePort có DNS.

#### External Name 
+ Kết nối một database nằm bên ngoài cluster 

## Namespace 
+ `kubectl get ns | kubectl describe ns ten_ns` 
+ Group một nhóm các tài nguyên trong cluster. Namespace khái niệm luận lý, Cluster cái niệm vật lý.
  
+ Namespace có thể nằm hết ở một node hoặc có thể ở các node khác nhau. chỉ là khái niệm luận lý.
+ Có thể tạo nhiều namespace trong một cluster. Giúp deploy các resource có thể trùng tên nhau.
  
+ Trong một namespace không thể tạo các tài nguyên cùng tên, ví dụ các pod cùng tên nhau.
+ Các namespace trong K8s có thể truy xuất với nhau.
+ **Các namespace có thể setup những giới hạn về ram, cpu, số lượng truy xuất (ví dụ cho môi trường product khác môi trường dev)**
+ Phân quyền : ví dụ developer chỉ có quyền vào namespace dev, admin có thể vào tất cả namespace 

+ Command:
  + `kubectl create namespace dev`
  + `kubectl get ns `
  + `kubectl run pod1 --image=vietaws/eks:v1 --port=8086 -n dev `
  + `kubectl get pods -n dev`
  + `kubectl describe pods pod1  -n dev`
  
+ Thử kết nối pod1 của dev vào pod1 của default 
  + `kubectl get pods -o wide`: lấy IP pod1 default 
  + `kubectl get pods -o wide -n dev`
  + `kubectl exec -it pod/pod1 -n dev -- sh`
  + Ping qua IP pod1 của default 

+ Tạo namespace bằng Declarative
  + `kubectl apply -f namespace.yaml `
  + Triển khai app1 trong ns1, app2 trong ns2 
    + Tạo file app1, app2 gồm deployment và service , thêm metadata namespace cho deployment và service
    + Đưa 3 file app1, app2, namespace.yaml vào folder tên ns 
    + Run: `kubectl apply -f ns`, deploy theo tên folder 
  + Check :
    + `kubectl get pods -n ns1`
    + `kubectl get pods -n ns2`
    + `kubectl get svc -n ns1`
    + `kubectl get svc -n ns2`
  + Delete `kubectl delete -f ns` : Khi xóa một namespace thì tất cả tài nguyên bên trong sẽ xóa.
    
# Error
+ minikube start
    ```
    Enabling 'default-storageclass' returned an error: running callbacks: [sudo KUBECONFIG=/var/lib/minikube/kubeconfig /var/lib/minikube/binaries/v1.32.0/kubectl apply --force -f /etc/kubernetes/addons/storageclass.yaml: Process exited with status 1
    ```
    minikube delete
