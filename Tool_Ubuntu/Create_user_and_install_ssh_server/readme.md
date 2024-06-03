# Create new user with root 
+ https://www.cyberciti.biz/faq/add-new-user-account-with-admin-access-on-linux/
+ Create a new user named thanhnx, run: `adduser thanhnx`
+ Make thanhnx user ‘sudo user’ (admin) run: `usermod -aG sudo thanhnx`
+ Verify it by running the `id thanhnx` command
+ Log in as thanhnx: `su - thanhnx`
+ Exit run: `exit`
# Install ssh server on ubuntu 
+ https://www.cyberciti.biz/faq/ubuntu-linux-install-openssh-server/
+ `sudo apt-get install openssh-server`
+ Enable the ssh service by typing: `sudo systemctl enable ssh`
+ Start the ssh service by typing: `sudo systemctl start ssh`
+ Check status ssh server: `sudo systemctl status ssh`

# Login to ssh by another pc
+ `ssh userName@Your-server-name-IP`
+ `ssh thanhnx@192.168.111.` Pass 1