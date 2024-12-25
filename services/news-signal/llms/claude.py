from typing import Literal, Optional
from llama_index.core.prompts import PromptTemplate

from llama_index.llms.anthropic import Anthropic
from .base import BaseNewsSignalExtractor, NewsSignal


class ClaudeNewsSignalExtractor(BaseNewsSignalExtractor):
    def __init__(
        self,
        model_name: str,
        api_key: str,
        temperature: Optional[float] = 0,
    ):
        self.llm = Anthropic(
            model=model_name,
            api_key=api_key,
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
    ) -> NewsSignal | dict:
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
    from .config import AnthropicConfig

    config = AnthropicConfig()

    llm = ClaudeNewsSignalExtractor(
        model_name=config.model_name,
        api_key=config.api_key,
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
    'reasoning': "The appearance of Bitcoin ETF advertisements on Alipay, a major Chinese payment platform,
    is bullish for BTC for several reasons: 1) It represents potential warming of crypto sentiment in China,
    which has historically been restrictive,
    2) It exposes Bitcoin ETFs to a massive potential investor base in China,
    3) It suggests possible institutional acceptance in the Chinese market. The news is specific to Bitcoin ETFs
    and doesn't have direct implications for Ethereum, hence the neutral signal for ETH."

    "btc_signal":1,
    "eth_signal":0,
    "reasoning":"The appearance of Bitcoin ETF advertisements on Alipay, a major Chinese payment platform,
    is bullish for BTC prices for several reasons: 1) It suggests potential increasing acceptance of Bitcoin
    investment products in China, a market that has been historically restricted,
    2) It could lead to increased awareness and potential demand from Chinese investors,
    3) Any softening of crypto stance in China typically has significant market impact due to the country's
    large investor base. The signal is positive (1) for BTC specifically since the news only mentions Bitcoin ETFs.
    The impact on ETH is neutral (0) as the news doesn't directly relate to Ethereum or its ecosystem."

    "btc_signal":1,
    "eth_signal":0,
    "reasoning":"The appearance of Bitcoin ETF advertisements on Alipay, a major Chinese payment platform,
    is bullish for BTC prices for several reasons: 1) It suggests potential increasing acceptance of Bitcoin
    investment products in China, a market that has been historically restricted,
    2) It could lead to increased awareness and potential demand from Chinese investors,
    3) Any softening of crypto stance in China typically has significant market impact due to the country's
    large investor base. The signal is positive (1) for BTC specifically since the news only mentions Bitcoin ETFs.
    The impact on ETH is neutral (0) as the news doesn't directly relate to Ethereum or its ecosystem."

    }


{   Processing example: U.S. Supreme Court Lets Nvidia's Crypto Lawsuit Move Forward
    'btc_signal': 0,
    'eth_signal': -1,
    'reasoning': "The Supreme Court allowing Nvidia's crypto lawsuit to proceed has neutral impact on Bitcoin
    as it doesn't affect its current ASIC-based mining ecosystem. However, it has a slightly negative impact
    on Ethereum and the broader GPU-mining ecosystem as it might make GPU manufacturers more cautious about serving
    the crypto market and could create negative sentiment around crypto-related businesses. The lawsuit focuses on
    Nvidia's disclosure practices during the 2017-2018 crypto boom and while historical in nature, could affect future
    hardware availability and business relationships in the GPU-crypto space."

    "btc_signal":0,
    "eth_signal":0,
    "reasoning":"The Supreme Court's decision to allow a lawsuit against Nvidia to proceed is primarily a corporate
    governance issue related to Nvidia's disclosure practices during the 2017-2018 crypto boom. This legal
    development has no direct impact on cryptocurrency fundamentals or operations. While it involves the crypto
    mining industry historically, it's a backward-looking legal matter that doesn't affect current crypto market
    dynamics or future prospects for either Bitcoin or Ethereum. Therefore, the news is expected to have neutral
    impact on both BTC and ETH prices."

    "btc_signal":0,
    "eth_signal":0,
    reasoning":"The Supreme Court's decision to allow a lawsuit against Nvidia to proceed is primarily a corporate
    legal matter concerning Nvidia's past disclosures about crypto mining revenue. This news doesn't directly impact
    cryptocurrency operations, regulations, or adoption. While Nvidia was a significant player in crypto mining hardware,
    this legal case focuses on historical disclosure practices rather than current or future crypto mining capabilities.
    Therefore, the news is unlikely to have any significant impact on either BTC or ETH prices."


}

{   Processing example: Trump's World Liberty Acquires ETH, LINK, and AAVE in $12M Crypto Shopping Spree
    'btc_signal': 0,
    'eth_signal': 1,
    'reasoning': 'The news indicates a significant $12M institutional investment directly into ETH and Ethereum ecosystem
    tokens (LINK, AAVE), which is bullish for ETH as it represents strong institutional interest and buying pressure.
    However, BTC was notably absent from the purchase list, suggesting a neutral impact on Bitcoin prices.
    While institutional crypto investment can generally benefit the whole crypto market, the specific focus on
    ETH ecosystem tokens rather than BTC suggests no direct price impact on Bitcoin.'

    "btc_signal":0,
    "eth_signal":1,
    "reasoning":"The news indicates a significant $12M institutional investment specifically in ETH and Ethereum ecosystem
    tokens (LINK, AAVE), which is directly positive for ETH price as it represents strong institutional interest and buying pressure.
    For BTC, while institutional crypto investment is generally positive for the whole market, this news specifically
    bypasses Bitcoin in favor of Ethereum ecosystem tokens, suggesting a neutral impact on BTC price."

}




"""
