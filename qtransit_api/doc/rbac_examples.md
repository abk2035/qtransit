# RBAC Example Requests

Examples using `curl` for the RBAC endpoints added.

1) Attach a permission to a role

```bash
curl -X POST "http://localhost:8000/roles/1/permissions" \
  -H "Authorization: Bearer <TOKEN>" \
  -d "permission_id=2"
```

2) Detach a permission from a role

```bash
curl -X DELETE "http://localhost:8000/roles/1/permissions/2" \
  -H "Authorization: Bearer <TOKEN>"
```

3) Assign a role to a user

```bash
curl -X POST "http://localhost:8000/users/3/roles" \
  -H "Authorization: Bearer <TOKEN>" \
  -d "role_id=1"
```

4) Remove a role from a user

```bash
curl -X DELETE "http://localhost:8000/users/3/roles/1" \
  -H "Authorization: Bearer <TOKEN>"
```

Using RBAC dependency on routes:

```python
from app.api.deps import require_permission

@router.get('/secure')
def secure_endpoint(_=Depends(require_permission('can_view'))):
    return {'ok': True}
```
