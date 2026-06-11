# QwenWhiteBgDetector

Qwen multi-angle ワークフロー向けの **白背景自動検出** ComfyUI カスタムノード。

入力画像の四辺（エッジ）ピクセルをサンプリングし、白背景かどうかを判定して、
判定結果に応じた背景プロンプト文字列を出力します。

- 白背景と判定 → `white_bg_prompt`（例: `, white background, simple white background`）
- 背景ありと判定 → `color_bg_prompt`（デフォルト空欄。空欄なら AI が自然に背景を推論）

## ノード

| 項目 | 値 |
| --- | --- |
| 表示名 | 🎨 White BG Detector (Qwen MultiAngle) |
| 内部名 | `QwenWhiteBgDetector` |
| カテゴリ | `Qwen MultiAngle` |
| 出力 | `bg_prompt` (STRING), `detected_type` (STRING) |

### 入力

| 名前 | 型 | デフォルト | 説明 |
| --- | --- | --- | --- |
| `image` | IMAGE | – | 判定対象の画像 |
| `white_bg_prompt` | STRING | `, white background, simple white background` | 白背景時に出力するプロンプト |
| `color_bg_prompt` | STRING | `` (空欄) | 背景あり時に出力するプロンプト |
| `white_ratio_required` | FLOAT | `0.70` | エッジの何割が白なら「白背景」とみなすか (0–1) |
| `pixel_white_threshold` | FLOAT | `0.90` | 各チャンネルがこの値以上なら「白ピクセル」とみなす (0–1) |
| `edge_sample_ratio` | FLOAT | `0.08` | 四辺のサンプリング幅（幅/高さに対する比率） |

## インストール

このリポジトリを `ComfyUI/custom_nodes/` 配下にクローンして ComfyUI を再起動してください。

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/Holonica-Development-Team/QwenWhiteBgDetector.git
```

依存ライブラリは ComfyUI に同梱の `torch` のみで、追加インストールは不要です。
