import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

# 惑星データ（画像ファイル名「local_img」を指定）
PLANET_DATA = {
    "水星 (Mercury)": {
        "period": "約88日",
        "distance": "0.39 AU (約5800万 km)",
        "size": "地球の約0.38倍",
        "feature": "太陽に最も近い惑星。昼夜の温度差が激しく、大気がほとんどありません。",
        "local_img": "mercury.png"
    },
    "金星 (Venus)": {
        "period": "約225日",
        "distance": "0.72 AU (約1億8000万 km)",
        "size": "地球の約0.95倍",
        "feature": "厚い二酸化炭素の大気に覆われており、強い温室効果で表面温度は400℃を超えます。",
        "local_img": "venus.png"
    },
    "地球 (Earth)": {
        "period": "365.26日 (1年)",
        "distance": "1.00 AU (約1億5000万 km)",
        "size": "基準 (直径約12,742 km)",
        "feature": "私たちが暮らす惑星。豊かな水と大気があり、多様な生命が存在します。",
        "local_img": "earth.png"
    },
    "火星 (Mars)": {
        "period": "約687日 (約1.9年)",
        "distance": "1.52 AU (約2億2800万 km)",
        "size": "地球の約0.53倍",
        "feature": "「赤い惑星」と呼ばれます。かつて水が存在した跡があり、探査が盛んです。",
        "local_img": "mars.png"
    },
    "木星 (Jupiter)": {
        "period": "約12年",
        "distance": "5.20 AU (約7億7800万 km)",
        "size": "地球の約11倍",
        "feature": "太陽系最大のガス惑星。大赤斑と呼ばれる巨大な嵐の渦があります。",
        "local_img": "jupiter.png"
    },
    "土星 (Saturn)": {
        "period": "約29.5年",
        "distance": "9.58 AU (約14億3000万 km)",
        "size": "地球の約9.4倍",
        "feature": "美しく巨大な「環（リング）」を持つガス惑星。水に浮くほど平均密度が低いです。",
        "local_img": "saturn.png"
    },
    "天王星 (Uranus)": {
        "period": "約84年",
        "distance": "19.22 AU (約28億7000万 km)",
        "size": "地球の約4.0倍",
        "feature": "自転軸が横倒し（約98度傾いている）になっている、青緑色の氷惑星です。",
        "local_img": "uranus.png"
    },
    "海王星 (Neptune)": {
        "period": "約165年",
        "distance": "30.05 AU (約45億 km)",
        "size": "地球の約3.9倍",
        "feature": "太陽から最も遠い惑星。強い風が吹き荒れており、美しい深い青色をしています。",
        "local_img": "neptune.png"
    }
}

class AdvancedPlanetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("太陽系惑星ビジュアルガイド")
        self.root.geometry("800x550")
        self.root.configure(bg="#080C14")

        # タイトル
        title_label = tk.Label(
            root, text="太陽系惑星ビジュアルガイド", 
            font=("Helvetica", 20, "bold"), fg="#FFFFFF", bg="#080C14"
        )
        title_label.pack(pady=15)

        # メインフレーム
        main_frame = tk.Frame(root, bg="#080C14")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 左側：ボタン
        btn_frame = tk.Frame(main_frame, bg="#080C14")
        btn_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # 右側：情報（左右分割）
        self.info_frame = tk.LabelFrame(
            main_frame, text="惑星を選択してください", 
            font=("Helvetica", 14, "bold"), fg="#00FFCC", bg="#111827",
            bd=2, relief=tk.GROOVE, padx=15, pady=15
        )
        self.info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # テキスト情報用のサブフレーム
        text_sub_frame = tk.Frame(self.info_frame, bg="#111827")
        text_sub_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 画像表示用のラベル
        self.img_label = tk.Label(self.info_frame, bg="#111827")
        self.img_label.pack(side=tk.RIGHT, padx=10, anchor="center")

        # 各種ステータス変数
        self.period_var = tk.StringVar(value="-")
        self.dist_var = tk.StringVar(value="-")
        self.size_var = tk.StringVar(value="-")
        self.feat_var = tk.StringVar(value="-")

        # ラベル配置
        labels_config = [
            ("【公転周期】", self.period_var),
            ("【太陽からの距離】", self.dist_var),
            ("【大きさ】", self.size_var),
        ]

        for title, var in labels_config:
            tk.Label(text_sub_frame, text=title, fg="#A0AABF", bg="#111827", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(5, 2))
            tk.Label(text_sub_frame, textvariable=var, fg="#FFFFFF", bg="#111827", font=("Helvetica", 12)).pack(anchor="w", pady=(0, 10))

        tk.Label(text_sub_frame, text="【主な特徴】", fg="#A0AABF", bg="#111827", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(5, 2))
        self.feat_label = tk.Label(
            text_sub_frame, textvariable=self.feat_var, fg="#FFFFFF", bg="#111827", 
            font=("Helvetica", 11), justify=tk.LEFT, wraplength=350
        )
        self.feat_label.pack(anchor="w", pady=5)

        # 画像キャッシュ用辞書
        self.image_cache = {}

        # ボタン生成
        for planet_name in PLANET_DATA.keys():
            btn = tk.Button(
                btn_frame, text=planet_name, width=15,
                font=("Helvetica", 11, "bold"),
                bg="#1F2937", fg="#FFFFFF",
                activebackground="#374151", activeforeground="#00FFCC",
                command=lambda name=planet_name: self.show_planet_info(name)
            )
            btn.pack(pady=5, fill=tk.X)

    def get_planet_image(self, file_name):
        if file_name in self.image_cache:
            return self.image_cache[file_name]

        # プログラムと同じ場所にある「planets」フォルダ内の画像パスを作る
        img_path = os.path.join(os.path.dirname(__file__), "planets", file_name)

        if os.path.exists(img_path):
            try:
                img = Image.open(img_path)
                img = img.resize((220, 220), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.image_cache[file_name] = photo
                return photo
            except Exception as e:
                print(f"画像の読み込みに失敗しました: {e}")
                return None
        else:
            print(f"画像ファイルが見つかりません: {img_path}")
            return None

    def show_planet_info(self, name):
        data = PLANET_DATA[name]
        self.info_frame.config(text=name)
        self.period_var.set(data["period"])
        self.dist_var.set(data["distance"])
        self.size_var.set(data["size"])
        self.feat_var.set(data["feature"])

        # ローカル画像を取得して表示
        photo = self.get_planet_image(data["local_img"])
        if photo:
            self.img_label.config(image=photo, text="")
            self.img_label.image = photo
        else:
            self.img_label.config(image="", text="（画像ファイルなし）", fg="#FFFFFF")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedPlanetApp(root)
    root.mainloop()
