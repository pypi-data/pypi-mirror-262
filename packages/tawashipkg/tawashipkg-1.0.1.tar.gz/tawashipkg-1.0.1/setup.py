from setuptools import setup, find_packages

setup(
    name='tawashipkg',  # パッケージの名前
    version='1.0.1',  #バージョニング。アップロードしなおすときは必ず数字を増やす
    packages=find_packages(),  # このパッケージに含めるpythonパッケージ名リスト。workspace内全てのパッケージを列挙する関数
    # 作者情報
    author='Tawashi',
    ## author_email='@mail',
    
    # 短い説明文と長い説明文を用意
    # context_typeは下記のいずれか
    # text/plain, text/x-rst, text/markdown
    description='This is a test package for youtube lecture.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    
    # Pythonバージョンは3.6以上で4未満
    python_requires='~=3.6',
    
    # PyPI上での検索、閲覧のために利用される
    # ライセンス、Pythonバージョン、OSを含めること
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
    
    # 依存パッケージの指定
    install_requires = [    
        # Clickのバージョンは7.0以上8未満
        'Click~=7.0'
    ],
    extras_require = {
        
    },
    
    # .py以外の設定ファイルや画像を含ませる変数
    package_data={'tawashipkg': ['data/*']},
)