# Rule: Workflow Integrity

1.  **Phase-Gate Protocol**: Never skip phases. Every task must follow: `Research -> Outline -> User Approve -> Draft -> Feedback -> Finalize`.
2.  **No Hallucinations**: All interest rates, market data, and facts must be grounded in SERP or Knowledge Base. If data is missing, STOP and ask the user.
3.  **Mandatory Approval**: Do not proceed to Drafting without a clear `/approve` on the Outline. Do not Finalize without a clear `/approve` on the Draft.
