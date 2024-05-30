# view disk use in ubuntu
+ sudo fdisk -l
+ lsblk
-> USB: sdc.. sdb..
# mount USB
+ sudo mkdir /media/USB_TaiNH
+ sudo mount /dev/sdc1 /media/USB_TaiNH/

# umount USB
+ sudo umount /dev/sdc1
+ sudo unount /media/USB_TaiNH/

# Copy folder in ubuntu(Must sudoers)
+ sudo cp -r obj_lan3 /media/USB_TaiNH/

# copy file to folder in ubuntu
+ cp darknet53.conv.74 file_train/
# check size of directory 
+ du -sh obj

# count number of file in directory
+ find obj_lan3/ | wc -l

# find one file in system
+ sudo find . -name *irtualenvwrapper.sh
+ sudo find / -name 'libcudart.so.10.1' 

# View hardware mount points, Kiểm tra HDD đã mount được với mount point(tên) nào?
+ sudo nano /etc/fstab
+ /etc/fstab: static file system information.

# blkid 
+ Use 'blkid' to print the universally unique identifier for a device; this may be used with UUID= as a more robust way to name devices 
that works even if disks are added and removed.
