from PyPDF2 import PdfReader

def extract_pdf_text(pdf_path):
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): The file path to the PDF document.

    Returns:
        str: The extracted text from the PDF document, with all pages concatenated into a single string.
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def process_output(summaries):
    """
    Processes summarized text into specific categories: Financial Performance, Market Dynamics, Expansion Plans, 
    Environmental Risks, and Regulatory or Policy Changes.

    Args:
        summaries (list of str): A list of summarized text strings, where each string corresponds to a section of content.

    Returns:
        tuple: A tuple containing the following five strings:
            - financial_performance (str): Summary related to Financial Performance.
            - market_dynamics (str): Summary related to Market Dynamics.
            - expansion_plans (str): Summary related to Expansion Plans.
            - environmental_risks (str): Summary related to Environmental Risks.
            - regulatory_or_policy_changes (str): Summary related to Regulatory or Policy Changes.
    """
    financial_performance, market_dynamics, expansion_plans, environmental_risks, regulatory_or_policy_changes = "", "", "", "", ""

    if len(summaries) > 8:
        financial_performance_index, market_dynamics_index, expansion_plans_index, environmental_risks_index, regulatory_or_policy_changes_index = -1, -1, -1, -1, -1
        
        for ind, val in enumerate(summaries):
            if "Financial Performance:" in val:
                financial_performance_index = ind
            elif "Market Dynamics:" in val:
                market_dynamics_index = ind
            elif "Expansion Plans:" in val:
                expansion_plans_index = ind
            elif "Environmental Risks:" in val:
                environmental_risks_index = ind
            elif "Regulatory Or Policy Changes:" in val:
                regulatory_or_policy_changes_index = ind

        financial_performance = (''.join(summaries[financial_performance_index+1:market_dynamics_index])).replace('*','')
        market_dynamics = (''.join(summaries[market_dynamics_index+1:expansion_plans_index])).replace('*','')
        expansion_plans = (''.join(summaries[expansion_plans_index+1:environmental_risks_index])).replace('*','')
        environmental_risks = (''.join(
            summaries[environmental_risks_index                                +1:regulatory_or_policy_changes_index])).replace('*','')
        regulatory_or_policy_changes = (''.join(summaries[regulatory_or_policy_changes_index+1:])).replace('*','')
    else:
        if len(summaries) in [6,7]:
            financial_performance = (summaries[1].split("**"))[-1]
            market_dynamics = (summaries[2].split("**"))[-1]
            expansion_plans = (summaries[3].split("**"))[-1]
            environmental_risks = (summaries[4].split("**"))[-1]
            regulatory_or_policy_changes = (summaries[5].split("**"))[-1]
        elif len(summaries)==5:
            financial_performance = (summaries[0].split("**"))[-1]
            market_dynamics = (summaries[1].split("**"))[-1]
            expansion_plans = (summaries[2].split("**"))[-1]
            environmental_risks = (summaries[3].split("**"))[-1]
            regulatory_or_policy_changes = (summaries[4].split("**"))[-1] 

    return financial_performance, market_dynamics, expansion_plans, environmental_risks, regulatory_or_policy_changes