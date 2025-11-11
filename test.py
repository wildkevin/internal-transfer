I need to design a multi-agent AI framework, and first I need create a planner agent.

Here is my problem statement for my framework
 New product launch still relies on sales manually search for likely clients - slow and limited coverage. e.g. when we launched Silver Forward, sales need manually search the possible corporate clients via web page (clients use Silver in the operation process thus has the needs to hedge the risk with the new product), and also have difficulty to identify the hidden needs from corporate families and supply chain

The user will input Target Product, Target customer type, Target industry, Target customer region, Target customer behavior
Exmaple 1:
Precious Metals – Silver (Ag)
Multinational manufacturers (including JVs in China)
Solar panels / automotive parts / medical devices Mainland China production sites (incl. export manufacturers in Yangtze River Delta, Pearl River Delta)
o Identify firms that physically consume silver as raw material (e.g. PV cells, catalytic parts, X-ray devices)
 o Exclude clients that only purchase semi-finished goods containing silver — their supplier already hedges.
o Prioritize importers of silver, silver powder, or silver wire in customs / trade data.
Example 2:
MENAT FX Solutions
Chinese SOEs and subsidiaries (central SOEs, provincial SOEs, large EPCs)
Engineering, power, energy, infrastructure construction
MENAT region (Middle East, North Africa, Türkiye)
o   Clients benefiting from Belt & Road Initiative projects in MENAT. o   Typical needs: project FX exposure, local-currency conversion, offshore liquidity mgmt. o   Common pain points: 1. Short-term offshore funding difficulty (fragmented projects). 2. Poor FX / rates market-timing ability. 3. Idle small-currency balances. 4. Mismatch between contract vs. actual revenue currency. o   Identify entities with multiple MENAT EPC projects (Egypt, Saudi, UAE, Algeria, etc.).

Then give me a planner agent initialization, which should include name, description, and instruction, where:
name: Every agent needs a unique string identifier. This name is crucial for internal operations, especially in multi-agent systems where agents need to refer to or delegate tasks to each other. Choose a descriptive name that reflects the agent's function 
description Provide a concise summary of the agent's capabilities. This description is primarily used by other LLM agents to determine if they should route a task to this agent. Make it specific enough to differentiate it from peers (e.g., "Handles inquiries about current billing statements," not just "Billing agent").
 instruction parameter is arguably the most critical for shaping an LlmAgent's behavior. It's a string (or a function returning a string) that tells the agent:Its core task or goal.
Its personality or persona (e.g., "You are a helpful assistant," "You are a witty pirate"). Constraints on its behavior (e.g., "Only answer questions about X," "Never reveal Y"). How and when to use its tools. You should explain the purpose of each tool and the circumstances under which it should be called, supplementing any descriptions within the tool itself. The desired format for its output (e.g., "Respond in JSON," "Provide a bulleted list"). Be Clear and Specific: Avoid ambiguity. Clearly state the desired actions and outcomes. Use Markdown: Improve readability for complex instructions using headings, lists, etc. Provide Examples (Few-Shot): For complex tasks or specific output formats, include examples directly in the instruction. Guide Tool Use: Don't just list tools; explain when and why the agent should use them.

Example:

capital_agent = LlmAgent(
    name="capital_agent",
    description="Answers user questions about the capital city of a given country.",
    instruction="""You are an agent that provides the capital city of a country.
When a user asks for the capital of a country:
1. Identify the country name from the user's query.
2. Use the `get_capital_city` tool to find the capital.
3. Respond clearly to the user, stating the capital city.
Example Query: "What's the capital of {country}?"
Example Response: "The capital of France is Paris."
""",
    # tools will be added next
)

planner_agent = LlmAgent(
    name="planner_agent",
    description="Identifies potential clients for new product launches based on specified criteria.",
    instruction="""You are a planner agent tasked with identifying potential clients for new product launches.
Your goal is to streamline the process by leveraging client data and identifying hidden needs within corporate families and supply chains.
When a user provides the necessary parameters (Target Product, Target customer type, Target industry, Target customer region, Target customer behavior):
1. Analyze these inputs to identify potential clients who might benefit from the new product.
2. Use available data sources (e.g., trade data, customs data, industry reports) to refine the list of potential clients.
3. Prioritize clients based on specific criteria such as import/export behavior, consumption of raw materials, and involvement in relevant projects.
4. Exclude entities that are unlikely to benefit directly (e.g., those whose suppliers already hedge risks).
5. Provide a concise report including prioritized client list and rationale for each choice.
Constraints:
- Focus only on the specified target regions and industries.
- Ensure the list is relevant to the defined target customer behavior.
- Never include clients outside the specified scope.
Desired Output Format:
- Provide the results in a structured format, such as a JSON object or a bulleted list.
Example Input:
Target Product: Precious Metals – Silver (Ag)
Target customer type: Multinational manufacturers
Target industry: Solar panels / automotive parts / medical devices
Example Output:
- Company A: Manufacturer of PV cells, imports silver powder.
- Company B: Automotive parts producer in Yangtze River Delta, consumes silver wire.
Guide Tool Use:
- Utilize data mining tools and APIs to gather necessary data about companies.
- Employ analytics tools to assess and prioritize potential client engagement.
""",
)
