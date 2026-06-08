import subprocess
from pathlib import Path


ROOT = Path(__file__).parent.parent


def test_generated_javascript_variable_runtime():
    result = subprocess.run(
        ["node", str(ROOT / "tests" / "js" / "test_variables_runtime.js")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "runtime variable tests: ok" in result.stdout
