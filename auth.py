import hashlib
import hmac
import secrets

ROLES = ("Admin", "Service Advisor", "Mechanic", "Accounts")
ROLE_PAGES = {
    "Admin": {
        "dashboard", "maintenances", "customers", "vehicles", "reminders",
        "mechanics", "payments", "diagnostics", "users",
    },
    "Service Advisor": {
        "dashboard", "maintenances", "customers", "vehicles", "reminders",
    },
    "Mechanic": {"dashboard", "maintenances", "vehicles", "diagnostics"},
    "Accounts": {"dashboard", "customers", "payments"},
}
_HASH_ITERATIONS = 310_000
_HASH_PREFIX = "pbkdf2_sha256"


def normalize_role(role):
    if not isinstance(role, str):
        return None
    for known_role in ROLES:
        if role.strip().casefold() == known_role.casefold():
            return known_role
    return None


def hash_password(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, _HASH_ITERATIONS
    )
    return "{}${}${}${}".format(
        _HASH_PREFIX, _HASH_ITERATIONS, salt.hex(), digest.hex()
    )


def verify_password(password, stored_password):
    if not stored_password.startswith(_HASH_PREFIX + "$"):
        return hmac.compare_digest(password, stored_password), True

    try:
        prefix, iterations, salt_hex, digest_hex = stored_password.split("$", 3)
        if prefix != _HASH_PREFIX:
            return False, False
        iterations = int(iterations)
        if iterations < 1:
            return False, False
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, iterations
        )
    except (ValueError, TypeError):
        return False, False

    return hmac.compare_digest(actual, expected), False


def ensure_role_column(cursor):
    cursor.execute("SHOW COLUMNS FROM users LIKE 'role'")
    if cursor.fetchone() is None:
        cursor.execute(
            "ALTER TABLE users ADD COLUMN role VARCHAR(32) NOT NULL DEFAULT 'Mechanic'"
        )


def authenticate(username, password):
    import connection

    db = connection.open_connection()
    cursor = db.cursor()
    try:
        ensure_role_column(cursor)
        db.commit()
        cursor.execute(
            "SELECT password, role FROM users WHERE username = %s LIMIT 1",
            (username,),
        )
        record = cursor.fetchone()
        if not record or record[0] is None:
            return None

        valid, needs_upgrade = verify_password(password, str(record[0]))
        if not valid:
            return None

        role = normalize_role(record[1]) or "Mechanic"
        if needs_upgrade:
            cursor.execute(
                "UPDATE users SET password = %s WHERE username = %s",
                (hash_password(password), username),
            )
        cursor.execute("SELECT role FROM users")
        bootstrap_admin = not any(
            normalize_role(row[0]) == "Admin" for row in cursor.fetchall()
        )
        if bootstrap_admin:
            role = "Admin"
            cursor.execute(
                "UPDATE users SET role = %s WHERE username = %s",
                (role, username),
            )
        db.commit()
        return {
            "username": username,
            "role": role,
            "bootstrap_admin": bootstrap_admin,
        }
    finally:
        cursor.close()
        db.close()


def create_user(username, password, role):
    import connection

    if not username or not username.strip():
        raise ValueError("Username cannot be empty.")
    if role not in ROLES:
        raise ValueError("Choose a valid workshop role.")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters.")

    db = connection.open_connection()
    cursor = db.cursor()
    try:
        ensure_role_column(cursor)
        cursor.execute(
            "SELECT 1 FROM users WHERE username = %s LIMIT 1", (username,)
        )
        if cursor.fetchone() is not None:
            raise ValueError("That username is already in use.")
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, hash_password(password), role),
        )
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()
        db.close()


def update_user_role(username, role):
    import connection

    if role not in ROLES:
        raise ValueError("Choose a valid workshop role.")

    db = connection.open_connection()
    cursor = db.cursor()
    try:
        ensure_role_column(cursor)
        cursor.execute("SELECT role FROM users WHERE username = %s", (username,))
        record = cursor.fetchone()
        if not record:
            raise ValueError("User no longer exists.")
        if role != "Admin" and normalize_role(record[0]) == "Admin":
            cursor.execute("SELECT role FROM users")
            admin_count = sum(
                normalize_role(row[0]) == "Admin" for row in cursor.fetchall()
            )
            if admin_count <= 1:
                raise ValueError("The last administrator cannot be demoted.")
        cursor.execute(
            "UPDATE users SET role = %s WHERE username = %s", (role, username)
        )
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()
        db.close()
