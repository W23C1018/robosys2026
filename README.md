# resistor

![test](https://github.com/W23C1018/robosys2026/actions/workflows/test.yml/badge.svg)

標準入力から受け取った抵抗のカラーコードと抵抗値（Ω）を相互変換するコマンドラインツールです。
電子工作やロボット製作における部品選定・回路確認を端末上で素早く行うために作成しました。

## 機能

* **カラーコード → 抵抗値変換**: 4本帯・5本帯のカラーコード（日本語・英語・略称に対応）から抵抗値と許容差を算出します。
* **抵抗値 → カラーコード変換**: 数値（k, M, G の接頭辞および Ω 付き表記に対応）から4本帯カラーコード（±5% 金）を算出します。
* **ストリーム処理**: 複数行の連続入力や他のコマンドとのパイプ接続に対応しています。

## インストール方法

```bash
git clone https://github.com/W23C1018/robosys2026.git
cd robosys2026
chmod +x resistor
```

## 使い方

### 1. カラーコードから抵抗値を求める

```bash
$ echo "赤 紫 茶 金" | ./resistor
270 Ω (±5%)

$ echo "yellow violet red gold" | ./resistor
4.7 kΩ (±5%)

$ echo "茶 黒 黒 赤 茶" | ./resistor
10 kΩ (±1%)
```

### 2. 抵抗値からカラーコードを求める

```bash
$ echo "4.7k" | ./resistor
黄 紫 赤 金

$ echo "1M" | ./resistor
茶 黒 緑 金
```

### 3. 複数行をまとめて変換する

```bash
$ printf "茶 黒 赤 金\n330\n" | ./resistor
1 kΩ (±5%)
橙 橙 茶 金
```

## テストの実行

```bash
./test.bash
```

## 動作環境

* Ubuntu 24.04 LTS
* Python 3.12（標準ライブラリのみで動作）

## ライセンス

* このソフトウェアパッケージは，3条項BSDライセンスの下，再頒布および使用が許可されます．
* © 2026 Shuusuke Inomata
