# EntraExportPhotos

Aplikace pro export fotografií zaměstnanců z Entra ID (Azure Active Directory) na základě jejich osobních čísel.

## Funkčnost

- Čte CSV soubor obsahující seznam osobních čísel zaměstnanců
- Pro každé osobní číslo načte fotografii z Entra ID
- Uloží fotografie do adresáře `PHOTOS`
- Pojmenuje soubory podle osobních čísel (formát: `personalNumber.jpg`)
- Interaktivní ověření uživatele přes prohlížeč

## Požadavky

- Python 3.8+
- Přístup k Microsoft Entra ID
- Azure AD/Entra ID účet s oprávněním číst profily uživatelů

## Instalace

1. Klonujte nebo otevřete projekt
2. Vytvořte virtuální prostředí:
   ```powershell
   python -m venv venv
   ```
3. Aktivujte virtuální prostředí:
   ```powershell
   venv\Scripts\Activate.ps1
   ```
4. Nainstalujte závislosti:
   ```powershell
   pip install -r requirements.txt
   ```

## Použití

1. **Připravte CSV soubor** s názvem `employees.csv`:
   ```
   PersonalNumber
   001
   002
   003
   ```
   - První řádek obsahuje hlavičku
   - Každý následující řádek obsahuje jedno osobní číslo

2. **Spusťte aplikaci**:
   ```powershell
   python src/main.py
   ```

3. **Ověřte se** - otevře se prohlížeč s přihlášením do Entra ID

4. **Fotografie budou uloženy** v adresáři `PHOTOS/` s názvy:
   - `001.jpg`
   - `002.jpg`
   - `003.jpg`

## Struktura projektu

```
EntraExportPhotos/
├── src/
│   └── main.py              # Hlavní aplikace
├── PHOTOS/                  # Výstupní adresář (vytvoří se automaticky)
├── employees.csv            # Soubor se vzorem
├── requirements.txt         # Python závislosti
├── README.md               # Tento soubor
└── .gitignore
```

## Výstup aplikace

Aplikace vypíše detailní zprávu o průběhu:
- ✓ Úspěšně uložené fotografie
- ⚠ Nenalezené uživatele
- ✗ Chyby při stažení

Na konci vypíše souhrn s počtem:
- Celkem zpracováno
- Úspěšně staženo
- Neúspěšných

## Poznámky

- Zajistěte, že CSV soubor je v UTF-8 kódování
- Osobní čísla by měla odpovídat hodnotě `employeeId` v Entra ID
- Pokud fotografie neexistuje, aplikace pokračuje na další osobu
- Aplikace přetáhne existující fotografie stejným názvem

## Řešení problémů

### Chyba: "Soubor 'employees.csv' nenalezen"
- Vytvořte soubor `employees.csv` v kořenovém adresáři projektu

### Chyba: Ověření se nepodařilo
- Zkontrolujte připojení k internetu
- Ujistěte se, že máte přístup k Entra ID

### Fotografie se nestahují
- Ověřte, že osobní čísla odpovídají hodnotě `employeeId` v Entra ID
- Zkontrolujte oprávnění účtu pro čtení profilů uživatelů

## License

[Doplnit dle potřeby]

