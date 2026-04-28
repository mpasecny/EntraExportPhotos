import os, csv, sys, requests
from pathlib import Path
from azure.identity import InteractiveBrowserCredential
class EntraPhotoExporter:
    def __init__(self, csv_file, output_dir="PHOTOS"):
        self.csv_file = csv_file
        self.output_dir = output_dir
        self.access_token = None
        self.downloaded_count = 0
        self.skipped_count = 0
        self._setup_output_directory()
        self._authenticate()
    def _setup_output_directory(self):
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        print(f" Výstupní adresář: {self.output_dir}")
    def _photo_exists(self, employee_id):
        return (Path(self.output_dir) / f"{employee_id}.jpg").exists()
    def _authenticate(self):
        print("Ověřování vůči Entra ID...")
        try:
            credential = InteractiveBrowserCredential()
            self.access_token = credential.get_token("https://graph.microsoft.com/.default").token
            print(" Úspěšné ověření")
        except Exception as e:
            print(f" Chyba: {str(e)}")
            sys.exit(1)
    def _get_user_by_employee_id(self, employee_id):
        try:
            headers = {"Authorization": f"Bearer {self.access_token}", "ConsistencyLevel": "eventual"}
            url = f"https://graph.microsoft.com/v1.0/users?$filter=employeeId eq '{employee_id}'"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                users = response.json().get("value", [])
                return users[0] if users else None
            return None
        except Exception as e:
            print(f" Chyba: {str(e)}")
            return None
    def _download_photo(self, user_id, employee_id):
        if self._photo_exists(employee_id):
            print(f" Fotografia {employee_id} již existuje")
            self.skipped_count += 1
            return True
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(f"https://graph.microsoft.com/v1.0/users/{user_id}/photo/$value", headers=headers)
            if response.status_code == 200:
                Path(self.output_dir, f"{employee_id}.jpg").write_bytes(response.content)
                print(f" Fotografia {employee_id} uložena")
                self.downloaded_count += 1
                return True
            return False
        except Exception as e:
            print(f" Chyba: {str(e)}")
            return False
    def export_photos(self):
        if not os.path.exists(self.csv_file):
            return False
        with open(self.csv_file, "r", encoding="utf-8") as f:
            reader, total, not_found = csv.reader(f), 0, 0
            next(reader, None)
            for row in reader:
                if not row: continue
                employee_id = row[0].strip()
                total += 1
                print(f"\nZpracování {total}: {employee_id}")
                user = self._get_user_by_employee_id(employee_id)
                if not user: not_found += 1
                else: self._download_photo(user["id"], employee_id)
        print(f"\n{'='*60}\nExport dokončen!\n{'='*60}")
        print(f"Celkem: {total}\nNově staženo: {self.downloaded_count}\nPřeskočeno: {self.skipped_count}\nNenalezeno: {not_found}\n{'='*60}")
        return True
if __name__ == "__main__":
    print("="*60 + "\nEntraExportPhotos\n" + "="*60)
    exporter = EntraPhotoExporter("employees.csv")
    exporter.export_photos()
