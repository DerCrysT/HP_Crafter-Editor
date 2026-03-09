# HP_Crafter-Editor
# Exodus DayZ Forge

Visual Recipe Editor for the DayZ Mod **HP_Crafter**

Developed by CrysT — Version 1.0

Modlink: https://steamcommunity.com/sharedfiles/filedetails/?id=3133007745&searchtext=crafter
---

## What is this?

Exodus DayZ Forge is a standalone desktop tool for creating and editing crafting recipes for the DayZ mod HP_Crafter.  
It replaces the need to manually edit large `HP_Crafter.json` files, which can grow to hundreds of thousands of lines.

The editor reads and writes the exact JSON structure required by the mod — files can be dropped directly onto your server.

---

## Download

**[Download latest release (.exe)](../../releases/latest)**

No installation required. Just download and run `ExodusCraftingEditor.exe`.

---

## Features

- **Categories** — Create, rename, delete and reorder craft categories (Drag & Drop + Up/Down buttons)
- **Recipes** — Full recipe editor with drag & drop reorder, duplicate, and copy/paste across categories
- **Customization** — Set all HUD icon and background image paths with file browser and preview
- **JSON Explorer** — Read-only tree view of the entire loaded JSON structure
- **Classname Library** — Built-in library of known DayZ classnames with autocomplete, rename and delete
- **Auto-Scan** — Automatically scans loaded and saved JSON files for new classnames and adds them to the library
- **Validation** — Validates all recipes before saving and warns about issues
- **English / Deutsch** — Language can be switched in the Settings menu (restart required)

---

## How to use

### 1. Start the tool

Double-click `ExodusCraftingEditor.exe`.

### 2. Open or create a file

- **New file** — Click `New` to start from scratch
- **Open existing** — Click `Open` and select your `HP_Crafter.json`

### 3. Edit categories

Go to the **Categories** tab.

- Use `+ New` to create a category
- Drag & Drop or the Up/Down buttons to reorder
- Double-click a category to jump directly to its recipes

### 4. Edit recipes

Go to the **Recipes** tab.

- Select a category from the dropdown at the top
- Click `+ New` to add a recipe
- Click a recipe in the list to open the detail editor on the right
- Use `Copy` + `Paste` to copy a recipe into a different category
- Use `Duplicate` to copy a recipe within the same category

### 5. Recipe fields

| Field | Description |
|---|---|
| Result | Classname of the output item |
| ResultCount | How many units are produced |
| RecipeName | Display name shown in the HUD |
| CraftType | Icon shown in the HUD (e.g. `toolspic`, `ammopic`) |
| ComponentsDontAffectHealth | If enabled, result health is fixed regardless of ingredient health |
| CraftComponents | List of required items — Classname, Amount, Destroy flag, HP change |
| AttachmentsNeed | Workbench attachments that must be mounted (e.g. `HP_Anvil`) |

### 6. CraftComponents — HP change

Items have **100 HP total**.  
The `Changehealth` field adjusts an item's health during crafting:

- `0` = no change
- `-5` = item loses 5 HP
- `+10` = item gains 10 HP

Components can be reordered via Drag & Drop.

### 7. Save

Click `Save` or `Ctrl+S`.  
The tool validates all recipes before writing the file and warns about any issues.  
New classnames found in the file are automatically added to the library on every save.

---

## Classname Library

The library stores known DayZ classnames and powers the autocomplete dropdowns throughout the editor.

- Classnames are loaded from `forge_library.json` at startup and merged with the built-in defaults
- Every time you save a JSON file, new classnames are scanned and added automatically
- You can manually rename or delete entries via **Tools -> Classname Library**

The library is stored in `forge_library.json` next to the `.exe` — it persists across sessions and grows automatically as you work.

---

## Files next to the .exe

| File | Purpose |
|---|---|
| `ExodusCraftingEditor.exe` | The application |
| `forge_settings.json` | Language preference |
| `forge_library.json` | Your classname library (auto-created on first save) |

---

## AttachmentsNeed — Known Slots

### HP_Crafter Mod Items

`HP_Anvil` `HP_Drill` `HP_Grinde` `HP_napilnik` `HP_Oiler` `HP_Vise` `HP_Payalnik` `HP_Tester` `HP_Pipe`

### Vanilla DayZ Items

`Crowbar` `FarmingHoe` `FirefighterAxe` `Hacksaw` `Hammer` `HandSaw` `Hatchet` `LugWrench` `Nails` `Pickaxe` `Pipewrench` `Pliers` `Screwdriver` `Shovel` `MetalPlate` `SledgeHammer` `WoodAxe` `Wrench`

---

## CraftType values

| Value | Description |
|---|---|
| `repairpic` | Repair |
| `paintpic` | Paint |
| `ammopic` | Ammo |
| `weaponpic` | Weapon |
| `toolspic` | Tools |
| `craftpic` | Craft (default) |
| `sewingkitpic` | Sewing |
| `buildingpic` | Building |
| `carpic` | Car |
| `furniturepic` | Furniture |
| `medicpic` | Medical |
| `bookpic` | Book |
| `housepic` | House |
| `donatepic` | Donate |
| `voltagepic` | Voltage |

Icon images can be customized per server in the **Customization** tab.

---

## JSON Structure

The tool reads and writes the exact structure required by HP_Crafter:

```json
{
  "m_CraftClasses": {
    "m_CustomizationSetting": { "PathToMainBackgroundImg": "", "...": "..." },
    "WorkbenchesClassnames": ["HP_Crafter"],
    "CraftCategories": [
      {
        "CategoryName": "Example",
        "CraftItems": [
          {
            "Result": "CopperWire",
            "ResultCount": 2,
            "ComponentsDontAffectHealth": 1,
            "CraftType": "toolspic",
            "RecipeName": "Copper Wire",
            "CraftComponents": [
              { "Classname": "Pliers", "Amount": 1, "Destroy": 0, "Changehealth": -5.0 }
            ],
            "AttachmentsNeed": ["HP_Vise"]
          }
        ]
      }
    ]
  }
}
```

---

## Running from source

If you want to run or modify the Python source directly:

```powershell
pip install PySide6
python hp_crafter_editor.py
```

**Build your own .exe:**

```powershell
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name "ExodusCraftingEditor" hp_crafter_editor.py
```

The finished `.exe` will be in the `dist` folder. The `build` folder and `.spec` file can be deleted afterwards.

---

## License

MIT License — free to use, modify and distribute.  
If you improve the tool, a credit or pull request is always appreciated.

---

## Credits

Exodus DayZ Forge — Developed by CrysT  
Built for the DayZ community. Not affiliated with Bohemia Interactive.

<img width="1920" height="1017" alt="ECTCustomization" src="https://github.com/user-attachments/assets/c9f1d6fc-b01b-4cf9-9909-5cab63b25ffc" />
<img width="1920" height="1019" alt="ECTCategories" src="https://github.com/user-attachments/assets/be46f98d-152d-40b8-93f6-4ca6210986ab" />
<img width="1920" height="1015" alt="ECTRecepies1" src="https://github.com/user-attachments/assets/a037e6be-a31a-40aa-af18-5b64e785bf0c" />
<img width="1920" height="1017" alt="ECTJsonExplorer" src="https://github.com/user-attachments/assets/a67777ab-f94d-402d-adcd-0d5917fa5e1a" />
<img width="1920" height="1019" alt="ECTClassnameLibary" src="https://github.com/user-attachments/assets/acddecb4-9f09-4bf9-bce0-77179250da5f" />
