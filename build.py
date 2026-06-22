"""Build script for creating executable."""

import PyInstaller.__main__
import os
import shutil

def build():
    """Build the executable."""
    print("Building telegram_bot_agent.exe...")

    # Clean previous build
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')

    # Run PyInstaller
    PyInstaller.__main__.run([
        'telegram_bot_agent.spec',
        '--clean',
        '--noconfirm',
    ])

    print("\n✅ Build complete!")
    print("Executable: dist/telegram_bot_agent.exe")

if __name__ == '__main__':
    build()