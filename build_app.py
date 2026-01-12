#!/usr/bin/env python3
"""
Build script for creating Mac M1 .app bundle
"""

import os
import sys
import subprocess
from pathlib import Path


def build_app():
    """Build the .app bundle using PyInstaller"""
    print("=" * 60)
    print("Building MD to PDF Converter for Mac M1")
    print("=" * 60)
    
    # Ensure we're in the right directory
    project_dir = Path(__file__).parent.absolute()
    os.chdir(project_dir)
    
    # Clean previous builds
    print("\n[1/3] Cleaning previous builds...")
    for dir_name in ['build', 'dist']:
        dir_path = project_dir / dir_name
        if dir_path.exists():
            subprocess.run(['rm', '-rf', str(dir_path)], check=True)
            print(f"  ✓ Removed {dir_name}/")
    
    # Run PyInstaller
    print("\n[2/3] Running PyInstaller...")
    result = subprocess.run(
        ['pyinstaller', '--clean', 'mdtopdf.spec'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("  ✗ Build failed!")
        print(result.stderr)
        return False
    
    print("  ✓ Build completed successfully")
    
    # Verify the .app was created
    print("\n[3/3] Verifying build...")
    app_path = project_dir / 'dist' / 'MD to PDF.app'
    
    if not app_path.exists():
        print("  ✗ .app bundle not found!")
        return False
    
    print(f"  ✓ App bundle created: {app_path}")
    
    # Get app size
    result = subprocess.run(
        ['du', '-sh', str(app_path)],
        capture_output=True,
        text=True,
        check=True
    )
    size = result.stdout.split()[0]
    print(f"  ✓ App size: {size}")
    
    print("\n" + "=" * 60)
    print("✓ BUILD SUCCESSFUL!")
    print("=" * 60)
    print(f"\nYour app is ready at:\n  {app_path}")
    print("\nTo run the app:")
    print(f"  open '{app_path}'")
    print("\nTo install the app:")
    print(f"  cp -r '{app_path}' /Applications/")
    print()
    
    return True


if __name__ == '__main__':
    success = build_app()
    sys.exit(0 if success else 1)
