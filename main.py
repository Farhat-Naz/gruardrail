from logging import config
from agents import Agent, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered, Runner, input_guardrail, output_guardrail
import rich
import asyncio
from connection import RunConfig
from pydantic import BaseModel

from new import og_main




class PassengerOutput(BaseModel):
    response:str
    isWeightExceed:bool



airport_security_guard = Agent (name="airport security guard", instructions = """ Your task is to check the passenger luggage.
        If passenger's luggage is more then 25KGs, gracefully stop them""",
        output_type = PassengerOutput
        )



@input_guardrail
async def security_guardrail(ctx, agent, inpurt):
    result = await Runner.run(airport_security_guard, input, run_config = config)
    rich.print(result.final_output)
    
    return GuardrailFunctionOutput(
        output_info= result.final_output.response,
        tripwire_triggered= result.final_output.isWeightExceed
    )
    
    
    
    

passenger_agent = Agent (name="passenger agent", instructions = "You are a passenger agent",
                        input_guardrails = [security_guardrail]
                        )

async def main():
    try:
        result = await Runner.run(passenger_agent, "My luggage weight is 25kg, run_config=config")
    except InputGuardrailTripwireTriggered:
        print("passenger cannot checkin")    
        
        
        
        
        #output guardrails 
class MessageOutput(BaseModel):
    resp: str

class PHDOutput(BaseModel):
    isPHDLevelResponse: bool         
    
phd_guardrail_agent=Agent(name = "PHD Guardrail Agent",
    instructions="""
        You are a PHD Guardrail Agent that evaluates if text is too complex for 8th grade students. If the response if 
        very hard to read for an eight grade student deny the agent response
    """,
    output_type = PHDOutput)       


@output_guardrail
async def PHD_guardrail(ctx, agent:Agent, output):
    result = await Runner.run(phd_guardrail_agent,output.response, run_config = config)        
    return GuardrailFunctionOutput(
        output_info = result.final_output,
        tripwire_trigerred=result.final_output.isPHDLevelResponse
    )
eight_grade_agent = Agent(name = "Eight grade student", instructions = "you are a student that answer the query to eight grade student, keep your vocablary simple and easy",
output_type = MessageOutput,
output_guardrails=[PHD_guardrail]   
)     

async def og_main():
    query = "What are trees? Explain using the most complex scientific terminology possible"
    # query = "What are trees? Explain in simple words"
    try:
        result = await Runner.run(eight_grade_agent, query, run_config=config)
        print(result.final_output)

    except OutputGuardrailTripwireTriggered:
        print('Agent output is not according to the expectations')
    
    
    
        
if __name__ == "__main__":
    asyncio.run(og_main())
    asyncio.run(main())        