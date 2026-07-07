# Administration Module & Permissions Matrix

## Purpose
Enforces the backend RBAC (Role-Based Access Control) matrix, establishing specific operational limits across customer and back-office roles.

---

## Roles & Responsibilities

The system defines 4 distinct roles:

1. **Super Admin**: Full permissions. Handles system setup, warehouse locations, price catalogs, reports, and accounts blocking.
2. **Admin**: Operational control. Manages customer accounts, catalog listings, order status progressions, and chat queues.
3. **Support Agent**: Customer support. Assigned to handle chat messages and read order detail snapshots for assistance.
4. **Customer**: General client. Places orders, configures profile addresses, and rates services.

---

## Security Permissions Matrix

| Endpoint / Action | Customer | Support Agent | Admin | Super Admin |
|---|---|---|---|---|
| Register / Auth Account | Public | Public | Public | Public |
| Add / Delete Addresses | ✅ Yes | ❌ No | ❌ No | ❌ No |
| View Service Catalog | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Place Order / Reorder | ✅ Yes | ❌ No | ❌ No | ❌ No |
| Cancel Order | ✅ Yes (Placed only) | ✅ Yes | ✅ Yes | ✅ Yes |
| Update Order Status / Rider | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| Submit Review rating | ✅ Yes | ❌ No | ❌ No | ❌ No |
| Open Support Chat | ✅ Yes | ❌ No | ❌ No | ❌ No |
| Send Chat Reply | ✅ Yes (Own) | ✅ Yes (Assigned) | ✅ Yes | ✅ Yes |
| Resolve Chat Session | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| Block / Unblock Users | ❌ No | ❌ No | ✅ Yes | ✅ Yes |
| Update Warehouse Settings | ❌ No | ❌ No | ❌ No | ✅ Yes |
| Generate Financial Reports | ❌ No | ❌ No | ✅ Yes | ✅ Yes |
