from src.person.person_schema import IdentifierEnum


def get_identifier_type(identifier: str):
    """Get the identifier type.
    
    Args:
        identifier (str): The identifier
        
    Returns:
        str: The identifier type
    """
    if "@" in identifier:
        return IdentifierEnum.EMAIL
    return IdentifierEnum.PHONE_NUMBER