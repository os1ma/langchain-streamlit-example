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

文書をベクトル化してローカルに保存

```console
python create_index.py
```

アプリケーションの起動

```console
streamlit run app.py
```

例えば以下のプロンプトで動作確認できます。

```
langchain-streamlit-example は何を import していますか？
```
