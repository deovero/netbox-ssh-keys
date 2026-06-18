# NetBox SSH Keys Plugin

A [NetBox](https://github.com/netbox-community/netbox) plugin for managing SSH public keys as first-class objects.

## Features

- **SSH Key Management** — Store and manage SSH public keys with type, key material, and auto-calculated SHA256 fingerprint
- **Tenant or Device Role Association** — Assign SSH keys to either a tenant (customer) or a device role (mutually exclusive)
- **REST API** — Full CRUD operations via NetBox's REST API
- **GraphQL** — Query and filter SSH keys (by name, key type, public key, fingerprint, tenant, device role) via NetBox's GraphQL API
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
| `name`        | CharField  | 256        | Friendly name for the key                        |
| `key_type`    | CharField  | 64         | Algorithm (ssh-rsa, ssh-ed25519, ecdsa-\*, sk-\*)|
| `public_key`  | CharField  | 1023       | Base64-encoded public key material               |
| `fingerprint` | CharField  | 128        | SHA256 fingerprint (auto-calculated)             |
| `tenant`      | ForeignKey | —          | Optional FK to Tenant (mutually exclusive with device role) |
| `device_role` | ForeignKey | —          | Optional FK to Device Role (mutually exclusive with tenant) |
| `description` | CharField  | 200        | Optional description                             |

Plus tags and custom fields via `NetBoxModel`.

### Uniqueness

- An SSH key may be assigned to a tenant **or** a device role, but not both.
- `fingerprint` + `tenant` — unique together. The same key material can exist under different tenants, but not twice under the same tenant.
- `fingerprint` + `device_role` — unique together. The same key material can exist under different device roles, but not twice under the same device role.
- The same key material can exist once for a tenant and once for a device role.
- `name` — not unique. Multiple keys (even across tenants) may share the same name.

### API Filtering

SSH keys can be filtered via the REST API using the following query parameters:

| Parameter     | Type   | Description                          |
|---------------|--------|--------------------------------------|
| `public_key`  | string | Exact match on base64 key material   |
| `fingerprint` | string | Exact match on SHA256 fingerprint    |
| `key_type`    | string | Filter by algorithm type             |
| `tenant`      | slug   | Filter by tenant slug                |
| `tenant_id`   | int    | Filter by tenant ID                  |
| `device_role` | slug   | Filter by device role slug           |
| `device_role_id` | int | Filter by device role ID            |
| `name`        | string | Filter by name                       |

### Multi-object Custom Fields

The `public_key` field is included in `brief_fields`, allowing SSH keys to be referenced in multi-object custom fields using `{"public_key": "<base64>"}` — similar to how IPAM prefixes use `{"prefix": "<cidr>"}`.

> **Note:** The `public_key` field stores only the base64-encoded key material (without the type prefix or comment).
> The 1023-character limit comfortably accommodates RSA-4096 (≈716 chars), ECDSA (≈140–232 chars),
> and Ed25519 (≈68 chars) keys. RSA-8192 keys (≈1392 chars) are **not** supported.

### GraphQL Queries

#### Tenant SSH Keys

```graphql
query tenant_sshkeys($tenantSlug:String!) {
  ssh_key_list(
    filters: {
      tenant: {
        slug: { exact: $tenantSlug }
      }
    }
  ) {
    public_key
    name
    authorized_keys_line
  }
}
```

Tenant SSH Keys: flat list

```graphql
query tenant_sshkeys_flat($tenantSlug:String!) {
  ssh_key_authorized_keys_lines(tenant_slug: $tenantSlug)
}
```

Variables:
```json
{
  "tenantSlug": "cust_somename"
}
```

#### Device Role SSH Keys

```graphql
query device_role_sshkeys($deviceRoleSlug: String!) {
  ssh_key_list(
    filters: {
      device_role: {
        slug: { exact: $deviceRoleSlug }
      }
    }
  ) {
    public_key
    name
    authorized_keys_line
  }
}
```

Tenant SSH Keys: flat list
```
query device_role_sshkeys_sshkeys_flat($deviceRoleSlug:String!) {
  ssh_key_authorized_keys_lines(device_role_slug: $deviceRoleSlug)
}
```

Variables:
```json
{
  "deviceRoleSlug": "purp_somename"
}
```


## Development

Clone the repository and install in editable mode inside your NetBox development environment:

```bash
git clone https://github.com/deovero/netbox-ssh-keys.git
cd netbox-ssh-keys
python3.14 -m venv .venv
source .venv/bin/activate
pip install -e .

# Generate/update migrations (from within NetBox)
cd /path/to/netbox/netbox
python manage.py makemigrations netbox_ssh_keys
python manage.py migrate netbox_ssh_keys
```

Enable the local Git hook so the patch version in `pyproject.toml` is automatically bumped on commit when unchanged from `HEAD`:

```bash
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit scripts/bump_version.py
```

## Testing in Docker

```
docker compose -f dev-docker/docker-compose.yml down --volumes --remove-orphans --rmi all
docker compose -f dev-docker/docker-compose.yml up --detach --build
```

If everything works after 5 minutes you should be able to login on http://localhost:8000 using admin/admin.

## License

Apache 2.0 — see [LICENSE](LICENSE).

