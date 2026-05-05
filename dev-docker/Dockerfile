# Extends the official NetBox image with the netbox-ssh-keys plugin
# installed from the local source tree.
ARG NETBOX_VERSION=v4.2-3.2.1
FROM netboxcommunity/netbox:${NETBOX_VERSION}

USER root

# Copy plugin sources into the image and install it.
COPY pyproject.toml README.md MANIFEST.in /opt/netbox-ssh-keys/
COPY netbox_ssh_keys /opt/netbox-ssh-keys/netbox_ssh_keys

RUN VIRTUAL_ENV=/opt/netbox/venv uv pip install --no-cache-dir /opt/netbox-ssh-keys

USER unit:unit
