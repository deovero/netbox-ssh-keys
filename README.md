# NetBox SSH Keys Plugin

A [NetBox](https://github.com/netbox-community/netbox) plugin for managing SSH public keys as first-class objects.

## Features

- **SSH Key Management** — Store and manage SSH public keys with type, key material, comment, and auto-calculated SHA256 fingerprint
- **Tenant Association** — Assign SSH keys to tenants (customers)
- **Device/VM Assignment** — Assign keys to devices and virtual machines via generic foreign keys
- **REST API** — Full CRUD operations via NetBox's REST API
- **GraphQL** — Query SSH keys via NetBox's built-in GraphQL API
- **Bulk Import** — Paste `authorized_keys` content to import multiple keys at once
- **Template Extensions** — SSH keys panel on Tenant, Device, and VM detail pages
- **Search** — SSH keys indexed in NetBox's global search

## Compatibility

| NetBox Version | Plugin Version |
|----------------|----------------|
| 4.2+           | 0.1.x          |

## Installation

```bash
pip install git+https://github.com/deovero/netbox-ssh-keys.git
```

Add to NetBox `configuration.py`:

```python
PLUGINS = ['netbox_ssh_keys']
```

Run database migrations:

```bash
cd /opt/netbox/netbox
python manage.py migrate netbox_ssh_keys
```

## Data Model

### SSHKey

| Field         | Type       | Description                                      |
|---------------|------------|--------------------------------------------------|
| `name`        | CharField  | Unique friendly name for the key                 |
| `key_type`    | CharField  | Algorithm (ssh-rsa, ssh-ed25519, ecdsa-*, sk-*)  |
| `public_key`  | TextField  | Base64-encoded public key material               |
| `comment`     | CharField  | Optional comment (e.g., user@host)               |
| `fingerprint` | CharField  | SHA256 fingerprint (auto-calculated, unique)      |
| `tenant`      | ForeignKey | Optional FK to Tenant                            |
| `description` | CharField  | Optional description                             |

Plus tags and custom fields via `NetBoxModel`.

### SSHKeyAssignment

| Field                  | Type              | Description                          |
|------------------------|-------------------|--------------------------------------|
| `ssh_key`              | ForeignKey        | FK to SSHKey                         |
| `assigned_object_type` | ForeignKey (CT)   | ContentType of the assigned object   |
| `assigned_object_id`   | PositiveBigInt    | PK of the assigned object            |
| `assigned_object`      | GenericForeignKey  | Device or VirtualMachine             |

Plus tags and custom fields via `NetBoxModel`.

## Development

```bash
git clone https://github.com/deovero/netbox-ssh-keys.git
cd netbox-ssh-keys
pip install -e .

# Generate/update migrations (from within NetBox)
cd /opt/netbox/netbox
python manage.py makemigrations netbox_ssh_keys
python manage.py migrate netbox_ssh_keys
```
