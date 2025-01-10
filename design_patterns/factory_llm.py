from abc import ABC, abstractmethod


# 1. Product Abstract Class
class LLM(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, max_tokens: int, temperature: float) -> None:
        pass


# 2. Concrete Products
class OpenAILLM(LLM):
    def generate_text(self, prompt: str, max_tokens: int, temperature: float) -> None:
        print(f"Generated text from OpenAI: {prompt} | {max_tokens} | {temperature}")


class AnthropicLLM(LLM):
    def generate_text(self, prompt: str, max_tokens: int, temperature: float) -> None:
        print(f"Generated text from Anthropic: {prompt} | {max_tokens} | {temperature}")


class HuggingFaceLLM(LLM):
    def generate_text(self, prompt: str, max_tokens: int, temperature: float) -> None:
        print(
            f"Generated text from HuggingFace: {prompt} | {max_tokens} | {temperature}"
        )


# 3. Creator (Factory) Abstract Class
class LLMFactory(ABC):
    @staticmethod
    def create_llm(llm_type: str) -> LLM:
        if llm_type == "OPENAI":
            return OpenAILLM()
        elif llm_type == "ANTHROPIC":
            return AnthropicLLM()
        elif llm_type == "HUGGINGFACE":
            return HuggingFaceLLM()
        else:
            raise ValueError(f"Invalid LLM type: {llm_type}")


# 4. Concrete Products Creators

if __name__ == "__main__":
    factory = LLMFactory()
    user_prefernce: list[str] = ["OPENAI", "ANTHROPIC", "HUGGINGFACE"]
    for prefernce in user_prefernce:
        llm: LLM = factory.create_llm(llm_type=prefernce)
        llm.generate_text(prompt="Tell me a Joke!", max_tokens=100, temperature=0.8)
