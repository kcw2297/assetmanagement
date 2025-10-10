import re
from pathlib import Path

VERSION_FILE = Path(__file__).parent / "version.py"

def get_current_version():
    content = VERSION_FILE.read_text()
    match = re.search(r'__version__ = "(\d+)\.(\d+)\.(\d+)"', content)
    if not match:
        raise ValueError("버전 형식을 찾을 수 없습니다")
    return tuple(map(int, match.groups()))

def bump_version(level="patch"):
    major, minor, patch = get_current_version()
    
    if level == "major":
        major += 1
        minor = 0
        patch = 0
    elif level == "minor":
        minor += 1
        patch = 0
    elif level == "patch":
        patch += 1
    else:
        raise ValueError("level은 'major', 'minor', 'patch' 중 하나여야 합니다")
    
    new_version = f"{major}.{minor}.{patch}"
    
    content = VERSION_FILE.read_text()
    new_content = re.sub(
        r'__version__ = "\d+\.\d+\.\d+"',
        f'__version__ = "{new_version}"',
        content
    )
    VERSION_FILE.write_text(new_content)
    
    print(f"버전 업데이트: {major-1 if level=='major' else major}.{minor-1 if level=='minor' else minor}.{patch-1 if level=='patch' else patch} → {new_version}")
    return new_version

if __name__ == "__main__":
    import sys
    level = sys.argv[1] if len(sys.argv) > 1 else "patch"
    bump_version(level)
