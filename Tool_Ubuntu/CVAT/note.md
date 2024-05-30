# Set up CVAT
## Document
		
		+ A Hung https://docs.google.com/document/d/1SoQCwtISql2mtKXprOHUJ2wdx7ovgn8NXrSyIZP4wTs/edit#
		+ My document: https://docs.google.com/document/d/1MZfjmLy_gHy21-LV1Ap8eO5ZFQKdNY3rUFLgHNoBJSM/edit
## Set up

		+ Download repo https://gitlab.com/greenlabs/dockers/-/tree/master/cvat#rest-api
		+ cd cvat - Change file docker-compose. Port, IP
		+ Run docker-compose up -d

## Config nginx.
		Note: IP public 14.241.120.239 public port 80, 443(ssl) with a domain public.
		All domain with IP, Port local can NAT to port 80 with domain in ahead.
		So don't need to open public port in local(only with web). 

		+ Create new domain https://www.digitalocean.com/community/tutorials/how-to-set-up-let-s-encrypt-with-nginx-server-blocks-on-ubuntu-16-04
			sudo certbot --nginx -d cvatabc.core.greenlabs.ai
		+ Create file : cvat.conf the same in : https:/https://github.com/Vuong02011996/tools_ubuntu/blob/master/CVAT/nginx_config.conf/github.com/Vuong02011996/tools_ubuntu/blob/master/CVAT/nginx_config.conf
		+ sudo nginx -t
		+ sudo systemctl reload nginx
## Error
		+ PermissionError: [Errno 13] Permission denied: '/home/django/logs/supervisord.log'
		+ Fix: sudo chmod -R 777 .

+ certbot --nginx -d konga.core.greenlabs.ai -d www.konga.core.greenlabs.ai