# Check size memory
+ df -h : check size all disk in system 
+ du -sh : check sum size current directory
+ du -sh * : check size all file/directory of current directory
+ check number of file in folder(count file image in folder): `ls -l . | grep -v '^d' | wc -l`

# Increase swap
+ `swapon`
+ `sudo swapoff /swapfile`
+ `swapon`
+ `sudo dd if=/dev/zero of=/swapfile bs=1M count=8192 status=progress`
+ `sudo chmod 600 /swapfile`
+ `sudo mkswap /swapfile`
+ `sudo swapon /swapfile`
+ `free -h`