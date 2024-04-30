from passlib.hash import bcrypt


def hashText(text: str) -> str:
    return bcrypt.hash(text)

def compareHashedText(text: str, hashed_text: str) -> bool:
    return bcrypt.verify(text, hashed_text)