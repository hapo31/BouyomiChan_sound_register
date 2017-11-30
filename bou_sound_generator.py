import sys
import os


class BouyomiDicRecord():
    def __init__(self, priority, lang, word, tag):
        # 優先度
        if isinstance(priority, str):
            self.priority = int(priority, 10)
        else:
            self.priority = priority
        # 言語("N" or "E")
        self.lang = lang
        # 置換前ワード
        self.word = word
        # 置換後ワード
        self.tag = tag

    def __str__(self):
        return "%d\t%s\t%s\t%s" % (self.priority, self.lang, self.word, self.tag)


def main():
    if len(sys.argv) <= 1:
        print("Not input directory... exit.")
        return

    dir = sys.argv[1]

    # 指定したサウンドファイルに設定する優先度
    priority = 50
    if len(sys.argv) > 3:
        priority = int(sys.argv[2], 10)

    # 指定したディレクトリの配下にあるサウンドファイルを抽出する
    files = os.listdir(dir)
    if len(files) <= 0:
        print("Not found sound file(s) in %s" % dir)
        return

    with open("./ReplaceTag.dic", "r+", encoding="utf_8_sig") as dic_file:
        dic_list = []
        line = dic_file.readline()
        # 現在のファイルの内容を配列へ(優先度順で再度ソートする必要があるため)
        while line:
            splited = line.split("\t")
            if len(splited) == 4:
                dic_list.append(BouyomiDicRecord(
                    splited[0], splited[1], splited[2], splited[3].strip()))
            line = dic_file.readline()
        # サウンドファイルからレコードを生成する
        for file in files:
            dirname = os.path.split(dir)[0]
            # ディレクトリ名が空になってしまったら元に戻す
            if not dirname:
                dirname = dir
            # 先頭のカレントディレクトリマークを削除
            if dirname[0:2] == ".\\" or dirname[0:2] == "./":
                dirname = dirname[2:]
            print("%s/%s" % (dirname, file))
            fsplited = file.split(".")
            filename = ""
            if len(fsplited) == 1:
                filename = file
            else:
                # 拡張子の除去
                filename = ".".join(fsplited[:-1])

            dic_list.append(BouyomiDicRecord(
                priority, "N", filename, "(SoundW %s/%s)" % (dirname, file)))
        dic_list.sort(reverse=True, key=lambda d: d.priority)

        dic_file.seek(0)
        for dic in dic_list:
            dic_file.write(str(dic) + "\n")


if __name__ == '__main__':
    main()
