import requests

def import_gists_to_database(db, username, commit=True):
    url = f"https://api.github.com/users/{username}/gists"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code}")

    gists = response.json()

    for gist in gists:
        db.execute(
            """
            INSERT INTO gists (
                id,
                github_id,
                description,
                created_at,
                updated_at,
                public
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                gist["id"],
                username,
                gist.get("description"),
                gist.get("created_at"),
                gist.get("updated_at"),
                int(gist.get("public", False))  # convert boolean to integer
            )
        )

    if commit:
        db.commit()
