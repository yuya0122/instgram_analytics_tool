# instgram_analytics_tool
instagram graph apiから情報を取得してgoogle spread sheetに結果を出力するツール

# 事前準備
### スプレッドシートの設定
1.  下記リンクを参考に、結果出力用のスプレッドシートの作成とservice accountの認証鍵（jsonファイル）の取得を行う。
    >https://amg-solution.jp/blog/26703
2. 1にて取得した認証鍵をsecretフォルダ直下に配置する(ファイル名のリネームは可能)
3. 2にて作成したスプレッドシートの名前と認証鍵の名前をconfig.iniに記載する。

### インスタグラムの設定
1. 下記リンクを参考にビジネスアカウントIDとアクセストークンの取得を行う
    >https://www.teijitaisya.com/instagram-graph-api/
2. 1にて取得したビズネスアカウントIDとアクセストークンと分析対象のユーザー名をconfig.iniに記載する。

### PC設定
1. python3.9をダウンロード
2. 仮想環境の作成。instagram_analytics_toolに移動し下記コマンドを実行する
    >python3 -m venv .venv
3. 仮想環境の有効化。下記コマンドを実行
    >macの場合(bash): source .venv/bin/activate  
    >windowsの場合(cmdprompt): .venv¥Scripts¥activate.bat
4. ライブラリのインストール
    >pip install -r requirements.txt

# ツール実行方法
仮想環境が有効となっている状態で下記コマンドを実行する
>python3 command.py --task_name insta_to_spread





