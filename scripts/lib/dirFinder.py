def findMatchingOutDir(scriptsSubPath):
    from pathlib import Path

    taskDir = Path(scriptsSubPath).parent
    outDir = Path(*["out" if part == "scripts" else part for part in taskDir.parts])
    return outDir
