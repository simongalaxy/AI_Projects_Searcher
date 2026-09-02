import asyncio
import os
from typing import List, Optional
import instructor
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

# 1. Define the schema matching your exact data requirements
class AIProjectDetails(BaseModel):
    project_name: str = Field(description="The formal name of the AI project or system.")
    description: str = Field(description="A brief summary of what the AI project does.")
    benefits: List[str] = Field(description="List of benefits or improvements brought by this AI project.")
    ai_tools: List[str] = Field(description="Specific AI models, algorithms, technologies, or tools used.")
    launch_date: str = Field(description="The scheduled or actual launch date mentioned, or 'Unknown'.")

class PressReleaseAnalysis(BaseModel):
    contains_ai_project: bool = Field(description="True if the text contains one or more AI projects, False otherwise.")
    projects: Optional[List[AIProjectDetails]] = Field(
        default=None, 
        description="A list of project details. Must be None or empty if contains_ai_project is False."
    )

# 2. Patch the AsyncOpenAI client with Instructor
# This adds the 'response_model' parameter to the client's chat completion methods
client = instructor.apatch(AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY")))

async def analyze_press_release(text: str) -> Optional[List[AIProjectDetails]]:
    prompt = f"""
    Analyze the following press release text. Determine if it contains any Artificial Intelligence (AI), 
    Machine Learning (ML), or Deep Learning projects. 

    If it does, set contains_ai_project to True and extract all project details according to the schema.
    If no AI/ML projects are mentioned, set contains_ai_project to False and leave the projects list as None.

    Press Release Text:
    {text}
    """
    
    # 3. Call the OpenAI API using instructor's structure enforcement
    result: PressReleaseAnalysis = await client.chat.completions.create(
        model="gpt-4o-mini",  # Highly efficient and cost-effective for structured extraction
        response_model=PressReleaseAnalysis,
        temperature=0.0,      # Keeps extraction deterministic and factually grounded
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    
    # 4. Return the structured project details if found, otherwise return None
    if result.contains_ai_project and result.projects:
        return result.projects
    return None

async def main():
    # Sample Test Case A: Press release with AI content
    ai_release = """
    TechCorp today announced the rollout of 'NexusDrive', its new cloud management system. 
    Powered by an internal predictive machine learning algorithm and utilizing the OpenAI GPT-4o API, 
    NexusDrive automatically allocates server resources to prevent downtime. Early beta testing 
    showed a 40% reduction in hosting costs and 99.99% uptime. The tool is slated for a global 
    commercial launch on November 15, 2026.
    """
    
    # Sample Test Case B: Press release without AI content
    non_ai_release = """
    Global Logistics Inc. announced today that it has expanded its delivery fleet by purchasing 50 new 
    eco-friendly electric transit vans. The expansion aims to lower carbon emissions across major European 
    shipping routes by the end of Q4.
    """
    
    print("--- Processing Press Release A ---")
    projects_a = await analyze_press_release(ai_release)
    if projects_a:
        # Instructor yields fully parsed, type-safe Pydantic objects natively
        for proj in projects_a:
            print(f"Project Name: {proj.project_name}")
            print(f"Description: {proj.description}")
            print(f"AI Tools Used: {', '.join(proj.ai_tools)}")
            print(f"Benefits: {', '.join(proj.benefits)}")
            print(f"Launch Date: {proj.launch_date}\n")
    else:
        print("None")
        
    print("--- Processing Press Release B ---")
    projects_b = await analyze_press_release(non_ai_release)
    if projects_b:
        print(projects_b)
    else:
        print("None")

# Run the async loop
if __name__ == "__main__":
    asyncio.run(main())
