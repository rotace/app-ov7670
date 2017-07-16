# app-ov7670
ov7670 camera module driver and software  

* ステップを踏んで開発するため，バージョンごとの目標を記載する．  
* v0.xは参考文献の追試であるが，
linux+pythonで画像表示したいため，
画像表示プログラムはpythonバージョンで作成する．
* ov7670の他のレジスタを容易に操作するため，
レジスタをpython側で指示する．
(この思想は非セキュリティ設計か)
* レジスタ操作のうち高速化の影響の薄い部分は可読性重視のプログラムに改良する．(I2C通信など)
* ROSの勉強も兼ねて，ov7670のROSドライバを作成する．
* 余裕あれば，nanoバージョンも作成する．

### v0.0
* モノクロ，QVGAによる画像送信  [参考文献](http://qiita.com/hi631/items/d85cf031ecadf397b8e1)
* シリアル受信及び画像表示  [参考文献](http://qiita.com/hi631/items/94fa041a13714377332f)

### v0.1
* カラー,速度Up  [参考文献](http://qiita.com/hi631/items/0170a531457e717f3606#_reference-aa3059f01c9f6da2085b)

### v0.2
* VGA,QQVGA対応  [参考文献](http://qiita.com/hi631/items/c08798e4091bc570d8d2#_reference-d530237dd7401640b2b1)

### v1.0
* レジスタ操作をpython側で指示するよう変更
* 可読性重視のプログラムへ改良

### v1.1
* ROS向けデバイスドライバの作成
