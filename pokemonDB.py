
import sqlite3
import json

DB_FILE = "pokemon.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            type1 TEXT NOT NULL,
            type2 TEXT,
            moves TEXT DEFAULT '[]'
        )
    """)
    conn.commit()
    conn.close()

def add_pokemon(name, type1, type2=None, moves=None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        moves_json = json.dumps(moves) if moves else '[]'
        cursor.execute("""
            INSERT INTO pokemon (name, type1, type2, moves)
            VALUES (?, ?, ?, ?)
        """, (name, type1, type2, moves_json))
        conn.commit()
        return f"Pokémon '{name}' added successfully!"
    except sqlite3.IntegrityError:
        return f"Pokémon '{name}' already exists."
    finally:
        conn.close()

def get_all_pokemon():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, type1, type2, moves FROM pokemon")
    pokemon_list = cursor.fetchall()
    conn.close()

    return [{
        "id": p[0],
        "name": p[1],
        "type1": p[2],
        "type2": p[3],
        "moves": json.loads(p[4]) if p[4] else []
    } for p in pokemon_list]

def update_pokemon(pokemon_id, new_data):
    if not new_data:
        return "No updates provided."

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    update_fields = []
    update_values = []

    for key, value in new_data.items():
        if key == "moves":
            value = json.dumps(value)
        update_fields.append(f"{key} = ?")
        update_values.append(value)

    update_values.append(pokemon_id)
    update_query = f"UPDATE pokemon SET {', '.join(update_fields)} WHERE id = ?"

    cursor.execute(update_query, tuple(update_values))
    conn.commit()
    conn.close()

    return "Pokémon updated successfully!"

# demo
if __name__ == "__main__":
    print("\n Initializing Database...")
    init_db()

    print("\n Adding Pokémon...")
    pokemon_list = [
        ("Pikachu", "Electric", None, ["Thunderbolt", "Quick Attack"]),
        ("Charmander", "Fire", None, ["Ember", "Scratch"]),
        ("Bulbasaur", "Grass", "Poison", ["Vine Whip", "Tackle"]),
        ("Eevee", "Normal", None, ["Tackle", "Sand Attack"]),
    ]

    for name, type1, type2, moves in pokemon_list:
        print(add_pokemon(name, type1, type2, moves))

    print("\n Retrieving all Pokémon:")
    for pokemon in get_all_pokemon():
        print(pokemon)

    print("\n Updating Raichu's info...")
    print(update_pokemon(1, {"name": "Raichu", "moves": ["Thunder", "Volt Tackle"]}))


    print("\n Final Pokémon List:")
    for pokemon in get_all_pokemon():
        print(pokemon)
