import pandas as ps
import json

def generate_2250_prompts():    
    ## マーカーデータの読み込み

    # JSONファイルのパスを指定します
    file_path = 'big5_markers.json'

    # JSONファイルを読み込みます
    with open(file_path, 'r', encoding='utf-8') as file:
            markers = json.load(file)

            # 読み込んだデータを表示します
            print(markers)
    
    # 読み込んだデータを表示します
    print(markers)


    ## ペルソナファイルの読み込み

    # CSVファイルのパスを指定します
    file_path = 'personas.csv'

    # CSVファイルを読み込みます
    df_personas = pd.read_csv(file_path)

    # データフレームの内容を表示します
    print(df_personas)


    ## 2250個のプロンプトを保存するデータフレーム
    df = pd.DataFrame(columns=['domain', 'level', 'persona_id', 'prompt'])

    for domain in ["EXT", "AGR", "CON", "NEU", "OPE"]:
        # リスト型の修飾子を作る
        qualifiers = ["extremely ", "very ", "", "a bit "] 


        # HIGHレベルの時
        for row in df_personas.itertuples():
            level = 9
            for qualifier in qualifiers:
                prompt = """For the following task, respond in a way that matches this description: "{} I'm """.format(row.persona)
                for i in range(0, len(markers["HIGH_{}".format(domain)])-1):
                    prompt += "{}".format(qualifier)
                    prompt += "{}".format(markers["HIGH_{}".format(domain)][i])
                    prompt += ", "
                prompt += "and {}{}.".format(qualifier, markers["HIGH_{}".format(domain)][-1]) # 最後はandを入れないとだめだから
                prompt += " Generate a list of 20 different Facebook status updates as this person. Each update must be verbose and reflect the person’s character and description. The updates should cover, but should not be limited to, the following topics: work, family, friends, free time, romantic life, TV / music / media consumption, and communication with others."
                df = df.append({'persona_id': row.id, 'domain': domain, 'level': level, 'prompt': prompt }, ignore_index=True)
                level -= 1

        ## qualifierが neither nor の時は特例でやる
        for row in df_personas.itertuples():
            level = 5
            prompt = """For the following task, respond in a way that matches this description: "{} I'm """.format(row.persona)
            for i in range(0, len(markers["LOW_{}".format(domain)])-1):
                prompt += "neither {} nor {}".format(markers["LOW_{}".format(domain)][i], markers["HIGH_{}".format(domain)][i])
                prompt += ", "
            prompt += "and neither {} nor {}.".format(markers["LOW_{}".format(domain)][-1], markers["HIGH_{}".format(domain)][-1]) # 最後はandを入れないとだめだから
            prompt += " Generate a list of 20 different Facebook status updates as this person. Each update must be verbose and reflect the person’s character and description. The updates should cover, but should not be limited to, the following topics: work, family, friends, free time, romantic life, TV / music / media consumption, and communication with others."
            df = df.append({'persona_id': row.id, 'domain': domain, 'level': level, 'prompt': prompt }, ignore_index=True)

    # ファイルとして出力
    df = df.sort_values(by=['domain', 'level', 'persona_id', 'prompt'])
    df.insert(0, 'id', range(1, len(df) + 1))
    df.to_csv('2250_prompts.csv', index=False, encoding='utf-8-sig')


def main():
     generate_2250_prompts()


if __name__ == "__main__":
     main()