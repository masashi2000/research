from typing import Any, Dict, Iterator, List, Optional
import pandas as pd
import csv
import requests
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings

class Ollama4Team(Ollama):
    """Ollama4Team is designed for team usage of Ollama.
    Ref: https://github.com/langchain-ai/langchain/blob/cccc8fbe2fe59bde0846875f67aa046aeb1105a3/libs/community/langchain_community/llms/ollama.py

    Example:

        .. code-block:: python

            model = Ollama4Team(api_key="", model="llama2:13b")
            result = model.invoke([HumanMessage(content="hello")])
    """

    """The default parameters for the Ollama API."""
    password: str
    base_url: str = "http://localhost:3000"

    def _create_stream(
        self,
        api_url: str,
        payload: Any,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Iterator[str]:
        if self.stop is not None and stop is not None:
            raise ValueError("`stop` found in both the input and default params.")
        elif self.stop is not None:
            stop = self.stop

        params = self._default_params

        for key in self._default_params:
            if key in kwargs:
                params[key] = kwargs[key]

        if "options" in kwargs:
            params["options"] = kwargs["options"]
        else:
            params["options"] = {
                **params["options"],
                "stop": stop,
                **{k: v for k, v in kwargs.items() if k not in self._default_params},
            }

        if payload.get("messages"):
            request_payload = {"messages": payload.get("messages", []), **params}
        else:
            request_payload = {
                "prompt": payload.get("prompt"),
                "images": payload.get("images", []),
                **params,
            }

        response = requests.post(
            url=api_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {self.password}",
                **(self.headers if isinstance(self.headers, dict) else {}),
            },
            json=request_payload,
            stream=True,
            timeout=self.timeout,
        )
        response.encoding = "utf-8"
        if response.status_code != 200:
            if response.status_code == 404:
                raise self.OllamaEndpointNotFoundError(
                    "Ollama call failed with status code 404. "
                    "Maybe your model is not found "
                    f"and you should pull the model with `ollama pull {self.model}`."
                )
            else:
                optional_detail = response.text
                raise ValueError(
                    f"Ollama call failed with status code {response.status_code}."
                    f" Details: {optional_detail}"
                )
        return response.iter_lines(decode_unicode=True)

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying parameters."""
        return {
            # The model name allows users to specify custom token counting
            # rules in LLM monitoring applications (e.g., in LangSmith users
            # can provide per token pricing for their model and monitor
            # costs for the given LLM.)
            "model_name": self.model,
        }

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model. Used for logging purposes only."""
        return "Ollama4Team"

class Ollama4TeamEmbeddings(OllamaEmbeddings):
    password: str
    base_url: str = "http://localhost:3000"
    def _process_emb_response(self, input: str) -> List[float]:
        """Process a response from the API.

        Args:
            response: The response from the API.

        Returns:
            The response as a dictionary.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.password}",
            **(self.headers or {}),
        }

        try:
            res = requests.post(
                f"{self.base_url}/api/embeddings",
                headers=headers,
                json={"model": self.model, "prompt": input, **self._default_params},
            )
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error raised by inference endpoint: {e}")

        if res.status_code != 200:
            raise ValueError(
                "Error raised by inference API HTTP code: %s, %s"
                % (res.status_code, res.text)
            )
        try:
            t = res.json()
            return t["embedding"]
        except requests.exceptions.JSONDecodeError as e:
            raise ValueError(
                f"Error raised by inference API: {e}.\nResponse: {res.text}"
            )


def hit_api_with_2250_prompts_10_times(csv_file_path):
    model_name = input("Model name? >>")
    llm = Ollama4Team(model=model_name, password="ollamasakurai", base_url="http://100.80.132.15:3000")
    model_name = model_name.replace(":", "-")


    # CSVファイルを読み込む
    df = pd.read_csv(csv_file_path)

    # 各周回の結果を保存するためのファイル名のリスト
    result_files = [f'result{i}_{model_name}.csv' for i in range(1, 11)]

    # ヘッダーを書き込む
    for result_file in result_files:
        with open(result_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # 元のデータフレームのカラム名に 'result' を追加
            result_columns = df.columns.tolist() + ['result'] + ['model_name']
            writer.writerow(result_columns)

    # 10周実行
    for attempt in range(10):
        for index, row in df.iterrows():
            prompt = row['prompt']

            # llm.invoke()を呼び出し
            result = llm.invoke(prompt)
            
            # 現在の行データをリストに変換し、結果を格納
            row_data = row.tolist() + [result] + [model_name]
            
            # 該当するresultファイルに書き込む
            with open(result_files[attempt], mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(row_data)

    print(f"Results have been saved to result1.csv through result10.csv")


def main():
    hit_api_with_2250_prompts_10_times()

if __name__ == "__main__":
    main()
