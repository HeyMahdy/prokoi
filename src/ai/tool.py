@tool
async def get_or_create_skills(skill_names: list[str]) -> list[int]:
    """
    Get or create skills by their names and return their IDs.

    This function takes a list of skill names and returns their corresponding IDs
    from the database. If a skill doesn't exist, it will be created automatically.
    This is useful for bulk skill operations like adding multiple skills to a user,
    job, or learning resource.

    Args:
        skill_names (list[str]): List of skill names to fetch or create.
                                 Examples: ["Python", "JavaScript", "React"]

    Returns:
        list[int]: List of skill IDs corresponding to the input skill names.

        Example success:
        [1, 2, 3, 5, 8]  # IDs for the requested skills

        Example error:
        {
            "error": "Database error occurred",
            "details": "Connection timeout"
        }

    Raises:
        HTTPException: If there's an error during skill creation or retrieval.

    Example usage:
        skill_ids = await get_or_create_skills(["Python", "FastAPI", "MySQL"])
        # Returns: [12, 45, 67]
    """
    try:
        skill_ids = []
        for name in skill_names:
            # Try fetching existing skill
            skill = await skillsService.get_skill_by_name(name)
            if not skill:
                # Skill doesn't exist, create it
                skill_id = await skillsService.create_skill(name)
                skill_ids.append(skill_id)
            else:
                skill_ids.append(skill.id)
        
        return skill_ids
    
    except Exception as e:
        print(e)
        return []