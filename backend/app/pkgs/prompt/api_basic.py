from app.pkgs.tools.llm import chatCompletion
from app.pkgs.prompt.api_interface import ApiInterface
from app.pkgs.knowledge.app_info import getServiceSwagger

class ApiBasic(ApiInterface):
    def clarifyAPI(self, userPrompt, apiDoc):
        message, ctx, success = step1ApiDocTasks(userPrompt, apiDoc)
        if success:
            return step2GenApiDoc(message, ctx)
        else:
            return message, False
    
def step2GenApiDoc(message, context):
    context.append({
        "role": "assistant",
        "content": message
        })
    
    context.append({
        "role": "user",
        "content": """Summarize all subtasks to output a swagger API.
        
note that it contains only the parts that need to be modified for new requirements, delete the parts that have nothing to do with new requirements.
        
Without any dialogue or explanation, just output the final API only."""})

    return chatCompletion(context)

def step1ApiDocTasks(user_prompt, apiDoc):
    context = []
    content = """As a senior full stack developer, Your task is to design the swagger API and add detailed business logic comments to the API. Now you need to think step-by-step based on the requirements document and the Existing API of the existing project, analyze what needs to be adjusted to meet the requirements, and break down the content into multiple subtasks, describing each subtask in as much detail as possible.

Attention:
1. Think repeatedly whether the needs are reasonably satisfied;
2. Make only minimal changes to meet the requirements;
3. You are only responsible for meeting the new requirements on the basis of the existing API, and do not modify the parts unrelated to this requirement;
4. Always reflect, subtasks are only responsible for completing the design requirements of the API, and do not need to focus on the parts unrelated to the API.
5. try to implement functionality in just one interface.

requirements document：
```
""" + user_prompt + """
```

Existing API：
```
""" + apiDoc + """
```
"""

    context.append({"role": "system", "content": content})
    message, success = chatCompletion(context)

    return message, context, success