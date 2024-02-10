import os
import requests
import zipfile
import json

print("\nLagata Mod Pack Installer")
print("Version 0.0.1")
print("\nCreated by Lagata, LLC, Inc (A subsidiary of Alphawin, LLC)\n")

url = "https://github.com/lagataLLCInc/mods/archive/refs/tags/release.zip"
appdata = os.getenv('APPDATA')  # Correct way to get %appdata% path
target = os.path.join(appdata, ".lagata")

def download_file(url, target):
    response = requests.get(url)
    with open(target, 'wb') as f:
        f.write(response.content)

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)

def create():
    print(f"Creating directory {target}")
    create_directory(target)
    print(f"Downloading {url}")
    zip_path = os.path.join(target, "release.zip")
    download_file(url, zip_path)
    print(f"Extracting release.zip to {target}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(target)
    print("Cleaning up release.zip")
    delete_file(zip_path)

def update_profile(profile_path, profile_name, last_version_id, game_dir):
    if os.path.exists(profile_path):
        with open(profile_path, 'r') as file:
            data = json.load(file)
        
        profiles = data.get("profiles", {})
        profiles[profile_name] = {
            "name": profile_name,
            "lastVersionId": last_version_id,
            "gameDir": game_dir
        }
        data["profiles"] = profiles
        
        with open(profile_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"{profile_path} updated with {profile_name} profile")

def install_fabric():
    if os.path.exists(os.path.join(target, "fabric-installer-1.0.0.jar")):
        print("Fabric already installed")
        return
    else:
        print("Installing Fabric")
        fabric_url = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/1.0.0/fabric-installer-1.0.0.jar"
        fabric_path = os.path.join(target, "fabric-installer-1.0.0.jar")
        download_file(fabric_url, fabric_path)
        os.system(f"java -jar {fabric_path} client -dir %appdata%\\.minecraft")

def main():
    create()
    print("Installation complete\n")
    print("Initializing Profiles Update")
    
    profiles_path = os.path.join(appdata, ".minecraft", "launcher_profiles.json")
    profiles_path_ms_store = os.path.join(appdata, ".minecraft", "launcher_profiles_microsoft_store.json")
    
    mod_pack_dir = os.path.join(appdata, ".lagata", "mods-release")
    install_fabric()

    update_profile(profiles_path, "lagata", "fabric-loader-0.15.6-1.20.4", mod_pack_dir)
    update_profile(profiles_path_ms_store, "lagata", "fabric-loader-0.15.6-1.20.4", mod_pack_dir)
    print("Profiles Updated")
    print("\n========================\nInstallation Complete\n\nEnjoy!\n========================\n")

main()
