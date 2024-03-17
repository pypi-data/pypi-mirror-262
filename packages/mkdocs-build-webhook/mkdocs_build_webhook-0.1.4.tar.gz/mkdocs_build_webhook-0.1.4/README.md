# mkdocs-build-webhook

A webhook that builds your mkdocs projects.

Run it with 

## Installation

    mkdir /usr/share/mkdocs-build-webhook/ /var/www/
    chown -R www-data:www-data /usr/share/mkdocs-build-webhook/ /var/www/


# Docker

    podman build -t mkdocs-build-webhook .    
    podman run  --userns keep-id --rm --name mkdocs-build-webhook -v ./dist/www/:/var/www/:z -e WEBHOOK_SECRET=secret -p 5000:5000 localhost/mkdocs-build-webhook