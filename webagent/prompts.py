SYSTEM_PROMPT = """You are a helpful assistant that creates realistic biographies and resumes for fictional characters based on a brief prompt. 
Your responses should be coherent, creative, and job-relevant."""

MAKE_UP_BIOGRAPHY_PROMPT = """
You are given a short prompt describing a person who wants to create a resume.
Your task is to creatively fill in all missing details in their biography, including:
- Full name (if not provided)
- Age (if not provided)
- Education history (degrees, institutions, years)
- Work experience (roles, companies, responsibilities)
- Skills and certifications
- Awards or personal achievements (optional)

The goal is to make this person a plausible candidate for their target job. Make sure the biography is coherent and reflects both the person's background and aspirations.

Prompt:
{input_prompt}

Biography:"""

GENERATE_RESUME_PROMPT = """
You are given a full biography of a person. Write a clean, modern, and professional one-page HTML resume (with embedded CSS) based on it.

The resume should:
- Be responsive and styled appropriately with inline or embedded CSS
- Contain sections like Name, Contact, Summary, Education, Work Experience, Skills
- Be readable and nicely formatted
- Contain no JavaScript

Biography:
{biography}

Resume HTML:"""

VALIDATE_RESUME_PROMPT = """
You are a strict HTML and CSS code reviewer. You will be given the HTML and CSS content of a resume.

Your task is to:
- Check for syntax errors (unclosed tags, wrong nesting, invalid attributes)
- Check if the structure includes expected resume sections
- Validate that CSS rules are applied correctly

Respond with one of the following:
- "VALID" if everything is fine
- "INVALID: <reason>" with a short explanation of what is wrong

Resume Code:
{resume_code}
"""
