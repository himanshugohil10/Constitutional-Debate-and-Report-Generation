class DebateManager:
    def __init__(self, llm_client, rag_data):
        self.llm = llm_client
        self.rag_data = rag_data

    def construct_debate_prompt(self, role, case_summary, history):
        """
        Constructs the prompt for a debate round.
        """
        system_prompt = f"""You are an expert constitutional lawyer arguing the {role} side of a case.
        
        STRICT OUTPUT CONSTRAINTS:
        1. Produce NO MORE THAN 3 points.
        2. Use NO MORE THAN 200 words total.
        3. Do not declare a winner or provide legal advice.
        4. Focus on constitutional arguments based on the provided data.
        
        RAG DATA (Authoritative Grounding):
        {self.rag_data}
        """

        user_prompt = f"""
        CASE SUMMARY:
        {case_summary}

        DEBATE HISTORY:
        {history}

        Your task:
        Argue {role} this case. 
        Build on previous arguments. 
        Avoid repetition. 
        Introduce new reasoning or rebuttals.
        """
        
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

    def construct_report_prompt(self, role, case_summary, full_history):
        """
        Constructs the prompt for the final report.
        """
        system_prompt = f"""You are a legal strategist generating a final report for the {role} side.
        
        RAG DATA:
        {self.rag_data}
        """

        user_prompt = f"""
        CASE SUMMARY:
        {case_summary}

        FULL DEBATE TRANSCRIPT:
        {full_history}

        Your task:
        Generate a strategic report for the {role} side.
        
        REQUIRED SECTIONS:
        
        Section 1: Case Summary ({role} perspective)
        
        Section 2: Constitutional Traceability of Arguments
        For each major argument, exact constitutional grounding is required.
        - Trace each argument ONLY to: Article 14, Article 19, Article 21, or the doctrines of Reasonable Restrictions, Proportionality, Arbitrariness, or Chilling Effect.
        - Label each argument as one of the following:
            - **[Grounded]**: Clearly linked to one of the above.
            - **[Needs Stronger Constitutional Anchor]**: Argument is relevant but weak in text/doctrine.
            - **[Ungrounded]**: No clear link to the allowed list.
        - If an argument is [Needs Stronger Constitutional Anchor] or [Ungrounded], provide one brief line suggesting which Article or doctrine could strengthen it.
        - Keep this section concise, practical, and focused strictly on traceability.

        Section 3: Likely counterpoints and Rebuttals
        - Identify likely counterpoints from the opposing side.
        - Provide brief rebuttals.

        CONSTRAINT:
        - Output format: Markdown (.md)
        - Length: Less than 2 pages
        - Do not predict outcomes or give legal advice.
        """

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
