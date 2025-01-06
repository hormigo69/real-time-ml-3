import httpx
from loguru import logger
from typing import Literal, Optional, List, Union

from llama_index.llms.ollama import Ollama
from llama_index.core.prompts import PromptTemplate

from .base import BaseNewsSignalExtractor, NewsSignal


class OllamaNewsSignalExtractor(BaseNewsSignalExtractor):
    def __init__(
        self,
        model_name: str,
        base_url: str,  # añadido al meter ollama_base_url en el config en lugar de hardcoded
        temperature: Optional[float] = 0,
    ):
        # base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        logger.info(f"Inicializando Ollama con URL base: {base_url}")

        self.llm = Ollama(
            model=model_name,
            temperature=temperature,
            request_timeout=60.0,
            base_url=base_url,
            additional_kwargs={
                "num_retries": 3,
                "retry_interval": 1.0,
            },
        )

        self.prompt_template = PromptTemplate(
            template="""
            You are an expert crypto financial analyst with deep knowledge of market dynamics and sentiment analysis.
            Analyze the following news story and determine its potential impact on crypto asset prices.
            Focus on both direct mentions and indirect implications for each asset.

            Do not output data for a given coin if the news is not relevant to it.

            ## Example input
            "Goldman Sachs wants to invest in Bitcoin and Ethereum, but not in XRP"

            ## Example output
            [
                {"coin": "BTC", "signal": 1},
                {"coin": "ETH", "signal": 1},
                {"coin": "XRP", "signal": -1},
            ]

            News story to analyze:
            {news_story}
            """
        )

        self.model_name = model_name

    def get_signal(
        self,
        text: str,
        output_format: Literal["dict", "list", "NewsSignal"] = "NewsSignal",
        max_retries: int = 3,
    ) -> Union[dict, List[dict], NewsSignal]:
        """
        Get the news signal from the given "text"

        Args:
            text (str): The news article to analyze
            output_format (Literal["dict", "list", "NewsSignal"]): The format of the output
            max_retries (int): Maximum number of retries on failure

        Returns:
            Union[dict, List[dict], NewsSignal]: The news signal
        """
        for attempt in range(max_retries):
            try:
                logger.debug(
                    f"Intentando procesar texto (intento {attempt + 1}): {text[:100]}..."
                )

                # logger.info(f"Configuración LLM - Modelo: {self.model_name}, URL base: {self.llm.base_url}")

                # logger.debug("Iniciando llamada a Ollama API...")

                response: NewsSignal = self.llm.structured_predict(
                    NewsSignal,
                    prompt=self.prompt_template,
                    news_story=text,
                )

                # logger.debug("Respuesta recibida exitosamente de Ollama API")

                # keep only news signals with non-zero signal
                response.news_signals = [
                    news_signal
                    for news_signal in response.news_signals
                    if news_signal.signal != 0
                ]

                if output_format == "list":
                    return response.model_dump()["news_signals"]
                else:
                    return response

            except (httpx.ReadTimeout, httpx.ConnectTimeout) as e:
                logger.error(
                    f"Error de timeout - Detalles de conexión:\n"
                    f"URL: {self.llm.base_url}\n"
                    f"Timeout configurado: {self.llm.request_timeout}s\n"
                    f"Error completo: {str(e)}"
                )
                if attempt == max_retries - 1:  # Si es el último intento
                    logger.error(f"Agotados todos los intentos para: {text[:100]}")
                    # Devolver un resultado vacío en lugar de fallar
                    if output_format == "list":
                        return []
                    elif output_format == "dict":
                        return {}
                    else:
                        return NewsSignal(news_signals=[])
                continue

            except Exception as e:
                logger.error(
                    f"Error inesperado al procesar texto. Detalles:\n"
                    f"URL: {self.llm.base_url}\n"
                    f"Modelo: {self.model_name}\n"
                    f"Texto: {text[:100]}...\n"
                    f"Tipo de error: {type(e).__name__}\n"
                    f"Error completo: {str(e)}"
                )
                # Devolver un resultado vacío en lugar de fallar
                if output_format == "list":
                    return []
                elif output_format == "dict":
                    return {}
                else:
                    return NewsSignal(news_signals=[])


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
