import polib
import pathlib

base_dir = pathlib.Path("../cron_descriptor/locale")

for po_file in base_dir.rglob("*.po"):
    mo_file = po_file.with_suffix(".mo")
    print(f"Compiling {po_file} → {mo_file}")
    po = polib.pofile(po_file)
    po.save_as_mofile(str(mo_file))