# NetBox SSH Keys Plugin

A [NetBox](https://github.com/netbox-community/netbox) plugin for managing SSH public keys as first-class objects.

## Features

- **SSH Key Management** — Store and manage SSH public keys with type, key material, and auto-calculated SHA256 fingerprint
- **Tenant Association** — Assign SSH keys to tenants (customers)
- **REST API** — Full CRUD operations via NetBox's REST API
- **GraphQL** — Query and filter SSH keys (by name, key type, public key, fingerprint, tenant) via NetBox's GraphQL API
- **Bulk Import** — Paste `authorized_keys` content to import multiple keys at once
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

| Field         | Type       | Max Length | Description                                      |
|---------------|------------|------------|--------------------------------------------------|
| `name`        | CharField  | 256        | Unique friendly name for the key                 |
| `key_type`    | CharField  | 64         | Algorithm (ssh-rsa, ssh-ed25519, ecdsa-*, sk-*)  |
| `public_key`  | CharField  | 1023       | Base64-encoded public key material               |
| `fingerprint` | CharField  | 128        | SHA256 fingerprint (auto-calculated, unique)      |
| `tenant`      | ForeignKey | —          | Optional FK to Tenant                            |
| `description` | CharField  | 200        | Optional description                             |

Plus tags and custom fields via `NetBoxModel`.

> **Note:** The `public_key` field stores only the base64-encoded key material (without the type prefix or comment).
> The 1023-character limit comfortably accommodates RSA-4096 (≈716 chars), ECDSA (≈140–232 chars),
> and Ed25519 (≈68 chars) keys. RSA-8192 keys (≈1392 chars) are **not** supported.

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
