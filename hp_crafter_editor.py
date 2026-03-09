#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exodus DayZ Forge — HP_Crafter Recipe Editor
Developed by CrysT | Version 1.0
Open Source — https://github.com
"""

import sys
import os
import json
import copy

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout,
    QHBoxLayout, QSplitter, QListWidget, QListWidgetItem, QPushButton,
    QLabel, QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QCheckBox,
    QTreeWidget, QTreeWidgetItem, QFileDialog, QMessageBox, QDialog,
    QDialogButtonBox, QFormLayout, QGroupBox, QScrollArea, QFrame,
    QToolButton, QCompleter, QAbstractItemView, QStatusBar,
    QInputDialog, QTextEdit, QHeaderView
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QColor, QPalette

# =============================================================================
# SETTINGS — language preference stored next to the exe / script
# =============================================================================
# Use the directory of the running executable (.exe or .py) as base
_BASE_DIR = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
_SETTINGS_FILE = os.path.join(_BASE_DIR, "forge_settings.json")
_LIBRARY_FILE  = os.path.join(_BASE_DIR, "forge_library.json")
_settings: dict = {"language": "en"}


def _load_settings():
    try:
        if os.path.exists(_SETTINGS_FILE):
            with open(_SETTINGS_FILE, "r", encoding="utf-8") as f:
                _settings.update(json.load(f))
    except Exception:
        pass


def _save_settings():
    try:
        with open(_SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(_settings, f, indent=2)
    except Exception:
        pass


_load_settings()

# =============================================================================
# TRANSLATIONS
# =============================================================================
_T: dict = {
    "en": {
        "window_title":       "Exodus DayZ Forge — HP_Crafter Recipe Editor",
        "no_file":            "No file loaded",
        "btn_new":            "📄 New",
        "btn_open":           "📂 Open",
        "btn_save":           "💾 Save",
        "btn_save_as":        "💾 Save As...",
        "tab_custom":         "⚙ Customization",
        "tab_categories":     "📂 Categories",
        "tab_recipes":        "📋 Recipes",
        "tab_explorer":       "🔍 JSON Explorer",
        "status_ready":       "Ready. Open an HP_Crafter.json or create a new file.",
        "menu_file":          "File",
        "menu_tools":         "Tools",
        "menu_settings":      "Settings",
        "menu_new":           "New",
        "menu_open":          "Open...",
        "menu_save":          "Save",
        "menu_save_as":       "Save As...",
        "menu_exit":          "Exit",
        "menu_validate":      "Validate JSON",
        "menu_scan":          "Scan Classnames from JSON",
        "menu_library":       "Classname Library",
        "menu_language":      "Language",
        "menu_about":         "About...",
        "cat_header":         "Categories",
        "cat_info":           (
            "Select a category from the list.\n\n"
            "Edit its recipes in the 'Recipes' tab.\n\n"
            "💡 Reorder:\n"
            "  • ▲ / ▼ Buttons\n"
            "  • Drag & Drop in the list\n"
            "  • Double-click → jumps to Recipes"
        ),
        "btn_cat_new":        "+ New",
        "btn_cat_del":        "🗑 Delete",
        "btn_cat_rename":     "✏ Rename",
        "btn_up":             "▲ Up",
        "btn_down":           "▼ Down",
        "tt_cat_list":        (
            "Reorder via Drag & Drop or ▲/▼ buttons.\n"
            "Order determines in-game display.\n"
            "Double-click to jump straight to its recipes."
        ),
        "tt_cat_up":          "Move category one position up",
        "tt_cat_down":        "Move category one position down",
        "tt_cat_new":         "Create a new empty category",
        "tt_cat_del":         "Delete selected category and all its recipes",
        "tt_cat_rename":      "Rename the selected category",
        "lbl_category":       "Category:",
        "lbl_recipes":        "Recipes",
        "btn_rec_new":        "+ New",
        "btn_rec_copy":       "📋 Copy",
        "btn_rec_paste":      "📋 Paste",
        "btn_rec_dup":        "⧉ Duplicate",
        "btn_rec_del":        "🗑 Delete",
        "grp_basic":          "Recipe Data",
        "grp_components":     "CraftComponents",
        "grp_attachments":    "AttachmentsNeed",
        "lbl_result":         "Result:",
        "lbl_result_count":   "ResultCount:",
        "lbl_recipe_name":    "RecipeName:",
        "lbl_craft_type":     "CraftType:",
        "lbl_comp_health":    "ComponentsDontAffectHealth:",
        "cb_comp_health":     "Components do not affect health",
        "btn_comp_add":       "+ Add",
        "btn_comp_rem":       "- Remove",
        "tt_result":          (
            "Class name of the result item (must exist in the game).\n"
            "Example: AK74, CopperWire, MetalPlate\n"
            "Tip: Type to filter or click the arrow for the full list."
        ),
        "tt_result_count":    (
            "How many units of the result item are created.\n"
            "Distributed into stacks based on max stack size."
        ),
        "tt_recipe_name":     "Display name shown in the HUD.\nExample: 'Copper Wire'",
        "tt_craft_type":      (
            "Determines which icon is shown in the HUD.\n"
            "Icon images can be customized in the 'Customization' tab."
        ),
        "tt_comp_health":     (
            "✔ ON  (1): Result health is fixed, independent of ingredients.\n"
            "✘ OFF (0): Health is calculated from the ingredient average."
        ),
        "tt_classname":       (
            "Class name of the required component.\n"
            "Example: Pliers, MetalPlate, Hammer\n"
            "Tip: Type to filter or click the arrow for the full list."
        ),
        "tt_amount":          "Required quantity of this component in the Workbench cargo.",
        "tt_destroy":         (
            "✔ ON:  Component is consumed when crafting.\n"
            "✘ OFF: Component is kept (e.g. tools)."
        ),
        "tt_changehealth":    (
            "Health change of the component during crafting.\n"
            "0 = no change  |  -5 = loses 5 HP  |  +10 = gains 10 HP\n"
            "Note: Items have 100 HP total."
        ),
        "tt_comp_dd":         "Drag & Drop rows to reorder components.",
        "tt_att_combo":       (
            "Select a Workbench Attachment from the list\n"
            "or type a custom name."
        ),
        "tt_att_add":         "+ Add selected attachment to the list",
        "tt_att_rem":         "- Remove selected attachment from the list",
        "custom_info":        (
            "Paths to background and icon images (EDDS/PAA format).\n"
            "Empty fields use the mod's built-in fallback images."
        ),
        "tt_browse":          "Select file",
        "tt_preview":         "Preview (PNG/JPG only)",
        "explorer_title":     "JSON Structure Overview (read-only)",
        "explorer_col0":      "Key",
        "explorer_col1":      "Value / Type",
        "dlg_unsaved":        "Unsaved Changes",
        "dlg_unsaved_new":    "There are unsaved changes. Create new file anyway?",
        "dlg_unsaved_open":   "There are unsaved changes. Open file anyway?",
        "dlg_unsaved_exit":   "There are unsaved changes. Really exit?",
        "dlg_invalid_title":  "Invalid File",
        "dlg_invalid_file":   (
            "The file does not contain an 'm_CraftClasses' block.\n"
            "Please select a valid HP_Crafter.json."
        ),
        "dlg_json_error":     "Error parsing JSON file:\n",
        "dlg_load_error":     "File could not be loaded:\n",
        "dlg_save_error":     "File could not be saved:\n",
        "dlg_valid_title":    "Validation",
        "dlg_valid_ok":       "✓ All recipes are valid!",
        "dlg_valid_found":    " problem(s) found:",
        "dlg_valid_save":     "Save anyway?",
        "dlg_scan_title":     "Scan Complete",
        "dlg_scan_new":       "{} new classname(s) added to library.",
        "dlg_scan_none":      "No new classnames found.",
        "dlg_new_cat":        "New Category",
        "dlg_new_cat_lbl":    "Category name:",
        "dlg_rename_cat":     "Rename Category",
        "dlg_rename_cat_lbl": "New name:",
        "dlg_del_cat":        "Delete Category",
        "dlg_del_cat_msg":    "Really delete category '{}'?\nAll contained recipes will be lost!",
        "dlg_del_rec":        "Delete Recipe",
        "dlg_del_rec_msg":    "Really delete recipe '{}'?",
        "dlg_no_cat":         "Please select a category first.",
        "dlg_hint":           "Note",
        "dlg_paste_title":    "Paste Recipe",
        "dlg_paste_lbl":      "Paste '{}' into which category?",
        "dlg_paste_empty":    "No recipe copied yet. Use 'Copy' first.",
        "st_loading":         "Loading {}...",
        "st_loaded":          "Loaded: {} categories, {} recipes.",
        "st_new_cls":         "  —  {} new classname(s) added to library.",
        "st_saved":           "Saved: {}",
        "st_lib_updated":     "  |  Library updated.",
        "st_new_file":        "New empty HP_Crafter file created.",
        "st_new_file_lbl":    "New file (unsaved)",
        "lib_title":          "Classname Library",
        "lib_total":          "Total: {} classnames",
        "lib_rename":         "Rename",
        "lib_delete":         "Delete",
        "lib_rename_title":   "Rename Classname",
        "lib_rename_lbl":     "New name:",
        "lib_del_title":      "Delete Classname",
        "lib_del_msg":        "Delete classname '{}'?",
        "about_title":        "About",
        "about_text":         (
            "Exodus DayZ Forge\n"
            "Developed by CrysT\n"
            "Version 1.0\n\n"
            "Visual Recipe Editor for the DayZ Mod HP_Crafter\n"
            "Supported structure: HP_Crafter.json v1\n\n"
            "Open Source — source code available on GitHub."
        ),
        "lang_title":         "Language Changed",
        "lang_msg":           (
            "Please restart the application to apply the language change."
        ),
    },
    "de": {
        "window_title":       "Exodus DayZ Forge — HP_Crafter Rezept-Editor",
        "no_file":            "Keine Datei geladen",
        "btn_new":            "📄 Neu",
        "btn_open":           "📂 Öffnen",
        "btn_save":           "💾 Speichern",
        "btn_save_as":        "💾 Speichern unter...",
        "tab_custom":         "⚙ Customization",
        "tab_categories":     "📂 Kategorien",
        "tab_recipes":        "📋 Rezepte",
        "tab_explorer":       "🔍 JSON Explorer",
        "status_ready":       "Bereit. Öffne eine HP_Crafter.json oder erstelle eine neue Datei.",
        "menu_file":          "Datei",
        "menu_tools":         "Tools",
        "menu_settings":      "Einstellungen",
        "menu_new":           "Neu",
        "menu_open":          "Öffnen...",
        "menu_save":          "Speichern",
        "menu_save_as":       "Speichern unter...",
        "menu_exit":          "Beenden",
        "menu_validate":      "JSON Validierung",
        "menu_scan":          "Classnames aus JSON scannen",
        "menu_library":       "Classname Bibliothek",
        "menu_language":      "Sprache",
        "menu_about":         "Über...",
        "cat_header":         "Kategorien",
        "cat_info":           (
            "Wähle eine Kategorie aus der Liste.\n\n"
            "Rezepte bearbeitest du im Tab 'Rezepte'.\n\n"
            "💡 Reihenfolge:\n"
            "  • ▲ / ▼ Buttons\n"
            "  • Drag & Drop in der Liste\n"
            "  • Doppelklick → springt zu Rezepten"
        ),
        "btn_cat_new":        "+ Neu",
        "btn_cat_del":        "🗑 Löschen",
        "btn_cat_rename":     "✏ Umbenennen",
        "btn_up":             "▲ Hoch",
        "btn_down":           "▼ Runter",
        "tt_cat_list":        (
            "Per Drag & Drop oder ▲/▼ neu anordnen.\n"
            "Reihenfolge bestimmt Anzeige im Spiel.\n"
            "Doppelklick springt direkt zu den Rezepten."
        ),
        "tt_cat_up":          "Kategorie eine Position nach oben",
        "tt_cat_down":        "Kategorie eine Position nach unten",
        "tt_cat_new":         "Neue leere Kategorie erstellen",
        "tt_cat_del":         "Gewählte Kategorie und alle Rezepte löschen",
        "tt_cat_rename":      "Name der Kategorie ändern",
        "lbl_category":       "Kategorie:",
        "lbl_recipes":        "Rezepte",
        "btn_rec_new":        "+ Neu",
        "btn_rec_copy":       "📋 Kopieren",
        "btn_rec_paste":      "📋 Einfügen",
        "btn_rec_dup":        "⧉ Duplizieren",
        "btn_rec_del":        "🗑 Löschen",
        "grp_basic":          "Rezept-Grunddaten",
        "grp_components":     "CraftComponents",
        "grp_attachments":    "AttachmentsNeed",
        "lbl_result":         "Result:",
        "lbl_result_count":   "ResultCount:",
        "lbl_recipe_name":    "RecipeName:",
        "lbl_craft_type":     "CraftType:",
        "lbl_comp_health":    "ComponentsDontAffectHealth:",
        "cb_comp_health":     "Komponenten beeinflussen Gesundheit nicht",
        "btn_comp_add":       "+ Hinzufügen",
        "btn_comp_rem":       "- Entfernen",
        "tt_result":          (
            "Klassenname des Ergebnis-Items.\n"
            "Beispiel: AK74, CopperWire, MetalPlate\n"
            "Tipp: Tippen zum Filtern."
        ),
        "tt_result_count":    "Anzahl der erzeugten Items.\nWird auf Stacks aufgeteilt.",
        "tt_recipe_name":     "Anzeigename im HUD.\nBeispiel: 'Copper Wire'",
        "tt_craft_type":      (
            "Bestimmt welches Icon im HUD erscheint.\n"
            "Im 'Customization' Tab anpassbar."
        ),
        "tt_comp_health":     (
            "✔ AN  (1): Ergebnis-Health ist fix.\n"
            "✘ AUS (0): Health aus Durchschnitt der Zutaten."
        ),
        "tt_classname":       (
            "Klassenname der Komponente.\n"
            "Beispiel: Pliers, MetalPlate\n"
            "Tipp: Tippen zum Filtern."
        ),
        "tt_amount":          "Benötigte Menge im Workbench-Cargo.",
        "tt_destroy":         (
            "✔ AN:  Wird beim Craften verbraucht.\n"
            "✘ AUS: Bleibt erhalten (Werkzeuge)."
        ),
        "tt_changehealth":    (
            "Gesundheitsänderung beim Craften.\n"
            "0 = keine  |  -5 = verliert 5 HP  |  +10 = erhält 10 HP\n"
            "Hinweis: Items haben 100 HP."
        ),
        "tt_comp_dd":         "Drag & Drop zum Neuanordnen der Komponenten.",
        "tt_att_combo":       "Attachment aus Liste wählen\noder eigenen Namen eingeben.",
        "tt_att_add":         "+ Attachment zur Liste hinzufügen",
        "tt_att_rem":         "- Markiertes Attachment entfernen",
        "custom_info":        (
            "Pfade zu Hintergrund- und Icon-Bildern (EDDS/PAA Format).\n"
            "Leere Felder nutzen den Mod-internen Fallback."
        ),
        "tt_browse":          "Datei auswählen",
        "tt_preview":         "Vorschau (nur PNG/JPG)",
        "explorer_title":     "JSON Struktur Übersicht (read-only)",
        "explorer_col0":      "Schlüssel",
        "explorer_col1":      "Wert / Typ",
        "dlg_unsaved":        "Ungespeicherte Änderungen",
        "dlg_unsaved_new":    "Es gibt ungespeicherte Änderungen. Trotzdem neue Datei erstellen?",
        "dlg_unsaved_open":   "Es gibt ungespeicherte Änderungen. Trotzdem öffnen?",
        "dlg_unsaved_exit":   "Es gibt ungespeicherte Änderungen. Wirklich beenden?",
        "dlg_invalid_title":  "Ungültige Datei",
        "dlg_invalid_file":   (
            "Die Datei enthält keinen 'm_CraftClasses' Block.\n"
            "Bitte wähle eine gültige HP_Crafter.json."
        ),
        "dlg_json_error":     "Fehler beim Parsen der JSON Datei:\n",
        "dlg_load_error":     "Datei konnte nicht geladen werden:\n",
        "dlg_save_error":     "Datei konnte nicht gespeichert werden:\n",
        "dlg_valid_title":    "Validierung",
        "dlg_valid_ok":       "✓ Alle Rezepte sind valide!",
        "dlg_valid_found":    " Problem(e) gefunden:",
        "dlg_valid_save":     "Trotzdem speichern?",
        "dlg_scan_title":     "Scan abgeschlossen",
        "dlg_scan_new":       "{} neue Classname(s) zur Bibliothek hinzugefügt.",
        "dlg_scan_none":      "Keine neuen Classnames gefunden.",
        "dlg_new_cat":        "Neue Kategorie",
        "dlg_new_cat_lbl":    "Kategoriename:",
        "dlg_rename_cat":     "Kategorie umbenennen",
        "dlg_rename_cat_lbl": "Neuer Name:",
        "dlg_del_cat":        "Kategorie löschen",
        "dlg_del_cat_msg":    "Kategorie '{}' wirklich löschen?\nAlle enthaltenen Rezepte gehen verloren!",
        "dlg_del_rec":        "Rezept löschen",
        "dlg_del_rec_msg":    "Rezept '{}' wirklich löschen?",
        "dlg_no_cat":         "Bitte zuerst eine Kategorie auswählen.",
        "dlg_hint":           "Hinweis",
        "dlg_paste_title":    "Rezept einfügen",
        "dlg_paste_lbl":      "'{}' in welche Kategorie einfügen?",
        "dlg_paste_empty":    "Noch kein Rezept kopiert. Bitte zuerst 'Kopieren' verwenden.",
        "st_loading":         "Lade {}...",
        "st_loaded":          "Geladen: {} Kategorien, {} Rezepte.",
        "st_new_cls":         "  —  {} neue Classname(s) zur Bibliothek hinzugefügt.",
        "st_saved":           "Gespeichert: {}",
        "st_lib_updated":     "  |  Bibliothek aktualisiert.",
        "st_new_file":        "Neue leere HP_Crafter Datei erstellt.",
        "st_new_file_lbl":    "Neue Datei (ungespeichert)",
        "lib_title":          "Classname Bibliothek",
        "lib_total":          "Gesamt: {} Classnames",
        "lib_rename":         "Umbenennen",
        "lib_delete":         "Löschen",
        "lib_rename_title":   "Classname umbenennen",
        "lib_rename_lbl":     "Neuer Name:",
        "lib_del_title":      "Classname löschen",
        "lib_del_msg":        "Classname '{}' löschen?",
        "about_title":        "Über",
        "about_text":         (
            "Exodus DayZ Forge\n"
            "Entwickelt von CrysT\n"
            "Version 1.0\n\n"
            "Visueller Rezept-Editor für die DayZ Mod HP_Crafter\n"
            "Unterstützte Struktur: HP_Crafter.json v1\n\n"
            "Open Source — Quellcode auf GitHub verfügbar."
        ),
        "lang_title":         "Sprache geändert",
        "lang_msg":           "Bitte starte die Anwendung neu, um die Sprache zu übernehmen.",
    }
}


def TR(key: str) -> str:
    """Return translated string for the currently active language."""
    lang = _settings.get("language", "en")
    return _T.get(lang, _T["en"]).get(key, _T["en"].get(key, key))


# =============================================================================
# CLASSNAME LIBRARY  (auto-extended on every save)
# =============================================================================
CLASSNAME_LIBRARY = {
    "results": [
        "AK74",
        "AK101",
        "M4A1",
        "SKS",
        "Mosin9130",
        "CZ527",
        "Winchester70",
        "CopperWire",
        "MetalPlate",
        "MetalWire",
        "Nail",
        "Plank",
        "Rope",
        "BarbedWire",
        "FieldShovel",
        "Hacksaw",
        "Hammer",
        "Hatchet",
        "Knife",
        "Pliers",
        "Screwdriver",
        "Wrench",
        "HandDrillKit",
        "ArmBandage",
        "Bandage",
        "Epinephrine",
        "Morphine",
        "Tetracycline",
        "Vitamins",
        "Battery9V",
        "BatteryD",
        "CanOpener",
        "CookingPot",
        "KitchenKnife",
        "LongRangeScope",
        "PistolSuppressor",
        "RiffleSuppressor",
        "TacticalBaconCan",
        "WalkieTalkie",
        "HP_HeavyPart",
        "TLS_Mednaya_provoloka",
        "TLS_MetalSheet",
        "TLS_Bolt",
        "TLS_Screw"
    ],
    "components": [
        "Pliers",
        "Hammer",
        "Hacksaw",
        "Screwdriver",
        "Wrench",
        "Hatchet",
        "KitchenKnife",
        "Knife",
        "HandDrillKit",
        "MetalPlate",
        "MetalWire",
        "Nail",
        "Plank",
        "Rope",
        "BarbedWire",
        "Rag",
        "LeatherSewing",
        "SewingKit",
        "BoneKnife",
        "StoneKnife",
        "CookingPot",
        "Battery9V",
        "BatteryD",
        "ElectronicComponents",
        "TLS_Datchik3",
        "TLS_DeviceA",
        "TLS_MetalScrap",
        "TLS_WoodPlank",
        "TLS_Provoloka",
        "CanOpener",
        "GasolineCanister",
        "Alkohol",
        "DisinfectantSpray",
        "Zelenka",
        "WoodBlock",
        "WoodStick",
        "SmallStone",
        "Stone",
        "ChestHolster",
        "BackpackLargeHunter",
        "PlasticBottle",
        "IronIngot",
        "CopperIngot"
    ]
}

# =============================================================================
# CRAFT TYPES
# =============================================================================
CRAFT_TYPES = [
    "repairpic", "paintpic", "ammopic", "weaponpic", "toolspic",
    "craftpic", "sewingkitpic", "buildingpic", "carpic", "furniturepic",
    "medicpic", "bookpic", "housepic", "donatepic", "voltagepic"
]

# =============================================================================
# WORKBENCH ATTACHMENTS
# HP_* = mod-specific items   |   no prefix = vanilla DayZ items
# =============================================================================
WORKBENCH_ATTACHMENTS = [
    # HP_ mod items
    "HP_Anvil", "HP_Drill", "HP_Grinde", "HP_napilnik", "HP_Oiler",
    "HP_Vise", "HP_Payalnik", "HP_Tester", "HP_Pipe",
    # Vanilla DayZ items (no HP_ prefix)
    "Crowbar", "FarmingHoe", "FirefighterAxe", "Hacksaw", "Hammer",
    "HandSaw", "Hatchet", "LugWrench", "Nails", "Pickaxe",
    "Pipewrench", "Pliers", "Screwdriver", "Shovel", "MetalPlate",
    "SledgeHammer", "WoodAxe", "Wrench",
]

# =============================================================================
# CUSTOMIZATION FIELDS
# =============================================================================
CUSTOMIZATION_FIELDS = [
    "PathToMainBackgroundImg", "PathTorepairpicImg", "PathTopaintpicImg",
    "PathToammopicImg", "PathToweaponpicImg", "PathTotoolspicImg",
    "PathTocraftpicImg", "PathTosewingkitpicImg", "PathTobuildingpicImg",
    "PathTocarpicImg", "PathTofurniturepicImg", "PathTomedicpicImg",
    "PathTobookpicImg", "PathTohousepicImg", "PathTodonatepicImg",
    "PathTovoltagepicImg",
]

# =============================================================================
# DATA MODEL
# =============================================================================
def default_data() -> dict:
    return {
        "m_CraftClasses": {
            "m_CustomizationSetting": {f: "" for f in CUSTOMIZATION_FIELDS},
            "WorkbenchesClassnames": ["HP_Crafter"],
            "CraftCategories": []
        }
    }


def default_recipe() -> dict:
    return {
        "Result": "", "ResultCount": 1, "ComponentsDontAffectHealth": 0,
        "CraftType": "craftpic", "RecipeName": "",
        "CraftComponents": [], "AttachmentsNeed": []
    }


def default_component() -> dict:
    return {"Classname": "", "Amount": 1, "Destroy": 1, "Changehealth": 0.0}


# =============================================================================
# CLASSNAME HELPERS
# =============================================================================
def get_all_classnames() -> list:
    return sorted(set(CLASSNAME_LIBRARY["results"]) | set(CLASSNAME_LIBRARY["components"]))


def add_to_library(classname: str, category: str = "components") -> bool:
    if not classname:
        return False
    lst = CLASSNAME_LIBRARY.setdefault(category, [])
    if classname not in lst:
        lst.append(classname)
        return True
    return False


def scan_classnames_from_data(data: dict) -> int:
    """Scan all classnames from loaded JSON and add new ones to the library."""
    new_count = 0
    for cat in data.get("m_CraftClasses", {}).get("CraftCategories", []):
        for item in cat.get("CraftItems", []):
            if add_to_library(item.get("Result", ""), "results"):
                new_count += 1
            for comp in item.get("CraftComponents", []):
                if add_to_library(comp.get("Classname", ""), "components"):
                    new_count += 1
    return new_count


def load_library_from_file():
    """Load forge_library.json if it exists and merge into CLASSNAME_LIBRARY."""
    try:
        if os.path.exists(_LIBRARY_FILE):
            with open(_LIBRARY_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            for category, names in saved.items():
                lst = CLASSNAME_LIBRARY.setdefault(category, [])
                for name in names:
                    if name and name not in lst:
                        lst.append(name)
    except Exception as e:
        print(f"Library load failed: {e}")


def save_library_to_file() -> bool:
    """Save the current CLASSNAME_LIBRARY to forge_library.json next to the exe."""
    try:
        with open(_LIBRARY_FILE, "w", encoding="utf-8") as f:
            json.dump(CLASSNAME_LIBRARY, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Library save failed: {e}")
    return False


# =============================================================================
# VALIDATION
# =============================================================================
def validate_recipe(recipe: dict) -> list:
    errors = []
    if not recipe.get("Result", "").strip():
        errors.append("Result must not be empty.")
    if recipe.get("ResultCount", 0) < 1:
        errors.append("ResultCount must be >= 1.")
    components = recipe.get("CraftComponents", [])
    if not components:
        errors.append("CraftComponents must not be empty (at least 1 component required).")
    for i, comp in enumerate(components):
        if not comp.get("Classname", "").strip():
            errors.append(f"Component {i + 1}: Classname must not be empty.")
        if comp.get("Amount", 0) < 1:
            errors.append(f"Component {i + 1}: Amount must be >= 1.")
    craft_type = recipe.get("CraftType", "")
    if craft_type and craft_type not in CRAFT_TYPES:
        errors.append(f"CraftType '{craft_type}' is not a known value (warning only).")
    return errors


# =============================================================================
# RECIPE LIST WIDGET  (drag & drop)
# =============================================================================
class RecipeListWidget(QListWidget):
    order_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.model().rowsMoved.connect(self.order_changed)


# =============================================================================
# COMPONENTS EDITOR  (with drag & drop reorder)
# =============================================================================
class ComponentsEditorWidget(QWidget):
    changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._components: list = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        toolbar = QHBoxLayout()
        self.btn_add = QPushButton(TR("btn_comp_add"))
        self.btn_add.setFixedHeight(28)
        self.btn_rem = QPushButton(TR("btn_comp_rem"))
        self.btn_rem.setFixedHeight(28)
        toolbar.addWidget(self.btn_add)
        toolbar.addWidget(self.btn_rem)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        self.list_widget = QListWidget()
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.list_widget.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.list_widget.setToolTip(TR("tt_comp_dd"))
        self.list_widget.model().rowsMoved.connect(self._on_drag_reorder)
        layout.addWidget(self.list_widget)

        self.btn_add.clicked.connect(self._add_component)
        self.btn_rem.clicked.connect(self._remove_selected)

    def _make_row_widget(self, comp: dict, index: int) -> QWidget:
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(4, 2, 4, 2)
        h.setSpacing(6)

        lbl_idx = QLabel(str(index + 1))
        lbl_idx.setFixedWidth(20)
        lbl_idx.setStyleSheet("color: #585b70;")

        all_names = get_all_classnames()
        cn_cb = QComboBox()
        cn_cb.setEditable(True)
        cn_cb.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        cn_cb.addItems(all_names)
        cn_cb.setCurrentText(comp.get("Classname", ""))
        cn_cb.setMinimumWidth(160)
        cn_cb.setToolTip(TR("tt_classname"))
        _cmp = QCompleter(all_names)
        _cmp.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        _cmp.setFilterMode(Qt.MatchFlag.MatchContains)
        cn_cb.setCompleter(_cmp)

        amt = QSpinBox()
        amt.setRange(1, 9999)
        amt.setValue(comp.get("Amount", 1))
        amt.setFixedWidth(62)
        amt.setPrefix("×")
        amt.setToolTip(TR("tt_amount"))

        destroy_cb = QCheckBox("Destroy")
        destroy_cb.setChecked(bool(comp.get("Destroy", 1)))
        destroy_cb.setToolTip(TR("tt_destroy"))

        # Step 5.0 — items have 100 HP total
        ch = QDoubleSpinBox()
        ch.setRange(-100.0, 100.0)
        ch.setValue(float(comp.get("Changehealth", 0.0)))
        ch.setSingleStep(5.0)
        ch.setDecimals(1)
        ch.setFixedWidth(82)
        ch.setPrefix("HP:")
        ch.setToolTip(TR("tt_changehealth"))

        h.addWidget(lbl_idx)
        h.addWidget(cn_cb)
        h.addWidget(amt)
        h.addWidget(destroy_cb)
        h.addWidget(ch)

        def _update():
            if index < len(self._components):
                self._components[index]["Classname"] = cn_cb.currentText().strip()
                self._components[index]["Amount"] = amt.value()
                self._components[index]["Destroy"] = 1 if destroy_cb.isChecked() else 0
                self._components[index]["Changehealth"] = ch.value()
                self.changed.emit()

        cn_cb.currentTextChanged.connect(_update)
        amt.valueChanged.connect(_update)
        destroy_cb.stateChanged.connect(_update)
        ch.valueChanged.connect(_update)
        return w

    def _read_components_from_widgets(self) -> list:
        """Read all component values directly from row widgets (used after D&D)."""
        components = []
        for i in range(self.list_widget.count()):
            w = self.list_widget.itemWidget(self.list_widget.item(i))
            if not w:
                continue
            layout = w.layout()
            cn_cb = amt = destroy_cb = ch = None
            for j in range(layout.count()):
                widget = layout.itemAt(j).widget()
                if isinstance(widget, QComboBox):
                    cn_cb = widget
                elif isinstance(widget, QSpinBox):
                    amt = widget
                elif isinstance(widget, QCheckBox):
                    destroy_cb = widget
                elif isinstance(widget, QDoubleSpinBox):
                    ch = widget
            if cn_cb and amt and destroy_cb and ch:
                components.append({
                    "Classname": cn_cb.currentText().strip(),
                    "Amount": amt.value(),
                    "Destroy": 1 if destroy_cb.isChecked() else 0,
                    "Changehealth": ch.value()
                })
        return components

    def _on_drag_reorder(self):
        """After D&D: sync model from widgets, rebuild to fix index labels."""
        self._components = self._read_components_from_widgets()
        self._rebuild_list()
        self.changed.emit()

    def _add_component(self):
        self._components.append(default_component())
        self._rebuild_list()
        self.changed.emit()

    def _remove_selected(self):
        row = self.list_widget.currentRow()
        if 0 <= row < len(self._components):
            self._components.pop(row)
            self._rebuild_list()
            self.changed.emit()

    def _rebuild_list(self):
        self.list_widget.clear()
        for i, comp in enumerate(self._components):
            item = QListWidgetItem()
            w = self._make_row_widget(comp, i)
            item.setSizeHint(w.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, w)

    def set_components(self, components: list):
        self._components = copy.deepcopy(components)
        self._rebuild_list()

    def get_components(self) -> list:
        return copy.deepcopy(self._components)


# =============================================================================
# ATTACHMENTS EDITOR
# =============================================================================
class AttachmentsEditorWidget(QWidget):
    changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._attachments: list = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        toolbar = QHBoxLayout()
        self.combo_add = QComboBox()
        self.combo_add.setEditable(True)
        self.combo_add.addItems(WORKBENCH_ATTACHMENTS)
        self.combo_add.setCurrentText("")
        self.combo_add.setFixedHeight(28)
        self.combo_add.setToolTip(TR("tt_att_combo"))

        btn_add = QPushButton("+")
        btn_add.setFixedSize(28, 28)
        btn_add.setToolTip(TR("tt_att_add"))

        btn_rem = QPushButton("-")
        btn_rem.setFixedSize(28, 28)
        btn_rem.setToolTip(TR("tt_att_rem"))

        toolbar.addWidget(self.combo_add)
        toolbar.addWidget(btn_add)
        toolbar.addWidget(btn_rem)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        self.list_widget = QListWidget()
        self.list_widget.setFixedHeight(100)
        layout.addWidget(self.list_widget)

        btn_add.clicked.connect(self._add_attachment)
        btn_rem.clicked.connect(self._remove_selected)

    def _add_attachment(self):
        val = self.combo_add.currentText().strip()
        if val and val not in self._attachments:
            self._attachments.append(val)
            self.list_widget.addItem(val)
            self.combo_add.setCurrentText("")
            self.changed.emit()

    def _remove_selected(self):
        row = self.list_widget.currentRow()
        if 0 <= row < len(self._attachments):
            self._attachments.pop(row)
            self.list_widget.takeItem(row)
            self.changed.emit()

    def set_attachments(self, attachments: list):
        self._attachments = list(attachments)
        self.list_widget.clear()
        for a in self._attachments:
            self.list_widget.addItem(a)

    def get_attachments(self) -> list:
        return list(self._attachments)


# =============================================================================
# RECIPE DETAIL EDITOR
# =============================================================================
class RecipeDetailEditor(QWidget):
    recipe_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._recipe = None
        self._ignore = False
        self._setup_ui()
        self.set_enabled(False)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(12)

        # Basic data
        grp_basic = QGroupBox(TR("grp_basic"))
        form = QFormLayout(grp_basic)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.result_edit = QComboBox()
        self.result_edit.setEditable(True)
        self.result_edit.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.result_edit.addItems(sorted(set(CLASSNAME_LIBRARY["results"])))
        self.result_edit.setCurrentText("")
        self.result_edit.setToolTip(TR("tt_result"))
        _cr = QCompleter(sorted(set(CLASSNAME_LIBRARY["results"])))
        _cr.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        _cr.setFilterMode(Qt.MatchFlag.MatchContains)
        self.result_edit.setCompleter(_cr)
        form.addRow(TR("lbl_result"), self.result_edit)

        self.result_count = QSpinBox()
        self.result_count.setRange(1, 9999)
        self.result_count.setToolTip(TR("tt_result_count"))
        form.addRow(TR("lbl_result_count"), self.result_count)

        self.recipe_name = QLineEdit()
        self.recipe_name.setToolTip(TR("tt_recipe_name"))
        form.addRow(TR("lbl_recipe_name"), self.recipe_name)

        self.craft_type = QComboBox()
        self.craft_type.addItems(CRAFT_TYPES)
        self.craft_type.setToolTip(TR("tt_craft_type"))
        form.addRow(TR("lbl_craft_type"), self.craft_type)

        self.comp_health_cb = QCheckBox(TR("cb_comp_health"))
        self.comp_health_cb.setToolTip(TR("tt_comp_health"))
        form.addRow(TR("lbl_comp_health"), self.comp_health_cb)

        layout.addWidget(grp_basic)

        grp_comp = QGroupBox(TR("grp_components"))
        comp_layout = QVBoxLayout(grp_comp)
        self.components_editor = ComponentsEditorWidget()
        comp_layout.addWidget(self.components_editor)
        layout.addWidget(grp_comp)

        grp_att = QGroupBox(TR("grp_attachments"))
        att_layout = QVBoxLayout(grp_att)
        self.attachments_editor = AttachmentsEditorWidget()
        att_layout.addWidget(self.attachments_editor)
        layout.addWidget(grp_att)

        layout.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        self.result_edit.currentTextChanged.connect(self._on_changed)
        self.result_count.valueChanged.connect(self._on_changed)
        self.recipe_name.textChanged.connect(self._on_changed)
        self.craft_type.currentTextChanged.connect(self._on_changed)
        self.comp_health_cb.stateChanged.connect(self._on_changed)
        self.components_editor.changed.connect(self._on_components_changed)
        self.attachments_editor.changed.connect(self._on_attachments_changed)

    def _on_changed(self):
        if self._ignore or self._recipe is None:
            return
        self._recipe["Result"] = self.result_edit.currentText().strip()
        self._recipe["ResultCount"] = self.result_count.value()
        self._recipe["RecipeName"] = self.recipe_name.text().strip()
        self._recipe["CraftType"] = self.craft_type.currentText()
        self._recipe["ComponentsDontAffectHealth"] = 1 if self.comp_health_cb.isChecked() else 0
        self.recipe_changed.emit()

    def _on_components_changed(self):
        if self._recipe is None:
            return
        self._recipe["CraftComponents"] = self.components_editor.get_components()
        self.recipe_changed.emit()

    def _on_attachments_changed(self):
        if self._recipe is None:
            return
        self._recipe["AttachmentsNeed"] = self.attachments_editor.get_attachments()
        self.recipe_changed.emit()

    def load_recipe(self, recipe: dict):
        self._recipe = recipe
        self._ignore = True
        self.result_edit.setCurrentText(recipe.get("Result", ""))
        self.result_count.setValue(recipe.get("ResultCount", 1))
        self.recipe_name.setText(recipe.get("RecipeName", ""))
        ct = recipe.get("CraftType", "craftpic")
        idx = self.craft_type.findText(ct)
        self.craft_type.setCurrentIndex(idx if idx >= 0 else 0)
        self.comp_health_cb.setChecked(bool(recipe.get("ComponentsDontAffectHealth", 0)))
        self.components_editor.set_components(recipe.get("CraftComponents", []))
        self.attachments_editor.set_attachments(recipe.get("AttachmentsNeed", []))
        self._ignore = False
        self.set_enabled(True)

    def clear(self):
        self._recipe = None
        self.set_enabled(False)

    def set_enabled(self, enabled: bool):
        for w in [self.result_edit, self.result_count, self.recipe_name,
                  self.craft_type, self.comp_health_cb,
                  self.components_editor, self.attachments_editor]:
            w.setEnabled(enabled)


# =============================================================================
# TAB: CUSTOMIZATION
# =============================================================================
class CustomizationTab(QWidget):
    changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._data: dict = {}
        self._path_edits: dict = {}
        self._preview_labels: dict = {}
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        lbl = QLabel(TR("custom_info"))
        lbl.setWordWrap(True)
        lbl.setStyleSheet("color: #a6adc8; margin-bottom: 8px;")
        layout.addWidget(lbl)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        container = QWidget()
        form = QFormLayout(container)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setSpacing(8)

        for field in CUSTOMIZATION_FIELDS:
            row_w = QWidget()
            row_h = QHBoxLayout(row_w)
            row_h.setContentsMargins(0, 0, 0, 0)
            row_h.setSpacing(4)

            edit = QLineEdit()
            edit.setPlaceholderText("path/to/image.edds")
            edit.textChanged.connect(lambda text, f=field: self._on_path_changed(f, text))

            btn = QToolButton()
            btn.setText("📁")
            btn.setToolTip(TR("tt_browse"))
            btn.clicked.connect(lambda checked=False, e=edit: self._browse_file(e))

            preview = QLabel()
            preview.setFixedSize(32, 32)
            preview.setStyleSheet("border:1px solid #555; background:#222;")
            preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
            preview.setToolTip(TR("tt_preview"))

            row_h.addWidget(edit)
            row_h.addWidget(btn)
            row_h.addWidget(preview)

            label = field.replace("PathTo", "").replace("Img", "")
            form.addRow(f"{label}:", row_w)
            self._path_edits[field] = edit
            self._preview_labels[field] = preview

        scroll.setWidget(container)
        layout.addWidget(scroll)

    def _browse_file(self, edit: QLineEdit):
        path, _ = QFileDialog.getOpenFileName(
            self, TR("tt_browse"), "",
            "Image files (*.edds *.paa *.png *.jpg *.jpeg *.bmp);;All files (*)"
        )
        if path:
            edit.setText(path)

    def _on_path_changed(self, field: str, text: str):
        self._data[field] = text
        lbl = self._preview_labels.get(field)
        if lbl:
            ext = os.path.splitext(text)[1].lower() if text else ""
            if text and os.path.exists(text) and ext in (".png", ".jpg", ".jpeg", ".bmp"):
                pix = QPixmap(text)
                if not pix.isNull():
                    lbl.setPixmap(pix.scaled(
                        32, 32, Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    ))
                else:
                    lbl.clear()
                    lbl.setText("?")
            else:
                lbl.clear()
                lbl.setText("?")
        self.changed.emit()

    def load_data(self, customization: dict):
        self._data = dict(customization)
        for field, edit in self._path_edits.items():
            val = customization.get(field, "")
            edit.blockSignals(True)
            edit.setText(val)
            edit.blockSignals(False)
            self._on_path_changed(field, val)

    def get_data(self) -> dict:
        return dict(self._data)


# =============================================================================
# TAB: CATEGORIES
# =============================================================================
class CategoriesTab(QWidget):
    category_double_clicked = Signal(int)
    changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._categories: list = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)

        left = QWidget()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 0, 0)
        ll.setSpacing(6)

        lbl = QLabel(TR("cat_header"))
        lbl.setStyleSheet("font-weight: bold; font-size: 13px;")
        ll.addWidget(lbl)

        self.cat_list = QListWidget()
        self.cat_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.cat_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.cat_list.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.cat_list.setToolTip(TR("tt_cat_list"))
        self.cat_list.model().rowsMoved.connect(self._on_drag_reorder)
        ll.addWidget(self.cat_list)

        order_row = QHBoxLayout()
        self.btn_up = QPushButton(TR("btn_up"))
        self.btn_down = QPushButton(TR("btn_down"))
        self.btn_up.setFixedHeight(26)
        self.btn_down.setFixedHeight(26)
        self.btn_up.setToolTip(TR("tt_cat_up"))
        self.btn_down.setToolTip(TR("tt_cat_down"))
        order_row.addWidget(self.btn_up)
        order_row.addWidget(self.btn_down)
        ll.addLayout(order_row)

        btn_row = QHBoxLayout()
        self.btn_new = QPushButton(TR("btn_cat_new"))
        self.btn_del = QPushButton(TR("btn_cat_del"))
        self.btn_rename = QPushButton(TR("btn_cat_rename"))
        self.btn_new.setToolTip(TR("tt_cat_new"))
        self.btn_del.setToolTip(TR("tt_cat_del"))
        self.btn_rename.setToolTip(TR("tt_cat_rename"))
        for b in [self.btn_new, self.btn_del, self.btn_rename]:
            b.setFixedHeight(28)
            btn_row.addWidget(b)
        ll.addLayout(btn_row)

        left.setMaximumWidth(300)
        layout.addWidget(left)

        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(12, 0, 0, 0)
        info = QLabel(TR("cat_info"))
        info.setWordWrap(True)
        info.setStyleSheet("color: #a6adc8;")
        info.setAlignment(Qt.AlignmentFlag.AlignTop)
        rl.addWidget(info)
        rl.addStretch()
        layout.addWidget(right, 1)

        self.cat_list.itemDoubleClicked.connect(
            lambda item: self.category_double_clicked.emit(self.cat_list.row(item))
        )
        self.btn_new.clicked.connect(self._new_category)
        self.btn_del.clicked.connect(self._delete_category)
        self.btn_rename.clicked.connect(self._rename_category)
        self.btn_up.clicked.connect(self._move_up)
        self.btn_down.clicked.connect(self._move_down)

    def _move_up(self):
        row = self.cat_list.currentRow()
        if row <= 0:
            return
        self._categories[row - 1], self._categories[row] = (
            self._categories[row], self._categories[row - 1]
        )
        item = self.cat_list.takeItem(row)
        self.cat_list.insertItem(row - 1, item)
        self.cat_list.setCurrentRow(row - 1)
        self.changed.emit()

    def _move_down(self):
        row = self.cat_list.currentRow()
        if row < 0 or row >= len(self._categories) - 1:
            return
        self._categories[row], self._categories[row + 1] = (
            self._categories[row + 1], self._categories[row]
        )
        item = self.cat_list.takeItem(row)
        self.cat_list.insertItem(row + 1, item)
        self.cat_list.setCurrentRow(row + 1)
        self.changed.emit()

    def _on_drag_reorder(self):
        name_to_cat = {c["CategoryName"]: c for c in self._categories}
        new_order = []
        for i in range(self.cat_list.count()):
            name = self.cat_list.item(i).text()
            if name in name_to_cat:
                new_order.append(name_to_cat[name])
        self._categories.clear()
        self._categories.extend(new_order)
        self.changed.emit()

    def _new_category(self):
        name, ok = QInputDialog.getText(self, TR("dlg_new_cat"), TR("dlg_new_cat_lbl"))
        if ok and name.strip():
            self._categories.append({"CategoryName": name.strip(), "CraftItems": []})
            self.cat_list.addItem(name.strip())
            self.cat_list.setCurrentRow(len(self._categories) - 1)
            self.changed.emit()

    def _delete_category(self):
        row = self.cat_list.currentRow()
        if row < 0:
            return
        cat_name = self._categories[row]["CategoryName"]
        reply = QMessageBox.question(
            self, TR("dlg_del_cat"),
            TR("dlg_del_cat_msg").format(cat_name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._categories.pop(row)
            self.cat_list.takeItem(row)
            self.changed.emit()

    def _rename_category(self):
        row = self.cat_list.currentRow()
        if row < 0:
            return
        old = self._categories[row]["CategoryName"]
        name, ok = QInputDialog.getText(
            self, TR("dlg_rename_cat"), TR("dlg_rename_cat_lbl"), text=old
        )
        if ok and name.strip():
            self._categories[row]["CategoryName"] = name.strip()
            self.cat_list.item(row).setText(name.strip())
            self.changed.emit()

    def load_categories(self, categories: list):
        self._categories = categories
        self.cat_list.clear()
        for cat in categories:
            self.cat_list.addItem(cat.get("CategoryName", "(unnamed)"))

    def get_categories(self) -> list:
        return self._categories


# =============================================================================
# TAB: RECIPES
# =============================================================================
class RecipesTab(QWidget):
    changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._categories: list = []
        self._recipe_clipboard = None   # cross-category copy/paste
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        top_bar = QHBoxLayout()
        top_bar.addWidget(QLabel(TR("lbl_category")))
        self.cat_combo = QComboBox()
        self.cat_combo.setMinimumWidth(200)
        top_bar.addWidget(self.cat_combo)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        left_widget = QWidget()
        ll = QVBoxLayout(left_widget)
        ll.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel(TR("lbl_recipes"))
        lbl.setStyleSheet("font-weight: bold;")
        ll.addWidget(lbl)

        self.recipe_list = RecipeListWidget()
        self.recipe_list.setMinimumWidth(200)
        ll.addWidget(self.recipe_list)

        btn_row1 = QHBoxLayout()
        self.btn_add   = QPushButton(TR("btn_rec_new"))
        self.btn_copy  = QPushButton(TR("btn_rec_copy"))
        self.btn_paste = QPushButton(TR("btn_rec_paste"))
        self.btn_dup   = QPushButton(TR("btn_rec_dup"))
        self.btn_del   = QPushButton(TR("btn_rec_del"))
        self.btn_paste.setEnabled(False)
        self.btn_copy.setToolTip(
            "Copy this recipe so it can be pasted into any other category."
        )
        self.btn_paste.setToolTip(
            "Paste the copied recipe — choose target category in the dialog."
        )
        for b in [self.btn_add, self.btn_copy, self.btn_paste, self.btn_dup, self.btn_del]:
            b.setFixedHeight(28)
            btn_row1.addWidget(b)
        ll.addLayout(btn_row1)

        btn_row2 = QHBoxLayout()
        self.btn_up   = QPushButton(TR("btn_up"))
        self.btn_down = QPushButton(TR("btn_down"))
        self.btn_up.setFixedHeight(28)
        self.btn_down.setFixedHeight(28)
        btn_row2.addWidget(self.btn_up)
        btn_row2.addWidget(self.btn_down)
        btn_row2.addStretch()
        ll.addLayout(btn_row2)

        left_widget.setMinimumWidth(200)
        left_widget.setMaximumWidth(340)
        splitter.addWidget(left_widget)

        right_widget = QWidget()
        rl = QVBoxLayout(right_widget)
        rl.setContentsMargins(0, 0, 0, 0)
        self.detail_editor = RecipeDetailEditor()
        rl.addWidget(self.detail_editor)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter, 1)

        self.cat_combo.currentIndexChanged.connect(self._on_category_changed)
        self.recipe_list.currentRowChanged.connect(self._on_recipe_selected)
        self.recipe_list.order_changed.connect(self._on_order_changed)
        self.btn_add.clicked.connect(self._add_recipe)
        self.btn_copy.clicked.connect(self._copy_recipe)
        self.btn_paste.clicked.connect(self._paste_recipe)
        self.btn_dup.clicked.connect(self._duplicate_recipe)
        self.btn_del.clicked.connect(self._delete_recipe)
        self.btn_up.clicked.connect(self._move_up)
        self.btn_down.clicked.connect(self._move_down)
        self.detail_editor.recipe_changed.connect(self._on_recipe_edited)

    def _get_current_category(self):
        idx = self.cat_combo.currentIndex()
        return self._categories[idx] if 0 <= idx < len(self._categories) else None

    @staticmethod
    def _recipe_display(recipe: dict) -> str:
        result = recipe.get("Result", "(no result)")
        name = recipe.get("RecipeName", "")
        return f"{result}  [{name}]" if name else result

    def _refresh_recipe_list(self):
        self.recipe_list.blockSignals(True)
        old_row = self.recipe_list.currentRow()
        self.recipe_list.clear()
        cat = self._get_current_category()
        if cat:
            for item in cat.get("CraftItems", []):
                self.recipe_list.addItem(self._recipe_display(item))
        self.recipe_list.blockSignals(False)
        count = self.recipe_list.count()
        if count > 0:
            self.recipe_list.setCurrentRow(max(0, min(old_row, count - 1)))

    def _on_category_changed(self, _idx: int):
        self.detail_editor.clear()
        self._refresh_recipe_list()

    def _on_recipe_selected(self, row: int):
        cat = self._get_current_category()
        if cat and 0 <= row < len(cat.get("CraftItems", [])):
            self.detail_editor.load_recipe(cat["CraftItems"][row])
        else:
            self.detail_editor.clear()

    def _on_order_changed(self):
        """Sync data model after drag & drop reorder in recipe list."""
        cat = self._get_current_category()
        if not cat:
            return
        items = cat.get("CraftItems", [])
        new_order = []
        for i in range(self.recipe_list.count()):
            text = self.recipe_list.item(i).text()
            for it in items:
                if self._recipe_display(it) == text and it not in new_order:
                    new_order.append(it)
                    break
        cat["CraftItems"] = new_order
        self.changed.emit()

    def _add_recipe(self):
        cat = self._get_current_category()
        if not cat:
            QMessageBox.information(self, TR("dlg_hint"), TR("dlg_no_cat"))
            return
        recipe = default_recipe()
        cat.setdefault("CraftItems", []).append(recipe)
        self._refresh_recipe_list()
        self.recipe_list.setCurrentRow(len(cat["CraftItems"]) - 1)
        self.changed.emit()

    def _copy_recipe(self):
        row = self.recipe_list.currentRow()
        cat = self._get_current_category()
        if not cat or row < 0:
            return
        items = cat.get("CraftItems", [])
        if row < len(items):
            self._recipe_clipboard = copy.deepcopy(items[row])
            self.btn_paste.setEnabled(True)
            result = self._recipe_clipboard.get("Result", "?")
            self.btn_paste.setToolTip(
                f"Paste '{result}' — choose target category in the dialog."
            )

    def _paste_recipe(self):
        if not self._recipe_clipboard:
            QMessageBox.information(self, TR("dlg_paste_title"), TR("dlg_paste_empty"))
            return
        if not self._categories:
            return
        cat_names = [c.get("CategoryName", "(unnamed)") for c in self._categories]
        name, ok = QInputDialog.getItem(
            self, TR("dlg_paste_title"),
            TR("dlg_paste_lbl").format(self._recipe_clipboard.get("Result", "?")),
            cat_names, 0, False
        )
        if ok and name:
            target_idx = cat_names.index(name)
            target_cat = self._categories[target_idx]
            pasted = copy.deepcopy(self._recipe_clipboard)
            target_cat.setdefault("CraftItems", []).append(pasted)
            # Refresh list if we pasted into the currently visible category
            if self.cat_combo.currentIndex() == target_idx:
                self._refresh_recipe_list()
            self.changed.emit()

    def _duplicate_recipe(self):
        row = self.recipe_list.currentRow()
        cat = self._get_current_category()
        if not cat or row < 0:
            return
        items = cat.get("CraftItems", [])
        if row < len(items):
            dup = copy.deepcopy(items[row])
            dup["RecipeName"] = dup.get("RecipeName", "") + " (Copy)"
            items.insert(row + 1, dup)
            self._refresh_recipe_list()
            self.recipe_list.setCurrentRow(row + 1)
            self.changed.emit()

    def _delete_recipe(self):
        row = self.recipe_list.currentRow()
        cat = self._get_current_category()
        if not cat or row < 0:
            return
        items = cat.get("CraftItems", [])
        if row < len(items):
            reply = QMessageBox.question(
                self, TR("dlg_del_rec"),
                TR("dlg_del_rec_msg").format(items[row].get("Result", "?")),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                items.pop(row)
                self._refresh_recipe_list()
                self.detail_editor.clear()
                self.changed.emit()

    def _move_up(self):
        row = self.recipe_list.currentRow()
        cat = self._get_current_category()
        if not cat or row <= 0:
            return
        items = cat.get("CraftItems", [])
        items[row - 1], items[row] = items[row], items[row - 1]
        self._refresh_recipe_list()
        self.recipe_list.setCurrentRow(row - 1)
        self.changed.emit()

    def _move_down(self):
        row = self.recipe_list.currentRow()
        cat = self._get_current_category()
        if not cat:
            return
        items = cat.get("CraftItems", [])
        if row < len(items) - 1:
            items[row], items[row + 1] = items[row + 1], items[row]
            self._refresh_recipe_list()
            self.recipe_list.setCurrentRow(row + 1)
            self.changed.emit()

    def _on_recipe_edited(self):
        row = self.recipe_list.currentRow()
        cat = self._get_current_category()
        if cat and 0 <= row < len(cat.get("CraftItems", [])):
            self.recipe_list.blockSignals(True)
            if self.recipe_list.item(row):
                self.recipe_list.item(row).setText(
                    self._recipe_display(cat["CraftItems"][row])
                )
            self.recipe_list.blockSignals(False)
        self.changed.emit()

    def load_categories(self, categories: list):
        self._categories = categories
        self.cat_combo.blockSignals(True)
        self.cat_combo.clear()
        for cat in categories:
            self.cat_combo.addItem(cat.get("CategoryName", "(unnamed)"))
        self.cat_combo.blockSignals(False)
        self.detail_editor.clear()
        if categories:
            self.cat_combo.setCurrentIndex(0)
            self._on_category_changed(0)

    def refresh_category_names(self, categories: list):
        current = self.cat_combo.currentIndex()
        self.cat_combo.blockSignals(True)
        self.cat_combo.clear()
        for cat in categories:
            self.cat_combo.addItem(cat.get("CategoryName", "(unnamed)"))
        self.cat_combo.blockSignals(False)
        self.cat_combo.setCurrentIndex(current if current < len(categories) else 0)

    def select_category(self, index: int):
        if 0 <= index < self.cat_combo.count():
            self.cat_combo.setCurrentIndex(index)


# =============================================================================
# TAB: JSON EXPLORER
# =============================================================================
class JsonExplorerTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        lbl = QLabel(TR("explorer_title"))
        lbl.setStyleSheet("font-weight: bold;")
        layout.addWidget(lbl)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels([TR("explorer_col0"), TR("explorer_col1")])
        self.tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tree.setAlternatingRowColors(True)
        layout.addWidget(self.tree)

    def load_data(self, data: dict):
        self.tree.clear()
        self._populate(self.tree.invisibleRootItem(), data)
        self.tree.expandToDepth(2)

    def _populate(self, parent, data, depth=0):
        if depth > 8:
            return
        if isinstance(data, dict):
            for key, value in data.items():
                item = QTreeWidgetItem([str(key), self._label(value)])
                item.setForeground(0, QColor("#7ec8e3"))
                parent.addChild(item)
                self._populate(item, value, depth + 1)
        elif isinstance(data, list):
            for i, value in enumerate(data):
                name = self._list_name(value, i)
                item = QTreeWidgetItem([name, self._label(value)])
                item.setForeground(0, QColor("#b5ead7"))
                parent.addChild(item)
                self._populate(item, value, depth + 1)
        else:
            s = str(data)
            parent.setText(1, s[:77] + "..." if len(s) > 80 else s)

    @staticmethod
    def _label(value) -> str:
        if isinstance(value, dict):
            return f"{{…}} ({len(value)} Keys)"
        if isinstance(value, list):
            return f"[…] ({len(value)} Items)"
        s = str(value)
        return f'"{s[:57]}..."' if len(s) > 60 else f'"{s}"'

    @staticmethod
    def _list_name(value, index: int) -> str:
        if isinstance(value, dict):
            for key in ("CategoryName", "Result", "RecipeName", "Classname"):
                if key in value:
                    return f"[{index}] {value[key]}"
        return f"[{index}]"


# =============================================================================
# MAIN WINDOW
# =============================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(TR("window_title"))
        self.setMinimumSize(1100, 750)
        self.resize(1280, 850)
        self._data = default_data()
        self._file_path = None
        self._unsaved = False
        self._setup_ui()
        self._setup_menu()
        self._apply_dark_theme()

    # ------------------------------------------------------------------
    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(4, 4, 4, 4)

        file_bar = QHBoxLayout()
        self.lbl_file = QLabel(TR("no_file"))
        self.lbl_file.setStyleSheet("color: #a6adc8; font-style: italic;")
        btn_new     = QPushButton(TR("btn_new"));     btn_new.setFixedHeight(32)
        btn_open    = QPushButton(TR("btn_open"));    btn_open.setFixedHeight(32)
        btn_save    = QPushButton(TR("btn_save"));    btn_save.setFixedHeight(32)
        btn_save_as = QPushButton(TR("btn_save_as")); btn_save_as.setFixedHeight(32)
        for b in [btn_new, btn_open, btn_save, btn_save_as]:
            file_bar.addWidget(b)
        file_bar.addSpacing(12)
        file_bar.addWidget(self.lbl_file)
        file_bar.addStretch()
        main_layout.addLayout(file_bar)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tab_custom     = CustomizationTab()
        self.tab_categories = CategoriesTab()
        self.tab_recipes    = RecipesTab()
        self.tab_explorer   = JsonExplorerTab()
        self.tabs.addTab(self.tab_custom,     TR("tab_custom"))
        self.tabs.addTab(self.tab_categories, TR("tab_categories"))
        self.tabs.addTab(self.tab_recipes,    TR("tab_recipes"))
        self.tabs.addTab(self.tab_explorer,   TR("tab_explorer"))
        main_layout.addWidget(self.tabs, 1)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self._set_status(TR("status_ready"))

        btn_new.clicked.connect(self._new_file)
        btn_open.clicked.connect(self._open_file)
        btn_save.clicked.connect(self._save_file)
        btn_save_as.clicked.connect(self._save_file_as)
        self.tab_custom.changed.connect(self._mark_unsaved)
        self.tab_categories.changed.connect(self._on_categories_changed)
        self.tab_recipes.changed.connect(self._mark_unsaved)
        self.tab_categories.category_double_clicked.connect(self._on_category_double_clicked)
        self.tabs.currentChanged.connect(self._on_tab_changed)

    def _setup_menu(self):
        mb = self.menuBar()

        file_menu = mb.addMenu(TR("menu_file"))
        file_menu.addAction(TR("menu_new"),      self._new_file,     "Ctrl+N")
        file_menu.addAction(TR("menu_open"),     self._open_file,    "Ctrl+O")
        file_menu.addSeparator()
        file_menu.addAction(TR("menu_save"),     self._save_file,    "Ctrl+S")
        file_menu.addAction(TR("menu_save_as"),  self._save_file_as, "Ctrl+Shift+S")
        file_menu.addSeparator()
        file_menu.addAction(TR("menu_exit"),     self.close,         "Ctrl+Q")

        tools_menu = mb.addMenu(TR("menu_tools"))
        tools_menu.addAction(TR("menu_validate"), self._validate_all)
        tools_menu.addAction(TR("menu_scan"),     self._scan_classnames)
        tools_menu.addAction(TR("menu_library"),  self._show_library)

        settings_menu = mb.addMenu(TR("menu_settings"))
        lang_menu = settings_menu.addMenu(TR("menu_language"))
        lang_menu.addAction("English",  lambda: self._set_language("en"))
        lang_menu.addAction("Deutsch",  lambda: self._set_language("de"))
        settings_menu.addSeparator()
        settings_menu.addAction(TR("menu_about"), self._show_about)

    # ------------------------------------------------------------------
    def _apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-size: 13px;
            }
            QTabWidget::pane {
                border: 1px solid #45475a;
                background-color: #181825;
            }
            QTabBar::tab {
                background: #313244;
                color: #cdd6f4;
                padding: 6px 16px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 100px;
            }
            QTabBar::tab:selected {
                background: #89b4fa;
                color: #1e1e2e;
                font-weight: bold;
            }
            QTabBar::tab:hover:!selected { background: #45475a; }
            QListWidget {
                background-color: #181825;
                border: 1px solid #45475a;
                border-radius: 4px;
                selection-background-color: #89b4fa;
                selection-color: #1e1e2e;
            }
            QListWidget::item:hover { background-color: #313244; }
            QListWidget::item:alternate { background-color: #1e1e2e; }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
                background-color: #313244;
                border: 1px solid #45475a;
                border-radius: 4px;
                padding: 3px 6px;
                color: #cdd6f4;
                selection-background-color: #89b4fa;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border-color: #89b4fa;
            }
            QComboBox::drop-down {
                border: none;
                background: #585b70;
                width: 22px;
                border-radius: 0 4px 4px 0;
                subcontrol-origin: padding;
                subcontrol-position: top right;
            }
            QComboBox::down-arrow {
                width: 0; height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #cdd6f4;
            }
            QComboBox QAbstractItemView {
                background-color: #313244;
                border: 1px solid #45475a;
                selection-background-color: #89b4fa;
                selection-color: #1e1e2e;
                padding: 2px;
            }
            QCheckBox { spacing: 8px; }
            QCheckBox::indicator {
                width: 18px; height: 18px;
                border: 2px solid #585b70;
                border-radius: 4px;
                background: #313244;
            }
            QCheckBox::indicator:hover { border-color: #89b4fa; }
            QCheckBox::indicator:checked {
                background-color: #a6e3a1;
                border-color: #a6e3a1;
            }
            QPushButton {
                background-color: #313244;
                border: 1px solid #45475a;
                border-radius: 4px;
                padding: 4px 12px;
                color: #cdd6f4;
            }
            QPushButton:hover {
                background-color: #45475a;
                border-color: #89b4fa;
            }
            QPushButton:pressed {
                background-color: #89b4fa;
                color: #1e1e2e;
            }
            QPushButton:disabled {
                background-color: #1e1e2e;
                color: #45475a;
                border-color: #313244;
            }
            QGroupBox {
                border: 1px solid #45475a;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 6px;
                color: #89b4fa;
            }
            QScrollBar:vertical {
                background: #1e1e2e;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background: #45475a;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
            QTreeWidget {
                background-color: #181825;
                border: 1px solid #45475a;
                alternate-background-color: #1e1e2e;
                selection-background-color: #89b4fa;
                selection-color: #1e1e2e;
            }
            QHeaderView::section {
                background-color: #313244;
                border: none;
                border-right: 1px solid #45475a;
                padding: 4px 8px;
                color: #89b4fa;
            }
            QStatusBar {
                background: #181825;
                color: #a6adc8;
                border-top: 1px solid #45475a;
            }
            QMenuBar {
                background: #181825;
                border-bottom: 1px solid #45475a;
            }
            QMenuBar::item:selected { background: #313244; }
            QMenu {
                background: #1e1e2e;
                border: 1px solid #45475a;
            }
            QMenu::item:selected { background: #89b4fa; color: #1e1e2e; }
            QSplitter::handle { background: #45475a; width: 2px; }
            QToolButton {
                background: #313244;
                border: 1px solid #45475a;
                border-radius: 3px;
                padding: 2px;
            }
            QToolButton:hover { background: #45475a; }
        """)

    # ------------------------------------------------------------------
    def _set_status(self, msg: str):
        self.status_bar.showMessage(msg)

    def _mark_unsaved(self):
        self._unsaved = True
        base = TR("window_title")
        suffix = f"  —  {os.path.basename(self._file_path)} *" if self._file_path else "  —  * "
        self.setWindowTitle(base + suffix)

    def _mark_saved(self):
        self._unsaved = False
        base = TR("window_title")
        suffix = f"  —  {os.path.basename(self._file_path)}" if self._file_path else ""
        self.setWindowTitle(base + suffix)

    def _on_categories_changed(self):
        self.tab_recipes.refresh_category_names(self.tab_categories.get_categories())
        self._mark_unsaved()

    def _on_category_double_clicked(self, idx: int):
        self.tab_recipes.select_category(idx)
        self.tabs.setCurrentWidget(self.tab_recipes)

    def _on_tab_changed(self, idx: int):
        if self.tabs.widget(idx) is self.tab_explorer:
            self._sync_data_from_tabs()
            self.tab_explorer.load_data(self._data)

    def _sync_data_from_tabs(self):
        self._data.setdefault("m_CraftClasses", {})["m_CustomizationSetting"] = (
            self.tab_custom.get_data()
        )

    def _load_data_into_tabs(self):
        cc = self._data.get("m_CraftClasses", {})
        self.tab_custom.load_data(cc.get("m_CustomizationSetting", {}))
        cats = cc.get("CraftCategories", [])
        self.tab_categories.load_categories(cats)
        self.tab_recipes.load_categories(cats)
        self.tab_explorer.load_data(self._data)

    # ------------------------------------------------------------------
    # FILE OPERATIONS
    # ------------------------------------------------------------------
    def _new_file(self):
        if self._unsaved:
            if QMessageBox.question(
                self, TR("dlg_unsaved"), TR("dlg_unsaved_new"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            ) != QMessageBox.StandardButton.Yes:
                return
        self._data = default_data()
        self._file_path = None
        self._load_data_into_tabs()
        self.lbl_file.setText(TR("st_new_file_lbl"))
        self._mark_unsaved()
        self._set_status(TR("st_new_file"))

    def _open_file(self):
        if self._unsaved:
            if QMessageBox.question(
                self, TR("dlg_unsaved"), TR("dlg_unsaved_open"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            ) != QMessageBox.StandardButton.Yes:
                return
        path, _ = QFileDialog.getOpenFileName(
            self, TR("menu_open"), "",
            "JSON files (*.json);;All files (*)"
        )
        if not path:
            return
        try:
            self._set_status(TR("st_loading").format(os.path.basename(path)))
            QApplication.processEvents()
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "m_CraftClasses" not in data:
                QMessageBox.warning(self, TR("dlg_invalid_title"), TR("dlg_invalid_file"))
                return
            self._data = data
            self._file_path = path
            new_count = scan_classnames_from_data(data)
            self._load_data_into_tabs()
            self.lbl_file.setText(path)
            self._mark_saved()
            cats = len(data["m_CraftClasses"].get("CraftCategories", []))
            recipes = sum(
                len(c.get("CraftItems", []))
                for c in data["m_CraftClasses"].get("CraftCategories", [])
            )
            msg = TR("st_loaded").format(cats, recipes)
            if new_count > 0:
                msg += TR("st_new_cls").format(new_count)
            self._set_status(msg)
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "JSON Error", TR("dlg_json_error") + str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", TR("dlg_load_error") + str(e))

    def _save_file(self):
        if not self._file_path:
            self._save_file_as()
        else:
            self._write_file(self._file_path)

    def _save_file_as(self):
        default = self._file_path or "HP_Crafter.json"
        path, _ = QFileDialog.getSaveFileName(
            self, TR("menu_save_as"), default,
            "JSON files (*.json);;All files (*)"
        )
        if path:
            self._write_file(path)

    def _write_file(self, path: str):
        self._sync_data_from_tabs()

        # Validate
        errors = []
        for cat in self._data.get("m_CraftClasses", {}).get("CraftCategories", []):
            cat_name = cat.get("CategoryName", "?")
            for i, recipe in enumerate(cat.get("CraftItems", [])):
                for e in validate_recipe(recipe):
                    errors.append(f"[{cat_name}] #{i + 1} ({recipe.get('Result', '?')}): {e}")

        if errors:
            err_text = "\n".join(errors[:20])
            if len(errors) > 20:
                err_text += f"\n... +{len(errors) - 20} more"
            if QMessageBox.warning(
                self, TR("dlg_valid_title"),
                f"{len(errors)}{TR('dlg_valid_found')}\n\n{err_text}\n\n{TR('dlg_valid_save')}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            ) != QMessageBox.StandardButton.Yes:
                return

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
            self._file_path = path
            self.lbl_file.setText(path)
            self._mark_saved()

            # Auto-scan classnames from the just-saved data and persist library
            scan_classnames_from_data(self._data)

            lib_updated = save_library_to_file()
            msg = TR("st_saved").format(os.path.basename(path))
            if lib_updated:
                msg += TR("st_lib_updated")
            self._set_status(msg)
        except Exception as e:
            QMessageBox.critical(self, "Error", TR("dlg_save_error") + str(e))

    # ------------------------------------------------------------------
    # TOOLS
    # ------------------------------------------------------------------
    def _validate_all(self):
        self._sync_data_from_tabs()
        errors = []
        cc = self._data.get("m_CraftClasses", {})
        if not cc.get("WorkbenchesClassnames"):
            errors.append("WorkbenchesClassnames is empty!")
        for cat in cc.get("CraftCategories", []):
            cat_name = cat.get("CategoryName", "?")
            for i, recipe in enumerate(cat.get("CraftItems", [])):
                for e in validate_recipe(recipe):
                    errors.append(f"[{cat_name}] #{i + 1} ({recipe.get('Result', '?')}): {e}")
        if errors:
            dlg = QDialog(self)
            dlg.setWindowTitle(TR("dlg_valid_title"))
            dlg.resize(600, 400)
            vl = QVBoxLayout(dlg)
            lbl = QLabel(f"{len(errors)}{TR('dlg_valid_found')}")
            lbl.setStyleSheet("color: #f38ba8; font-weight: bold;")
            vl.addWidget(lbl)
            txt = QTextEdit(); txt.setReadOnly(True)
            txt.setText("\n".join(errors))
            vl.addWidget(txt)
            bb = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
            bb.accepted.connect(dlg.accept)
            vl.addWidget(bb)
            dlg.exec()
        else:
            QMessageBox.information(self, TR("dlg_valid_title"), TR("dlg_valid_ok"))

    def _scan_classnames(self):
        self._sync_data_from_tabs()
        new_count = scan_classnames_from_data(self._data)
        if new_count > 0:
            QMessageBox.information(
                self, TR("dlg_scan_title"), TR("dlg_scan_new").format(new_count)
            )
        else:
            QMessageBox.information(self, TR("dlg_scan_title"), TR("dlg_scan_none"))

    def _show_library(self):
        dlg = QDialog(self)
        dlg.setWindowTitle(TR("lib_title"))
        dlg.resize(520, 520)
        vl = QVBoxLayout(dlg)

        tab_widget = QTabWidget()
        for category, names in CLASSNAME_LIBRARY.items():
            tab = QWidget()
            tl = QVBoxLayout(tab)

            lst = QListWidget()
            lst.addItems(sorted(names))
            tl.addWidget(lst)

            btn_row = QHBoxLayout()
            btn_rename = QPushButton(TR("lib_rename"))
            btn_delete = QPushButton(TR("lib_delete"))
            btn_row.addWidget(btn_rename)
            btn_row.addWidget(btn_delete)
            btn_row.addStretch()
            tl.addLayout(btn_row)

            def _rename(cat=category, lst_ref=lst):
                item = lst_ref.currentItem()
                if not item:
                    return
                old = item.text()
                new, ok = QInputDialog.getText(
                    dlg, TR("lib_rename_title"), TR("lib_rename_lbl"), text=old
                )
                if ok and new.strip() and new.strip() != old:
                    lib_list = CLASSNAME_LIBRARY.get(cat, [])
                    if old in lib_list:
                        lib_list[lib_list.index(old)] = new.strip()
                    item.setText(new.strip())

            def _delete(cat=category, lst_ref=lst):
                item = lst_ref.currentItem()
                if not item:
                    return
                name = item.text()
                reply = QMessageBox.question(
                    dlg, TR("lib_del_title"), TR("lib_del_msg").format(name),
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    lib_list = CLASSNAME_LIBRARY.get(cat, [])
                    if name in lib_list:
                        lib_list.remove(name)
                    lst_ref.takeItem(lst_ref.row(item))

            btn_rename.clicked.connect(_rename)
            btn_delete.clicked.connect(_delete)

            tab_widget.addTab(tab, category.capitalize())

        vl.addWidget(tab_widget)

        total = sum(len(v) for v in CLASSNAME_LIBRARY.values())
        lbl = QLabel(TR("lib_total").format(total))
        lbl.setStyleSheet("color: #a6adc8;")
        vl.addWidget(lbl)

        bb = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        bb.accepted.connect(dlg.accept)
        vl.addWidget(bb)
        dlg.exec()

    def _show_about(self):
        QMessageBox.information(self, TR("about_title"), TR("about_text"))

    def _set_language(self, lang: str):
        _settings["language"] = lang
        _save_settings()
        QMessageBox.information(self, TR("lang_title"), TR("lang_msg"))

    # ------------------------------------------------------------------
    def closeEvent(self, event):
        if self._unsaved:
            if QMessageBox.question(
                self, TR("dlg_unsaved"), TR("dlg_unsaved_exit"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            ) != QMessageBox.StandardButton.Yes:
                event.ignore()
                return
        event.accept()


# =============================================================================
# ENTRY POINT
# =============================================================================
def main():
    # Load persisted library before building the UI
    load_library_from_file()

    app = QApplication(sys.argv)
    app.setApplicationName("Exodus DayZ Forge")
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window,          QColor(30, 30, 46))
    palette.setColor(QPalette.ColorRole.WindowText,      QColor(205, 214, 244))
    palette.setColor(QPalette.ColorRole.Base,            QColor(24, 24, 37))
    palette.setColor(QPalette.ColorRole.AlternateBase,   QColor(30, 30, 46))
    palette.setColor(QPalette.ColorRole.ToolTipBase,     QColor(49, 50, 68))
    palette.setColor(QPalette.ColorRole.ToolTipText,     QColor(205, 214, 244))
    palette.setColor(QPalette.ColorRole.Text,            QColor(205, 214, 244))
    palette.setColor(QPalette.ColorRole.Button,          QColor(49, 50, 68))
    palette.setColor(QPalette.ColorRole.ButtonText,      QColor(205, 214, 244))
    palette.setColor(QPalette.ColorRole.BrightText,      QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Link,            QColor(137, 180, 250))
    palette.setColor(QPalette.ColorRole.Highlight,       QColor(137, 180, 250))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(30, 30, 46))
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
