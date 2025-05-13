import os
import sqlite3
import pytest
import sys
# Přidání cesty k nadřazené složce, kde je co2_logger.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import co2_logger


#from ..rpi import co2_logger
# Název testovací databáze – nebude ovlivňovat produkční
TEST_DB = 'test_co2_data.db'

# === Fixture, která zajistí použití testovací databáze ve všech testech ===
@pytest.fixture(autouse=True)
def use_test_db(monkeypatch):
    # Nahrazení globální proměnné DB_FILE testovací databází
    monkeypatch.setattr(co2_logger, "DB_FILE", TEST_DB)
    yield
    # Po každém testu: smažeme soubor databáze
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

# === Test 1: Inicializace databáze vytvoří potřebnou tabulku ===
def test_database_initialization():
    co2_logger.initialize_database()
    
    # Ověříme, že databázový soubor byl vytvořen
    assert os.path.exists(TEST_DB)

    # Připojení k databázi a kontrola existence tabulky
    with sqlite3.connect(TEST_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='co2_readings'")
        assert cursor.fetchone() is not None  # tabulka existuje

# === Test 2: Zápis jedné hodnoty do databáze ===
def test_write_to_db():
    co2_logger.initialize_database()

    # Zapsání jedné hodnoty CO₂
    co2_logger.write_to_db("2025-01-01 12:00:00", 750)

    # Kontrola, že je hodnota správně uložena
    with sqlite3.connect(TEST_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM co2_readings")
        rows = cursor.fetchall()

        assert len(rows) == 1  # jeden řádek
        assert rows[0][2] == 750  # správná hodnota CO₂

# === Test 3: Simulace měření CO₂ pomocí monkeypatch ===
def test_read_co2_mocked_value(monkeypatch):
    # Nahrazení mh_z19.read tak, aby vracelo pevnou hodnotu
    monkeypatch.setattr(co2_logger.mh_z19, 'read', lambda: {'co2': 880})

    timestamp, co2 = co2_logger.read_co2()

    # Kontrola vrácených hodnot
    assert co2 == 880
    assert timestamp is not None

# === Test 4: Simulace selhání senzoru (vrací None) ===
def test_read_co2_none(monkeypatch):
    # Nahrazení mh_z19.read tak, aby vracelo None
    monkeypatch.setattr(co2_logger.mh_z19, 'read', lambda: None)

    timestamp, co2 = co2_logger.read_co2()

    # Kontrola, že čtení selhalo
    assert co2 is None
