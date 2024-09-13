# Check size memory
+ df -h : check size all disk in system 
+ du -sh : check sum size current directory
+ du -sh * : check size all file/directory of current directory
+ check number of file in folder(count file image in folder): `ls -l . | grep -v '^d' | wc -l`

# No space left on device ubuntu
+ `Ctr + alt + f2`
+ remove image docker not using:  `docker image prune -a` -> sudo reboot
+ Check folder using memory: View folder mounted with SSD (`/`)
  + `cd /`
  + `du -sh *`
  + Fine folder using memory and delete (var/log) - `sudo rm /var/log/Xorg.1.log.old`
  

# Increase swap
+ `swapon`
+ `sudo swapoff /swapfile`
+ `swapon`
+ `sudo dd if=/dev/zero of=/swapfile bs=1M count=8192 status=progress`
+ `sudo chmod 600 /swapfile`
+ `sudo mkswap /swapfile`
+ `sudo swapon /swapfile`
+ `free -h`