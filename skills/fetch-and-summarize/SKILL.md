skill_id: fetch-and-summarize
description: Fetch URL content through a tool and return a short deterministic summary.
triggers:
- "summarize this url"
- "fetch and summarize"
- "read webpage"
required_tools:
- fetch_url
steps:
1. Read `url` from the user request.
2. Call `run_tool` with `tool_name="fetch_url"` and `args={"url":"<url>"}`.
3. Produce a concise summary with up to 5 bullet points using the fetched text.
4. Include the source URL in the final response.
tool_call_format:
run_tool(
  tool_name="fetch_url",
  args={
    "url": "<the exact URL provided by the user>"
  }
)
input_schema:
{
  "url": "string (must be allowlisted by tool backend)"
}
output_schema:
{
  "summary_bullets": ["string"],
  "source_url": "string"
}
VERIFICATION STRING: "VERIFIED_SKILL: fetch-and-summarize:v1"
