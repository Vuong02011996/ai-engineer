# Reference
+[install_nginx](https://phoenixnap.com/kb/how-to-install-nginx-on-ubuntu-20-04)
## Install nginx
+ sudo apt-get update
+ sudo apt-get install nginx
+ nginx -v
+ sudo systemctl status nginx
+ if not running: sudo systemctl start nginx
+ sudo systemctl enable nginx : load nginx when system starts.

## Command often using

+ sudo nginx -t (check config syntax)
+ sudo systemctl restart nginx (restart nginx service)


## Install cert-box(app by let's encrypt)
+ [Cấp chứng chỉ ssl cho domain](https://phoenixnap.com/kb/letsencrypt-nginx)
+ Domain phải được đăng kí trước.
+ Cấp chứng chỉ ssl cho domain https.
+ Adjust Firewall to Allow HTTPS Traffic(sudo ufw status)
  + Nginx HTTP (opens port 80)
  + Nginx HTTPS (opens port 443 – encrypted traffic)
  + Nginx Full (opens port 80 and 443) - sudo ufw allow 'Nginx Full'
### Install cert box
+ sudo snap install --classic certbot
+ sudo ln -s /snap/bin/certbot /usr/bin/certbot
+ ### Cấp chứng chỉ ssl cho domain.
+ sudo certbot --nginx -d clover.greenlabs.ai

## Note(a Quang)
+ Nếu máy 133 đã được public port 80 và 443 thì mới dùng certbox cấp chứng chỉ ssl cho domain (https). Còn không chỉ chạy được domain http.
+ Hiện tại a Quang đã dùng máy ảo 192.168.111.55(ssh ggsysadmin@192.168.111.55) để mở port 80, 443 để dns proxy pass. cho all domain `*.greenlab.ai.`
+ Chỉ cần ssh vô máy 55(ssh dev@192.168.111.55 | pass dev##4321) để config nginx.
+ Copy ssl key có sẵn(a Quang tạo 1 key general) vào file `*.conf` là oke.
+ 192.168.111.55 -> 192.168.111.146.(root |ggadminbk)
+ ```commandline
        ssl_certificate /etc/ssl/private/greenlabs.pem;
        ssl_certificate_key /etc/ssl/private/greenlabs.key;
```