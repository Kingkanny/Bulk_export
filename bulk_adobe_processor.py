import os
import shutil
import json
from pathlib import Path

# CONFIGURATION
ADOBE_CC_ROOT = Path("/Volumes/Evangelion/test")
OUTPUT_ROOT = Path("/Volumes/Evangelion/test")
SKIP_PROCESSED = True  # Skip folders that already have output

def process_single_library(source_folder):
    """Your existing processing logic for one library"""
    manifest_path = source_folder / "manifest"
    asset_map = {}
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading manifest: {str(e)}")
        return 0

    # Parse manifest (your existing code)
    for element in data['children']:
        if element['name'] == 'elements':
            for asset in element['children']:
                asset_id = asset['id']
                asset_name = asset['name']
                base_name = asset_name
                counter = 1
                while asset_name in asset_map.values():
                    asset_name = f"{base_name}_{counter}"
                    counter += 1
                asset_map[asset_id] = asset_name

    # Create output folder
    output_folder = OUTPUT_ROOT / f"{source_folder.name}"
    output_folder.mkdir(exist_ok=True)
    processed = 0

    # Process assets (your existing code)
    for asset_folder in source_folder.glob('*-*-*-*-*'):
        if not asset_folder.is_dir():
            continue
            
        asset_id = asset_folder.name
        if asset_id not in asset_map:
            continue
            
        for file in asset_folder.glob('*'):
            if file.is_file():
                ext = file.suffix.lower()
                new_name = f"{asset_map[asset_id]}{ext}"
                dest_path = output_folder / new_name
                
                counter = 1
                while dest_path.exists():
                    base, ext = os.path.splitext(new_name)
                    dest_path = output_folder / f"{base}_{counter}{ext}"
                    counter += 1
                
                shutil.copy2(file, dest_path)
                processed += 1
                break
    
    return processed

def main():
    print("=== Bulk Adobe CC Library Processor ===")
    print(f"Processing all libraries in: {ADOBE_CC_ROOT}")
    print(f"Output will be saved to: {OUTPUT_ROOT}\n")
    
    OUTPUT_ROOT.mkdir(exist_ok=True)
    total_processed = 0
    total_libraries = 0

    # Process each subfolder in Adobe CC directory
    for library_folder in ADOBE_CC_ROOT.iterdir():
        if not library_folder.is_dir():
            continue
            
        # Skip non-library folders
        if not (library_folder / "manifest").exists():
            print(f"⚠️ Skipping {library_folder.name} (no manifest)")
            continue
            
        # Skip already processed if enabled
        output_folder = OUTPUT_ROOT / f"{library_folder.name}"
        if SKIP_PROCESSED and output_folder.exists():
            print(f"⏩ Skipping {library_folder.name} (already processed)")
            continue
            
        print(f"\nProcessing {library_folder.name}...")
        count = process_single_library(library_folder)
        
        if count > 0:
            print(f"✅ Processed {count} assets")
            total_processed += count
            total_libraries += 1
        else:
            print("⚠️ No assets processed")

    print(f"\n=== Completed ===")
    print(f"Processed {total_processed} assets from {total_libraries} libraries")
    print(f"Output folders created in: {OUTPUT_ROOT}")
    print("\nEach library has its own folder with '_Renamed' suffix")

if __name__ == "__main__":
    main()
