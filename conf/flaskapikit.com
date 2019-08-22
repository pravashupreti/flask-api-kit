server {
        listen          5000;
        client_max_body_size 200M;
        server_name ~^(?<subdomain>\w+)-dev\.flaskapikit\.com$;
        proxy_read_timeout 120;

        if ($http_x_forwarded_proto != 'https') {
            rewrite ^(.*) https://$host$1 redirect;
        }

        location / {
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $http_x_forwarded_proto;
            proxy_set_header Host $host;
            uwsgi_pass      unix:///run/app.sock;
            include         uwsgi_params;
            uwsgi_param     UWSGI_SCHEME $scheme;
            uwsgi_read_timeout  120s;
            uwsgi_max_temp_file_size 20480m;
        }

}

server {
        listen          5000;
        client_max_body_size 200M;
        server_name ~^(?<subdomain>\w+)-qa\.flaskapikit\.com$;
        proxy_read_timeout 120;

        if ($http_x_forwarded_proto != 'https') {
            rewrite ^(.*) https://$host$1 redirect;
        }

        location / {
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $http_x_forwarded_proto;
            proxy_set_header Host $host;
            uwsgi_pass      unix:///run/app.sock;
            include         uwsgi_params;
            uwsgi_param     UWSGI_SCHEME $scheme;
            uwsgi_read_timeout  120s;
            uwsgi_max_temp_file_size 20480m;
        }

}

server {
        listen          5000;
        client_max_body_size 200M;
        server_name ~^(?<subdomain>\w+)-staging\.flaskapikit\.com$;
        proxy_read_timeout 120;

        if ($http_x_forwarded_proto != 'https') {
            rewrite ^(.*) https://$host$1 redirect;
        }

        location / {
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $http_x_forwarded_proto;
            proxy_set_header Host $host;
            uwsgi_pass      unix:///run/app.sock;
            include         uwsgi_params;
            uwsgi_param     UWSGI_SCHEME $scheme;
            uwsgi_read_timeout  120s;
            uwsgi_max_temp_file_size 20480m;
        }

}

server {
        listen          5000;
        client_max_body_size 200M;
        server_name     _;
        proxy_read_timeout 120;

        if ($http_x_forwarded_proto != 'https') {
            rewrite ^(.*) https://$host$1 redirect;
        }

        location / {
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $http_x_forwarded_proto;
            proxy_set_header Host $host;
            uwsgi_pass      unix:///run/app.sock;
            include         uwsgi_params;
            uwsgi_param     UWSGI_SCHEME $scheme;
            uwsgi_read_timeout  120s;
            uwsgi_max_temp_file_size    20480m;
        }

}
