import json

def generate_big5_markers_json():
    data = {
            "LOW_EXT" : ["unfriendly", "introverted", "silent", "timid", "unassertive", "inactive", "unenergetic", "unadventurous", "gloomy"],
            "HIGH_EXT": ["friendly", "extroverted", "talkative", "bold", "assertive", "active", "energetic", "adventurous and daring", "cheerful"],
            "LOW_AGR" : ["distrustful", "immoral", "dishonest", "unkind", "stingy", "unaltruistic", "uncooperative", "self-important", "unsympathetic", "selfish", "disagreeable"],
            "HIGH_AGR": ["trustful", "moral", "honest", "kind", "generous", "altruistic", "cooperative", "humble", "sympathetic", "unselfish", "agreeable"],
            "LOW_CON" : ["unsure", "messy", "irresponsible", "lazy", "undisciplined", "impractical", "extravagant", "disorganized", "negligent", "careless"],
            "HIGH_CON": ["self-efficacious", "orderly", "responsible", "hardworking", "self-disciplined", "practical", "thrifty", "organized", "conscientious","thorough"],
            "LOW_NEU" : ["relaxed", "at ease", "easygoing", "calm", "patient", "happy", "unselfconscious", "level-headed", "contented", "emotionally stable"],
            "HIGH_NEU": ["tense", "nervous", "anxious", "angry", "irritable", "depressed", "self-conscious", "impulsive", "discontented", "emotionally unstable"],
            "LOW_OPE" : ["unimaginative", "uncreative", "artistically unappreciative", "unaesthetic", "unreflective", "emotionally closed", "uninquisitive", "predictable", "unintelligent", "unanalytical", "unsophisticated", "socially conservative"],
            "HIGH_OPE": ["imaginative", "creative", "artistically appreciative", "aesthetic", "reflective", "emotionally aware", "curious", "spontaneous", "intelligent", "analytical", "sophisticated", "socially progressive"]
    }
    # JSONファイルに保存
    with open("big5_markers.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

            print("データがbig5_markers.jsonに保存されました。")

def main():
    generate_big5_markers_json()

if __name__ == "__main__":
    main()
