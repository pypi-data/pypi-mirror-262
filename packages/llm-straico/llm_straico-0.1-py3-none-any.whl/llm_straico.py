import straico
import llm
import os

client = straico.StraicoClient(os.environ.get("STRAICO_API_KEY"))

@llm.hookimpl
def register_models(register):
    register(StraicoGPT35())

class StraicoGPT35(llm.Model):
    model_id = "straico-gpt-3.5"

    def execute(self, prompt, stream, response, conversation):
        result = client.make_model_request("openai/gpt-3.5-turbo-0125", prompt)['completion']['choices'][0]['message']['content']
        return result
                                                                                                  