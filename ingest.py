
from pypdf import PdfReader
from pathlib import Path
from git import Repo


def load_resume(path):
    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text


def load_readmes(folder):

    docs = []

    for file in Path(folder).rglob("README.md"):

        try:
            docs.append({
                "repo": file.parent.name,
                "source": str(file),
                "text": file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )
            })

        except Exception as e:
            print(e)

    return docs


def load_python_files(folder):

    docs = []

    ignore = {
        ".git",
        "__pycache__",
        "venv",
        ".venv"
    }

    for file in Path(folder).rglob("*.py"):

        if any(part in ignore for part in file.parts):
            continue

        try:
            docs.append({
                "repo": file.parts[-2],
                "source": str(file),
                "text": file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )
            })

        except:
            pass

    return docs


def load_commits(repo_path):

    repo = Repo(repo_path)

    docs = []

    for commit in repo.iter_commits():

        docs.append({
            "repo": Path(repo_path).name,
            "author": str(commit.author),
            "date": str(commit.committed_datetime),
            "message": commit.message.strip()
        })

    return docs


def chunk_text(
    text,
    chunk_size=800,
    overlap=150
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(
            text[start:end]
        )

        start += (
            chunk_size - overlap
        )

    return chunks


if __name__ == "__main__":


    resume = load_resume(
        "data/Riyashah1.pdf"
    )

    print("=" * 50)
    print("RESUME LOADED")
    print("=" * 50)

    print(resume[:500])

    print("\n")


    readmes = load_readmes(
        "data/github"
    )

    print("=" * 50)
    print(
        f"README FILES FOUND : {len(readmes)}"
    )
    print("=" * 50)

    for doc in readmes:
        print(doc["repo"])

    print("\n")


    python_files = load_python_files(
        "data/github"
    )

    print("=" * 50)
    print(
        f"PYTHON FILES FOUND : {len(python_files)}"
    )
    print("=" * 50)

    for doc in python_files[:5]:
        print(doc["source"])

    print("\n")

   

    print("=" * 50)
    print("COMMIT HISTORY")
    print("=" * 50)

    for repo in Path(
        "data/github"
    ).iterdir():

        if repo.is_dir():

            commits = load_commits(
                str(repo)
            )

            print(
                f"{repo.name} : {len(commits)} commits"
            )

    print("\n")



    print("=" * 50)
    print("BUILDING CORPUS")
    print("=" * 50)

    all_chunks = []

    # Resume

    for chunk in chunk_text(
        resume
    ):

        all_chunks.append({
            "repo": "resume",
            "type": "resume",
            "text": chunk
        })

    # README files

    for doc in readmes:

        for chunk in chunk_text(
            doc["text"]
        ):

            all_chunks.append({
                "repo": doc["repo"],
                "type": "readme",
                "text": chunk
            })


    for doc in python_files:

        for chunk in chunk_text(
            doc["text"]
        ):

            all_chunks.append({
                "repo": doc["repo"],
                "type": "code",
                "text": chunk
            })


    for repo in Path(
        "data/github"
    ).iterdir():

        if repo.is_dir():

            commits = load_commits(
                str(repo)
            )

            for commit in commits:

                all_chunks.append({
                    "repo": commit["repo"],
                    "type": "commit",
                    "text":
                    f"""
Author:
{commit['author']}

Date:
{commit['date']}

Message:
{commit['message']}
"""
                })

    print(
        f"\nTOTAL CHUNKS : {len(all_chunks)}"
    )

    print("\nFIRST CHUNK:\n")

    print(
        all_chunks[0]["text"][:500]
    )
