# /etc/nginx/sites-available/watchservice.com

# Redirect www.watchservice.com to watchservice.com
server {
        server_name www.watchservice.com;
        rewrite ^ http://watchservice.com/ permanent;
}

# Handle requests to watchservice.com on port 80
server {
        listen 80;
        server_name 185.228.234.35;

                # Handle all locations
        location / {
                        # Pass the request to Gunicor
                proxy_pass http://localhost:8000;
                # Set some HTTP headers so that our app knows where the
                # request really came from
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
}
