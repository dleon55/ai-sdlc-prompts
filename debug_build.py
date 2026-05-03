import sys
import subprocess
with open("build.log", "w") as f:
    try:
        result = subprocess.run([sys.executable, "build.py"], capture_output=True, text=True)
        f.write("STDOUT:\n")
        f.write(result.stdout)
        f.write("\nSTDERR:\n")
        f.write(result.stderr)
    except Exception as e:
        f.write(f"ERROR: {str(e)}")
print("Log written to build.log")
