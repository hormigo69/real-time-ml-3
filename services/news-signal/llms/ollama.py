from typing import Literal, Optional

from llama_index.llms.ollama import Ollama
from llama_index.core.prompts import PromptTemplate

from .base import BaseNewsSignalExtractor, NewsSignal


class OllamaNewsSignalExtractor(BaseNewsSignalExtractor):
    def __init__(
        self,
        model_name: str,
        temperature: Optional[float] = 0,
    ):
        self.llm = Ollama(
            model=model_name,
            temperature=temperature,
        )

        self.prompt_template = PromptTemplate(
            template="""
            You are a financial analyst.
            You are given a news article and you need to determine the impact of the news on the BTC and ETH prices.

            You need to output the signal in the following format:
            {
                "btc_signal": 1,
                "eth_signal": 0
            }

            The signal is either 1, 0, or -1.
            1 means the price is expected to go up.
            0 means the price is expected to stay the same.
            -1 means the price is expected to go down.

            Here's the news article:
            {news_article}
            """
        )

        self.model_name = model_name

    def get_signal(
        self,
        text: str,
        output_format: Literal["dict", "NewsSignal"] = "dict",
    ) -> dict | NewsSignal:
        """
        Get the news signal from the given "text"

        Args:
            text (str): The news article to analyze
            output_format (Literal["dict", "NewsSignal"]): The format of the output

        Returns:
            dict | NewsSignal: The news signal
        """
        response: NewsSignal = self.llm.structured_predict(
            NewsSignal,
            prompt=self.prompt_template,
            news_article=text,
        )

        if output_format == "dict":
            return response.to_dict()
        else:
            return response


if __name__ == "__main__":
    from .config import OllamaConfig

    config = OllamaConfig()

    llm = OllamaNewsSignalExtractor(
        model_name=config.model_name,
    )

    examples = [
        "Bitcoin ETF ads spotted on China's Alipay payment app",
        "U.S. Supreme Court Lets Nvidia's Crypto Lawsuit Move Forward",
        "Trump's World Liberty Acquires ETH, LINK, and AAVE in $12M Crypto Shopping Spree",
    ]

    for example in examples:
        print(f"Processing example: {example}")
        response = llm.get_signal(example)
        print(response)


"""

{   Processing example: Bitcoin ETF ads spotted on China's Alipay payment app
    'btc_signal': 1,
    'eth_signal': 0,
    'reasoning': "The news of Bitcoin ETF ads being spotted on China's Alipay payment app
    suggests a growing interest in Bitcoin and other cryptocurrencies among Chinese investors.
    This could lead to increased demand for BTC, causing its price to rise."
}


{   Processing example: U.S. Supreme Court Lets Nvidia's Crypto Lawsuit Move Forward
    'btc_signal': -1,
    'eth_signal': 0,
    'reasoning': "The US Supreme Court's decision allows Nvidia to pursue its crypto lawsuit,
    which may lead to increased regulatory uncertainty and potential restrictions on cryptocurrency
    mining. This could negatively impact Bitcoin prices as investors become more cautious about the
    long-term prospects of cryptocurrencies. Ethereum, being a more established platform with a wider
    range of use cases, is less likely to be directly affected by this development."
}

{   Processing example: Trump's World Liberty Acquires ETH, LINK, and AAVE in $12M Crypto Shopping Spree
    'btc_signal': 0,
    'eth_signal': 1,
    'reasoning': "The acquisition of ETH by a major company like Trump's World Liberty suggests that there
    is increased demand for Ethereum, which could lead to an increase in its price."
}




"""
