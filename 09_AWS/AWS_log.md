# Kiểm tra danh sách Kubernetes Clusters
```
kubectx	                    Liệt kê các clusters
kubectx <cluster_name>	    Chọn cluster để làm việc
kubens	                    Liệt kê namespaces trong cluster
kubens <namespace_name>	    Chuyển sang namespace cụ thể
kubectl get pods	        Liệt kê tất cả các Pods trong namespace hiện tại
kubectl logs <pod_name>	    Xem logs của một Pod
kubectl logs -f <pod_name>	Theo dõi logs của Pod theo thời gian thực
kubectl logs <pod_name> -c <container_name>	Xem logs của container trong Pod
stern <pod_name>	        Theo dõi logs của nhiều Pods cùng lúc
```