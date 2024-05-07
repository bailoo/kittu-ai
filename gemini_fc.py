
import google.generativeai as genai
import google.ai.generativelanguage as glm

def gemini(prompt):
    GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
    genai.configure(api_key=GOOGLE_API_KEY)

    fees = glm.Schema(
        type = glm.Type.OBJECT,
        properties = {
            'program': glm.Schema(type=glm.Type.STRING),
            'fees': glm.Schema(type=glm.Type.NUMBER),
            'period': glm.Schema(type=glm.Type.STRING)
        },
        required = ['program', 'fees', 'period']
    )

    printfees = glm.FunctionDeclaration(
        name="printfees",
        description=textwrap.dedent("""\
            prints fees.
            """),
        parameters=glm.Schema(
            type=glm.Type.OBJECT,
            properties = {
                'fees': fees
            }
        )
    )

    model = genai.GenerativeModel(
        model_name = 'gemini-pro',
        #model_name = 'gemini-1.5-pro-latest',
        tools = [printfees]
    )

    try:
        response = model.generate_content(prompt)
            #tool_config={'function_calling_config':'ANY'})
        return response
    
    except Exception as e:
        print(f"An error occurred while Gemini: {str(e)}")
        return [f"Error: {str(e)}"]

def get_pagetext(web_url):
    return

def get_fees(web_url, collname, course):
        pagetext = get_pagetext(web_url)
        if pagetext:
            result = gemini("""\
                Please return as a single piece of valid JSON text the fees for """ + course + """ program using the following schema: 
                {"program": PROGRAM, "fees": num, "period": PERIOD} 
                PROGRAM = academic program
                PERIOD = time period
                """ + pagetext)

            try:
                response = result.candidates[0].content.parts[0]

                #print(response.prompt_feedback, flush=True)
                #print(response.candidates, flush=True)
                #to_markdown(response.text)
    
                #if hasattr(response, 'text'):
                    #print(response.text)

                if hasattr(response, 'function_call'):
                    fc = response.function_call
                    #print(fc)
                    llm_output = json.dumps(type(fc).to_dict(fc), indent=4)
                    fwrite(llm_output_file, llm_output)
                    return llm_output
                else:
                    print("Error: No text response from Gemini")
                    return None
    
            except Exception as e:
                error_message = f"An error occurred while scraping the page: {str(e)}"
                print(error_message)
                return None

def main():
    web_url = "https://isbmb.ac.in/fees-structure"
    collname = "ISBMB"
    course = "Master of Arts in Mass Communication, Advertisement and Journalism (MAMCAJ)"
    fees = get_fees(web_url, collname, course)
    print(fees)

if __name__ == "__main__":
    main()
