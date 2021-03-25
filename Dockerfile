FROM odoo:14

# Expose Odoo services
# EXPOSE 8069 8071 8072
USER root

RUN echo 'deb http://ftp.de.debian.org/debian buster main' > /etc/apt/sources.list.d/dpkg.list \
    && apt-get update \
    && apt-get install --no-install-recommends -y python3-pyinotify \
    && rm -rf /etc/apt/sources.list.d/dpkg.list

# Set default user when running the container
USER odoo

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
CMD ["odoo"]