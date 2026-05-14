"""Script para iniciar o servidor de desenvolvimento."""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "nexo.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_excludes=[
            "node_modules/*",
            "webapp/*",
            "desktop/*",
            "focalboard-legacy/*",
            ".*",
            "*.md",
            "_reversa_*/*",
            ".reversa/*",
        ],
    )
