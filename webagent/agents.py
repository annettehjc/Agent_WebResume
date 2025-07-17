import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables.graph import MermaidDrawMethod
from typing import TypedDict, List
import nest_asyncio
import dotenv
dotenv.load_dotenv()    # that loads the .env file variables into os.environ
nest_asyncio.apply()  # apply nest_asyncio to allow nested event loops


from webagent.prompts import (
    SYSTEM_PROMPT,
    MAKE_UP_BIOGRAPHY_PROMPT,
    GENERATE_RESUME_PROMPT,
    VALIDATE_RESUME_PROMPT
)

# choose any model, catalogue is available under https://build.nvidia.com/models
MODEL_NAME = "meta/llama-3.3-70b-instruct"


class ResumeGenerator:

    def __init__(self, max_refinements: int=5, **kwargs):
        self.llm = ChatNVIDIA(          
                    model=MODEL_NAME,
                    api_key=os.getenv("NVIDIA_API_KEY"), 
                    temperature=0.9,   
                    )
        self.max_refinements = max_refinements

    def complete_biography(self, input_prompt: str) -> AIMessage:

        """
        Fill in the gaps in the character's biography:
        everything that is relevant for a resume, such as
        education, work experience, skills, etc.
        
        Args:
            input_prompt (str): The initial (partial) description of the character
            
        Returns:
            AIMessage: The completed biography of the character
        """

        prompt = MAKE_UP_BIOGRAPHY_PROMPT.format(input_prompt=input_prompt)
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ]
        response = self.llm.invoke(messages)
        return response
    
    def generate_resume(self, biography: str) -> AIMessage:

        """
        Generate HTML (and CSS) code for a one-page resume based on the character biography.
        
        Args:
            biography (str): The complete biography of the character
            
        Returns:
            AIMessage: The HTML (and CSS) code for the resume
        """

        prompt = GENERATE_RESUME_PROMPT.format(biography=biography)
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ]
        response = self.llm.invoke(messages)
        return response

    
    def validate_resume(self, resume_code: str) -> bool:

        """
        Validate the generated HTML (and CSS) code for the resume.
        It should check if the HTML is well-formed and if the CSS styles are applied correctly.
        
        Args:
            resume_code (str): The HTML (and CSS) code for the resume
            
        Returns:
            bool: Whether the resume code is valid or not
        """
        prompt = VALIDATE_RESUME_PROMPT.format(resume_code=resume_code)
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ]
        response = self.llm.invoke(messages)
        return "VALID" in response.content.upper()

    
    def refine_resume_code(self, resume_code: str) -> AIMessage:
        
        """
        Refine the generated HTML (and CSS) code for the resume.
        It should fix technical errors in the code as well as
        change contents if they are not matching the biography.
        
        Args:
            resume_code (str): The HTML (and CSS) code for the resume
            
        Returns:
            AIMessage: The refined HTML (and CSS) code for the resume
        """
        # Optionally use biography for context
        prompt = (
            f"Refine the following resume code to fix any errors and ensure it matches the biography.\n"
            f"Resume Code:\n{resume_code}"
        )
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ]
        response = self.llm.invoke(messages)
        return response

    def save_resume(self, resume_code: str) -> None:

        """
        Save the generated HTML (and CSS) code for the resume to a file.
        
        Args:
            resume_code (str): The HTML (and CSS) code for the resume
        """
        filename: str = "resume.html"
        with open(filename, "w") as f:
            f.write(resume_code)
    
    def run(self,query: str) -> AIMessage:

        """
        Run the agent with the given query.
        """

        biography_msg = self.complete_biography(query)
        biography = biography_msg.content
        resume_msg = self.generate_resume(biography)
        resume_code = resume_msg.content

        for i in range(self.max_refinements):
            if self.validate_resume(resume_code):
                self.save_resume(resume_code)
                print(f"Resume saved after {i+1} attempt(s).")
                return resume_msg
            else:
                print(f"validation failed, refining resume (attempt {i+1})...")
                resume_msg = self.refine_resume_code(resume_code, biography)
                resume_code = resume_msg.content

        print("max refinements reached. Resume may not be valid.")
        self.save_resume(resume_code)
        return resume_msg