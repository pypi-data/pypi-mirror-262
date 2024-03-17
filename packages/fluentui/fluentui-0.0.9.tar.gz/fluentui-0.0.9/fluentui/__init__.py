from pathlib import Path

FluentuiAssetPath = (Path(__file__).parent / 'assets').as_posix()
FluentuiLightStyle = Path(f'{FluentuiAssetPath}/light-style.qss').read_text(encoding='utf8')
