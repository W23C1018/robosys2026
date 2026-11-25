#!/bin/bash -xv
# SPDX-FileCopyrightText: 2026 Shuusuke Inomata
# SPDX-License-Identifier: BSD-3-Clause

ng () {
    echo "${1}行目が違うよ"
    res=1
}

res=0

### 正常系: 日本語カラーコード -> 抵抗値 ###
out=$(echo "赤 紫 茶 金" | ./resistor)
[ "${out}" = "270 Ω (±5%)" ] || ng "$LINENO"

### 正常系: 英語カラーコード -> 抵抗値 ###
out=$(echo "yellow violet red gold" | ./resistor)
[ "${out}" = "4.7 kΩ (±5%)" ] || ng "$LINENO"

### 正常系: 5本帯カラーコード -> 抵抗値 ###
out=$(echo "茶 黒 黒 赤 茶" | ./resistor)
[ "${out}" = "10 kΩ (±1%)" ] || ng "$LINENO"

### 正常系: 抵抗値 -> カラーコード（逆変換） ###
out=$(echo "4.7k" | ./resistor)
[ "${out}" = "黄 紫 赤 金" ] || ng "$LINENO"

out=$(echo "1M" | ./resistor)
[ "${out}" = "茶 黒 緑 金" ] || ng "$LINENO"

### 正常系: 複数行の連続処理 ###
out=$(printf "茶 黒 赤 金\n330\n" | ./resistor)
expected=$(printf "1 kΩ (±5%%)\n橙 橙 茶 金")
[ "${out}" = "${expected}" ] || ng "$LINENO"

### 異常系: 空入力 ###
out=$(echo "" | ./resistor 2>/dev/null)
[ "$?" = 1 ] || ng "$LINENO"
[ "${out}" = "" ] || ng "$LINENO"

### 異常系: 不明な色名 ###
out=$(echo "赤 紫 虹 金" | ./resistor 2>/dev/null)
[ "$?" = 1 ] || ng "$LINENO"
[ "${out}" = "" ] || ng "$LINENO"

### 異常系: 有効数字に無効な色（金） ###
out=$(echo "金 紫 茶 金" | ./resistor 2>/dev/null)
[ "$?" = 1 ] || ng "$LINENO"

### 異常系: 負の値や表現不能な値 ###
out=$(echo "-100" | ./resistor 2>/dev/null)
[ "$?" = 1 ] || ng "$LINENO"

out=$(echo "123" | ./resistor 2>/dev/null)
[ "$?" = 1 ] || ng "$LINENO"

[ "${res}" = 0 ] && echo "OK"
exit "${res}"
