import setuptools #導入setuptools打包工具
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="example-pkg-CSSA", # 用自己的名替換其中的YOUR_USERNAME_
    version="0.1.3",    #包版本號，便於維護版本
    author="Example Author",    #作者，可以寫自己的姓名
    author_email="ladder.cssa@gmail.com",    #作者聯系方式，可寫自己的郵箱地址
    description="A small example package",#包的簡述
    long_description=long_description,    #包的詳細介紹，一般在README.md文件內
    long_description_content_type="text/markdown",
    url="https://github.com/LadderCSSA/NOMTrainer",    #自己項目地址，比如github的項目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',    #對python的最低版本要求
)
