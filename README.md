# langchain-streamlit-example

## 実行手順

.env ファイルを以下の内容で作成

```
OPENAI_API_KEY=<your-openai-api-key>
```

Python のインストール

```console
pyenv local 3.10
```

Python の仮想環境の作成と有効化

```console
python -m venv .venv
. .venv/bin/activate
```

パッケージのインストール

```console
pip install -r requirements.txt
```

アプリケーションの起動

```console
streamlit run app.py
```
