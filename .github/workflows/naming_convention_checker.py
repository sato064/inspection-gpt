import re
from spellchecker import SpellChecker
import os
import subprocess
spell = SpellChecker()
#キャメルケースになっているかチェックする場合
def is_cammelcase(target_string):
    #まずスネークケースになっていないかチェック
    if "_" in target_string:
        # print(target_string + " ← アンダーバーが含まれています，スネークケースになっていませんか？")
        return False
    #次に最初の文字が大文字になっていないかチェック
    elif target_string[0].isupper():
        # print(target_string + " ← 先頭の文字が大文字になっています")
        return False
    #最後に，大文字で正しく単語が区切られているかチェック
    else:
        splited_list = re.split('(?=[A-Z])', target_string)
        misspelled = spell.unknown(splited_list)
        if len(misspelled) > 0:
            # print(target_string + " ← キャメルケースになっていますが，単語が正しく区切られていないか，スペルミスがあります")
            return False
        else:
            # print("正常なキャメルケースになっています")
            return True

def is_pascalcase(target_string):
    #まずスネークケースになっていないかチェック
    if "_" in target_string:
        # print(target_string + " ← アンダーバーが含まれています，スネークケースになっていませんか？")
        return False
    #次に最初の文字が大文字になっていないかチェック
    elif not target_string[0].isupper():
        # print(target_string + " ← 先頭の文字が小文字になっています")
        return False
    #最後に，大文字で正しく単語が区切られているかチェック
    else:
        splited_list = re.split('(?=[A-Z])', target_string)
        splited_list.remove("")
        # print(splited_list)
        misspelled = spell.unknown(splited_list)
        if len(misspelled) > 0:
            # print(target_string + " ← パスカルケースになっていますが，単語が正しく区切られていないか，スペルミスがあります")
            return False
        else:
            # print("正常なパスカルケースになっています")
            return True
        
#test start
# is_cammelcase("snake_case")
# is_cammelcase("UpperCamelCase")
# is_cammelcase("lowerCamelCasse")
# is_cammelcase("lowerCamelId")
# is_pascalcase("Book")
print(os.environ['PR_NUMBER'])

with open('docs/class_diagram_template.md') as f:
    num = 0
    field_flag = False
    for line in f:
        num += 1
        if line.startswith("###"):
            # print(line[4:][:-1])
            if not is_pascalcase(line[4:][:-1]):
                print(str(num) +"行目の " + line[4:][:-1] +" がパスカルケースになっていません")
                subprocess.call('gh pr comment ${{ github.event.number }} --body "' + str(num) +"行目のクラス名 " + line[4:][:-1] +' がパスカルケースになっていません"')
        if not line.startswith("|") and field_flag:
            field_flag = False
        if line.startswith("|フィールド名"):
            field_flag = True
        if  line.startswith("|:"):
            continue
        if line.startswith("|") and not line.startswith("|フィールド名") and field_flag:
            if not is_cammelcase(line[1:].split('|')[0]):
                print(str(num) +"行目の " + line[1:].split('|')[0] +" がキャメルケースになっていません")
                subprocess.call('gh pr comment ${{ github.event.number }} --body "' + str(num) +"行目のフィールド名 " + line[1:].split('|')[0] +' がキャメルケースになっていません"')