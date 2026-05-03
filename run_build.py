import traceback
try:
    import build
    build.build()
    with open("success.txt", "w") as f:
        f.write("OK")
except Exception as e:
    with open("error.txt", "w") as f:
        f.write(traceback.format_exc())
