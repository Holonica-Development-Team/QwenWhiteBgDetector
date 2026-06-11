"""
QwenWhiteBgDetector
===================
Qwen multi-angle ワークフロー向け 白背景自動検出ノード。

入力画像の四辺ピクセルをサンプリングし、白背景かどうかを判定。
・白背景の場合 → white_bg_prompt (例: ", white background, simple white background")
・背景ありの場合 → color_bg_prompt (デフォルト: "" 空欄でAIが自然に推論)

インストール方法:
  このフォルダごと ComfyUI/custom_nodes/ に配置して ComfyUI を再起動。
"""

import torch


class QwenWhiteBgDetector:
    """
    白背景検出ノード。
    入力画像の四辺エッジをサンプリングし、
    白背景かどうかに応じた背景プロンプトテキストを出力する。
    """

    CATEGORY = "Qwen MultiAngle"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("bg_prompt", "detected_type")
    FUNCTION = "detect"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                # ---- 白背景と判定されたときのプロンプト ----
                "white_bg_prompt": (
                    "STRING",
                    {
                        "default": ", white background, simple white background",
                        "multiline": False,
                    },
                ),
                # ---- 背景ありと判定されたときのプロンプト ----
                # 空欄 = AIが自然に背景を推論 (通常はこれで OK)
                "color_bg_prompt": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                    },
                ),
                # ---- チューニングパラメータ ----
                # エッジの何%が白ければ「白背景」とみなすか (0~1)
                "white_ratio_required": (
                    "FLOAT",
                    {"default": 0.70, "min": 0.10, "max": 1.00, "step": 0.01},
                ),
                # 各チャンネルがこの値以上なら「白ピクセル」とみなす (0~1)
                "pixel_white_threshold": (
                    "FLOAT",
                    {"default": 0.90, "min": 0.50, "max": 1.00, "step": 0.01},
                ),
                # 四辺のうち何割をサンプリングするか (幅/高さに対する比率)
                "edge_sample_ratio": (
                    "FLOAT",
                    {"default": 0.08, "min": 0.01, "max": 0.30, "step": 0.01},
                ),
            }
        }

    def detect(
        self,
        image,
        white_bg_prompt,
        color_bg_prompt,
        white_ratio_required,
        pixel_white_threshold,
        edge_sample_ratio,
    ):
        """
        image: Tensor shape (batch, H, W, C), 値域 [0, 1]
        """
        img = image[0]          # バッチ先頭の1枚を使用
        H, W, C = img.shape

        # ---- 四辺をスライスしてピクセルを収集 ----
        edge_px = max(1, int(min(H, W) * edge_sample_ratio))

        top    = img[:edge_px,    :,        :].reshape(-1, C)
        bottom = img[H - edge_px:, :,       :].reshape(-1, C)
        left   = img[:,           :edge_px, :].reshape(-1, C)
        right  = img[:,    W - edge_px:,    :].reshape(-1, C)

        edge_pixels = torch.cat([top, bottom, left, right], dim=0)  # (N, C)

        # ---- 白ピクセル判定: RGB3チャンネルすべてが閾値以上 ----
        rgb = edge_pixels[:, :3]                          # alpha は無視
        is_white   = rgb.min(dim=1).values >= pixel_white_threshold
        white_ratio = is_white.float().mean().item()

        # ---- 判定 ----
        if white_ratio >= white_ratio_required:
            detected = f"white background (edge white ratio: {white_ratio:.0%})"
            return (white_bg_prompt, detected)
        else:
            detected = f"colored/complex background (edge white ratio: {white_ratio:.0%})"
            return (color_bg_prompt, detected)


# ---- ComfyUI へのノード登録 ----
NODE_CLASS_MAPPINGS = {
    "QwenWhiteBgDetector": QwenWhiteBgDetector,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "QwenWhiteBgDetector": "🎨 White BG Detector (Qwen MultiAngle)",
}
