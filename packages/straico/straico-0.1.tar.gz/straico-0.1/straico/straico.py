import requests

# client implementation of
# https://documenter.getpostman.com/view/5900072/2s9YyzddrR

__version__ = 0.1

class StraicoClient:
    base_url = "https://api.straico.com/v0/"

    def __init__(self, api_key: str):
        """
        Takes in the Straico API key for authorization
        """
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def get_user_data(self) -> dict:
        """
        This endpoint allows users to fetch details of a specific user from the Straico platform. By sending a GET request to the provided URL, including the necessary Authorization header with the user's unique API key, users can access information such as the user's first name, last name, the number of coins associated with the account, and the plan they are subscribed to.

        Returns:
            JSON object containing the user's data, including their first name, last name, available coins, and current plan under the "data" key.
        """
        endpoint = self.base_url + "user"
        response = self._make_request("GET", endpoint)
        """
        {
  "data": {
    "first_name": "Jane",
    "last_name": "Doe",
    "coins": 562621.19,
    "plan": "Ultimate Pack"
  },
  "success": true
}
        """
        if response:
            return response["data"]

    def get_model_data(self) -> dict:
        """
        This endpoint allows users to fetch a list of available models along with their details from the Straico API. By sending a GET request to the provided URL and including the required Authorization header with the user's unique API key, users can access information about various models offered by Straico and their associated pricing.

        Returns:
            JSON object containing an array of model objects. Each model object includes details such as the model's name, unique model identifier, and pricing information. The pricing information consists of the cost in coins and the word limit for each model.
        """
        endpoint = self.base_url + "models"
        response = self._make_request("GET", endpoint)
        """
        {
  "data": [
    {
      "name": "Anthropic: Claude Instant v1",
      "model": "anthropic/claude-instant-v1",
      "pricing": {
        "coins": 2,
        "words": 100
      }
    },
    {
      "name": "Anthropic: Claude v2.0",
      "model": "anthropic/claude-2.0",
      "pricing": {
        "coins": 8,
        "words": 100
      }
    },
    {
      "name": "Anthropic: Claude v2.1",
      "model": "anthropic/claude-2",
      "pricing": {
        "coins": 8,
        "words": 100
      }
    },
    {
      "name": "Dolphin 2.6 Mixtral 8x7B",
      "model": "cognitivecomputations/dolphin-mixtral-8x7b",
      "pricing": {
        "coins": 1,
        "words": 100
      }
    },
    {
      "name": "Goliath 120B",
      "model": "alpindale/goliath-120b",
      "pricing": {
        "coins": 5,
        "words": 100
      }
    },
    {
      "name": "Google: Gemini Pro (preview)",
      "model": "google/gemini-pro",
      "pricing": {
        "coins": 1,
        "words": 100
      }
    },
    {
      "name": "Google: PaLM 2 Chat 32k",
      "model": "google/palm-2-chat-bison-32k",
      "pricing": {
        "coins": 1,
        "words": 100
      }
    },
    {
      "name": "Gryphe: MythoMax L2 13B 8k (beta)",
      "model": "gryphe/mythomax-l2-13b-8k",
      "pricing": {
        "coins": 1,
        "words": 100
      }
    },
    {
      "name": "Meta: CodeLlama 70B Instruct",
      "model": "codellama/codellama-70b-instruct",
      "pricing": {
        "coins": 1,
        "words": 100
      }
    },
    {
      "name": "Meta: Llama v2 70B Chat (beta)",
      "model": "meta-llama/llama-2-70b-chat",
      "pricing": {
        "coins": 1,
        "words": 100
      }
    },
    {
      "name": "Mistral 7B Instruct v0.1 (beta)",
      "model": "mistralai/mistral-7b-instruct",
      "pricing": {
        "coins": 1,
        "words": 100
      }
    },
    {
      "name": "Mistral: Medium",
      "model": "mistralai/mistral-medium",
      "pricing": {
        "coins": 3,
        "words": 100
      }
    },
    {
      "name": "Mistral: Mixtral 8x7B (beta)",
      "model": "mistralai/mixtral-8x7b-instruct",
      "pricing": {
        "coins": 1,
        "words": 100
      }
    },
    {
      "name": "OpenAI: GPT-3.5 Turbo 16k",
      "model": "openai/gpt-3.5-turbo-0125",
      "pricing": {
        "coins": 0,
        "words": 100
      }
    },
    {
      "name": "OpenAI: GPT-4",
      "model": "openai/gpt-4",
      "pricing": {
        "coins": 20,
        "words": 100
      }
    },
    {
      "name": "OpenAI: GPT-4 Turbo 128k - Preview",
      "model": "openai/gpt-4-0125-preview",
      "pricing": {
        "coins": 8,
        "words": 100
      }
    }
  ],
  "success": true
}
        """
        if response:
            return response["data"]

    def make_model_request(self, model: str, message: str) -> dict:
        """
        This endpoint enables users to generate prompt completion based on a specified model using the Straico API. By making a POST request to the provided URL and including the necessary Authorization header with the user's unique API key, along with setting the Content-Type to application/x-www-form-urlencoded, users can request prompt completion for a given message input under a particular model.

        Params:
            model: Specifies the model under which the prompt completion will be generated (e.g., 'anthropic/claude-2.0').
            message: Represents the message for which prompt completion is requested

        Returns:
            JSON object containing the prompt completion generated based on the provided message input. Additionally, the response includes details such as the generated completion content, finish reason, model used, completion ID, object type, creation timestamp, usage metrics (prompt tokens, completion tokens, total tokens), pricing information (input cost, output cost, total cost), and word count details (input words, output words, total words).
        """
        data = {"model": model, "message": message}
        endpoint = self.base_url + "prompt/completion"
        response = self._make_request("POST", endpoint, data=data)
        """
        {
        "data": {
            "completion": {
      "choices": [
        {
          "message": {
            "role": "assistant",
            "content": " Here are 5 tips for recycling at home in markdown format:\n\n# 5 Tips for Recycling at Home\n\nRecycling at home is one of the easiest ways to reduce your environmental impact. Here are 5 tips to help you recycle more effectively:\n\n## 1. Learn what can and can't be recycled in your area\n\nEvery municipality has slightly different rules about what can go in your recycling bin. Check with your local recycling program to find out which types of plastic, paper, glass, and metal they accept. \n\n## 2. Rinse food residue off items before recycling\n\nGive recyclable items a quick rinse before tossing them in the bin. Food residue can contaminate other recyclables.\n\n## 3. Flatten cardboard boxes and plastic bottles\n\nFlattening cardboard boxes and plastic bottles saves space in your recycling bin and in recycling trucks. More materials can be transported at once when items are flattened out.\n\n## 4. Keep a recycling bin in every room\n\nHaving recycling bins throughout the house makes it easy to recycle as you go. Place bins in kitchens, offices, bedrooms, and bathrooms.\n\n## 5. Avoid \"wishcycling\" \n\nWishcycling is when you toss questionable items in the recycling in hopes that they can be recycled. This causes contamination. Only recycle items you know are accepted by your program. When in doubt, throw it out.\n\nFollowing these simple tips will help you maximize your recycling efforts at home and reduce waste. Every bottle, can, and box makes a difference!"
          },
          "finish_reason": "stop_sequence"
        }
      ],
      "model": "anthropic/claude-2.0",
      "id": "gen-7KcpqQ4VHVcJXkcqWOPKIGXUMWRU",
      "object": "chat.completion",
      "created": 1707670927,
      "usage": {
        "prompt_tokens": 26,
        "completion_tokens": 329,
        "total_tokens": 355
      }
    },
    "price": {
      "input": 1.2,
      "output": 19.6,
      "total": 20.8
    },
    "words": {
      "input": 15,
      "output": 245,
      "total": 260
    }
  },
  "success": true
}"""
        if response:
            return response["data"]

    def _make_request(self, method: str, url: str, **kwargs):
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            print(f"Response content: {e.response.content}")  # Add this line to log the error response
            return None
