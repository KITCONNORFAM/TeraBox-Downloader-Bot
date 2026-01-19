def is_premium(user_id):
    return bool(r.get(f"premium:{user_id}"))

def add_premium(uid, days):
    r.set(f"premium:{uid}", "true", ex=days*86400)

def remove_premium(uid):
    r.delete(f"premium:{uid}")
