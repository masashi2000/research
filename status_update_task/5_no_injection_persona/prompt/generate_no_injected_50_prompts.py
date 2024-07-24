import pandas as pd
import json


def generate_2250_prompts():    

    ## ペルソナファイルの読み込み

    # CSVファイルのパスを指定します
    file_path = 'personas.csv'

    # CSVファイルを読み込みます
    df = pd.read_csv(file_path)

    # データフレームの内容を表示します
    print(df)


    # 'persona'列の各レコードの先頭に "A:" を追加
    df['persona'] = 'For the following task, respond in a way that matches this description: "' + df['persona'] + '"' + " Generate a list of 20 different Facebook status updates as this person. Each update must be verbose and reflect the person’s character and description. The updates should cover, but should not be limited to, the following topics: work, family, friends, free time, romantic life, TV / music / media consumption, and communication with others."

    # 修正されたデータフレームを新しいCSVファイルとして保存
    output_path = 'persona_50_prompts_without_injection.csv'  # 保存先のパスに置き換えてください
    df.to_csv(output_path, index=False)

    print("修正されたCSVファイルが保存されました:", output_path)



def main():
     generate_2250_prompts()


if __name__ == "__main__":
     main()
