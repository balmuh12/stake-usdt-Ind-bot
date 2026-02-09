import json
import os

DB_FILE = "database.json"

# Load database
def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"users": []}, f)
    with open(DB_FILE) as f:
        return json.load(f)

# Save database
def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Tambah transaksi user
def add_user_transaction(user_id, name, package, deposit):
    db = load_db()
    for user in db["users"]:
        if user["user_id"] == user_id:
            return False  # sudah ada
    db["users"].append({
        "user_id": user_id,
        "name": name,
        "package": package,
        "deposit": deposit,
        "duration": PACKAGES[package]["duration"],
        "profit_per_day": PACKAGES[package]["profit_per_day"],
        "status": "pending",
        "days_completed": 0
    })
    save_db(db)
    return True

# Update status transaksi
def update_status(user_id, status):
    db = load_db()
    for user in db["users"]:
        if user["user_id"] == user_id:
            user["status"] = status
    save_db(db)

# Ambil semua transaksi pending
def get_pending_transactions():
    db = load_db()
    return [u for u in db["users"] if u["status"] == "pending"]
