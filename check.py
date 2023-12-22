import os
import requests

path = os.path.abspath(os.curdir)
odoo_versions = ['9.0', '10.0', '11.0', '12.0', '13.0', '14.0', '15.0', '16.0', '17.0']

def append_file(module_name, upgradable, index):
    with open("./README.md", "a") as readme:
        readme.write(f"{index} | [{module_name}]({module_name}/) | ")
        for odoo_version in odoo_versions:
            supported, link = check_upgrade(module_name, odoo_version)
            if supported == "true":
                readme.write(f"[True]({link}) | ")
            else:
                readme.write("False | ")
        readme.write("\n")

def list_dirs(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and not d.startswith('.git')]

def check_upgrade(module_name, odoo_version):
    response = requests.get(f"https://apps.odoo.com/apps/modules/{odoo_version}/{module_name}/")
    if response.status_code == 200:
        return "true", f"https://apps.odoo.com/apps/modules/{odoo_version}/{module_name}/"
    elif response.status_code == 404:
        return "false", "Not Found"

def delete_lines():
    with open("./README.md", "r") as input_file:
        with open("./README-temp.md", "w") as output_file:
            for line in input_file:
                if not line.strip("\n").startswith('['):
                    output_file.write(line)

print("Starting to check!")

delete_lines()
os.replace('./README-temp.md', './README.md')

# Header row
with open("./README.md", "a") as readme:
    readme.write("Index | Addon | ")
    for odoo_version in odoo_versions:
        readme.write(f"Upgradeable to {odoo_version} | ")
    readme.write("\n--- | --- | ")
    for _ in odoo_versions:
        readme.write("--- | ")
    readme.write("\n")

modules = list_dirs(path)
for i, module in enumerate(modules, start=1):
    print(f"Processing {module}...")
    append_file(module, check_upgrade(module, odoo_version), i)

print("Finished checking!")
