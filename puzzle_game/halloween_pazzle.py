"""
完成版「ハロウィンパズル」

横 8マス
縦 10マス
1マス 62ドット
余白 24ドット
"""
#モジュール起動
import tkinter
import random

#インデックス処理
index = 0 #ゲーム進行度
timer = 0 #時間管理
score = 0 #スコア
hisc = 0 #ハイスコア
nanido = 0 #難易度
tsugi = 0 #次にセットするキャラの値を入れる変数

#カーソルの位置
cursor_x = 0
cursor_y = 0

#マウス設定の初期化
mouse_x = 0
mouse_y = 0
mouse_c = 0 #マウスクリック時の変数

"""関数"""
#マウスを動かした時の関数
def mouse_move(e):
    global mouse_x, mouse_y
    mouse_x = e.x
    mouse_y = e.y

#マウスをクリックした時の関数
def mouse_press(e):
    global mouse_c
    mouse_c = 1

#マスのキャラリスト
mob = []
#判定用リスト
check = []
for i in range(10): #１０列
    mob.append([0,0,0,0,0,0,0,0])
    check.append([0,0,0,0,0,0,0,0])

#キャラの表示
def draw_mob():
    #一度キャラの表示を削除
    cvs.delete("MOB")
    for y in range(10): #縦
        for x in range(8): #横
            #リストの要素が0より大きいなら
            if mob[y][x] > 0:
                #キャラの画像を表示
                cvs.create_image(x*62+60, y*62+60, image=img_mob[mob[y][x]], tag="MOB")

#キャラが並んだ時の判定関数
def check_mob():
    for y in range(10): #縦
        for x in range(8): #横
            check[y][x] = mob[y][x]

    #縦に３つ並んだら
    for y in range(1, 9):
        for x in range(8):
            if check[y][x] > 0:
                if check[y-1][x] == check[y][x] and check[y+1][x] == check[y][x]:
                    mob[y-1][x] = 7
                    mob[y][x] = 7
                    mob[y+1][x] = 7

    #横に３つ並んだら
    for y in range(10):
        for x in range(1, 7):
            if check[y][x] > 0:
                if check[y][x-1] == check[y][x] and check[y][x+1] == check[y][x]:
                    mob[y][x-1] = 7
                    mob[y][x] = 7
                    mob[y][x+1] = 7

    #斜めに３つ並んだら
    for y in range(1, 9):
        for x in range(1, 7):
            if check[y][x] > 0:
                #左上と右下が同じなら
                if check[y-1][x-1] == check[y][x] and check[y+1][x+1] == check[y][x]:
                    mob[y-1][x-1] = 7
                    mob[y][x] = 7
                    mob[y+1][x+1] = 7
                
                #左下と右上が同じなら
                if check[y+1][x-1] == check[y][x] and check[y-1][x+1] == check[y][x]:
                    mob[y+1][x-1] = 7
                    mob[y][x] = 7
                    mob[y-1][x+1] = 7

#揃った後の処理
def sweep_mob():
    #消した数を数える
    num = 0
    for y in range(10):
        for x in range(8):

            #もしマスがスターになっていれば
            if mob[y][x] == 7:
                #スターを消し
                mob[y][x] = 0
                #消した数を１増やす
                num = num + 1
    return num

#落下させる関数
def drop_mob():
    #落下したかのフラグ
    flg = False
    for y in range(8, -1, -1): #縦 落下
        for x in range(8): #横
            #キャラのあるマスの 下のマス が 空なら
            if mob[y][x] != 0 and mob[y+1][x] == 0:

                #空白にキャラを入れる
                mob[y+1][x] = mob[y][x]
                #元のキャラのマスは空にする
                mob[y][x] = 0
                #落下したフラグ開始
                flg = True
    return flg

#最上段に達した確認する関数
def over_mob():
    for x in range(8):
        #もし最上段にキャラがあるなら
        if mob[0][x] > 0:
            # True と返す
            return True
    #最上段でなければ  False を返す
    return False

#最上段にキャラをセットする関数
def set_mob():
    for x in range(8):
        mob[0][x] = random.randint(0, nanido)

#影付きの文字列表示する関数
def draw_txt(txt, x, y, siz, col, tg):
    fnt = ("Times New Roman", siz, "bold")
    #２ドットずらして描写（影）
    cvs.create_text(x+2, y+2, text=txt, fill="black", font=fnt, tag=tg)
    cvs.create_text(x, y, text=txt, fill=col, font=fnt, tag=tg)


#メイン処理
def game_main():
    global index, timer, score, hisc, nanido, tsugi
    global cursor_x, cursor_y, mouse_c

    # index0(タイトルロゴ表示) の設定
    if index == 0:
        #タイトル表示
        cvs.create_image(292, 200, image=title, tag="TITLE")
        draw_txt("パズル☆ゲーム", 292, 340, 40, "yellow", "TITLE")
        #難易度 easy の表示
        cvs.create_rectangle(168, 384, 456, 456, fill="skyblue", width=0, tag="TITLE")
        draw_txt("easy", 312, 420, 40, "white", "TITLE")

        #難易度 normal の表示
        cvs.create_rectangle(168, 528, 456, 600, fill="lightgreen", width=0, tag="TITLE")
        draw_txt("normal", 312, 564, 40, "white", "TITLE")

        #難易度 hard の表示
        #cvs.create_rectangle(168, 672, 456, 744, fill="orange", width=0, tag="TITLE")
        #draw_txt("hard", 312, 708, 40, "white", "TITLE")

        # index1に移行  
        index = 1
        #クリック時にフラグ解除
        mouse_c = 0
    # index1(スタート待ち) の設定
    elif index == 1:
        #もしマウスをクリックしたら
        nanido = 0
        if mouse_c == 1:
            #もし easy を選択したならば
            if 168 < mouse_x and mouse_x < 456 and 384 < mouse_y and mouse_y < 456:
                nanido = 4 #4種類
            #もし normal 選択したならば
            if 168 < mouse_x and mouse_x < 456 and 528 < mouse_y and mouse_y < 600:
                nanido = 5  #5種類
            #もし normal 選択したならば
            if 168 < mouse_x and mouse_x < 456 and 672 < mouse_y and mouse_y < 744:
                nanido = 6  #6種類

        #nanidoの値に数値が入ってるのなら
        if nanido > 0:  
            #ゲーム初期化
            for y in range(10):
                for x in range(8):
                    mob[y][x] = 0
                    mouse_c = 0
                    score = 0
                    tsugi = 0
                    cursor_x = 0
                    cursor_y = 0
                    set_mob()
                    draw_mob()
                    cvs.delete("TITLE")
                    #  index2 に移行
                    index = 2
    
    # index2(落下) の設定
    elif index == 2:
        #もし落下先にキャラがないなら
        if drop_mob() == False:
            #  index3 に移行
            index = 3
        draw_mob()
    
    # index3(３つそろったか判定) の設定
    elif index == 3:
        #同じキャラがそろったか確認
        check_mob()
        draw_mob()
        #  index4 に移行
        index = 4
    
    # index4(そろったキャラの処理) の設定
    elif index == 4:
        #肉球を消し、消した数を sc に入れる
        sc = sweep_mob()
        #スコア加算(難易度が高いほどスコアも高い)
        score = score + sc*nanido*2
        #ハイスコア更新
        if score > hisc:
            hisc = score

        #もし消した肉球があれば
        if sc > 0:
            # index 2 に再度移行
            index = 2
        else:
            #もし最上段に達してなければ
            if over_mob() == False:
                #次のキャラをランダムに決めて
                tsugi = random.randint(1, nanido)
                # index 5 に再度移行
                index = 5

            #最上段に達したとき
            else:
                # index 6（ゲームオーバー） に再度移行
                index = 6
                timer = 0
        draw_mob()

    # index5(ポインタとカーソルの処理) の設定
    elif index == 5:
        if 24 <= mouse_x and mouse_x < 24+62*8 and 24 <= mouse_y and mouse_y < 24+62*10:
            #カーソルの横の位置を計算
            cursor_x = int((mouse_x-24)/62)
            #カーソルの縦の位置を計算
            cursor_y = int((mouse_y-24)/62)
            #もしクリックしたら
            if mouse_c == 1:
                mouse_c = 0 #クリックしたフラグ解除
                set_mob() #最上段にキャラセット
                #カーソルのマスにキャラをセット
                mob[cursor_y][cursor_x] = tsugi
                #次に配置するキャラを空にして
                tsugi = 0
                # index 2 に再度移行
                index = 2
        cvs.delete("CURSOR") #カーソルを消し
        #新たな位置にカーソルを表示
        #cvs.create_image(cursor_x*72+60, cursor_y*72+60, image=cursor, tag="CURSOR")
        cvs.create_image(cursor_x*62+60, cursor_y*62+60, image=cursor, tag="CURSOR")
        draw_mob()

    # index6(ゲームオーバー) の設定
    elif index == 6:
        timer = timer + 1
        if timer == 1:
            #ゲームオーバーと表示
            draw_txt("GAME OVER", 312, 348, 60, "red", "OVER")
        if timer == 30: #値が30になったら
            cvs.delete("OVER")
            # index 0 に移行
            index = 0
    #一度スコア表示を削除        
    cvs.delete("INFO")
    #スコア表示
    draw_txt("SCORE"+str(score), 140, 40, 32, "blue", "INFO")
    #ハイスコア表示
    draw_txt("HISC"+str(hisc), 430, 40, 32, "yellow", "INFO")

    #もし次に配置するキャラの値がセットされているならば
    if tsugi > 0:
        cvs.create_image(732, 128, image=img_mob[tsugi], tag="INFO")
    #0.2秒後に再び メイン処理 の関数を実行
    root.after(200, game_main)

""" tkinterの設定 """
#画面設定
root = tkinter.Tk()
root.title("ハロウィンパズル")
root.resizable(False, False) #画面サイズ変更不可
root.bind("<Motion>", mouse_move)
root.bind("<ButtonPress>", mouse_press)

#キャンバス設定
#cvs = tkinter.Canvas(root, width=912, height=768)
cvs = tkinter.Canvas(root, width=912, height=698, bg="violet")
cvs.pack()

#画像設定
#タイトル画像
title = tkinter.PhotoImage(file="image/title.png")

#背景
bg = tkinter.PhotoImage(file="image/bg.png")
woman = tkinter.PhotoImage(file="image/woman.png")
fukidashi = tkinter.PhotoImage(file="image/fukidashi.png")

#カーソル画像 
cursor = tkinter.PhotoImage(file="image/cursor.png")

#マスのキャラ
img_mob =[
    None, #img_mob[0]には何も入れない
    tkinter.PhotoImage(file="image/obake.png"),
    tkinter.PhotoImage(file="image/pumpkin.png"),
    tkinter.PhotoImage(file="image/zombie.png"),
    tkinter.PhotoImage(file="image/majo.png"),
    tkinter.PhotoImage(file="image/ookamiotoko.png"),
    tkinter.PhotoImage(file="image/shinigami.png"),
    tkinter.PhotoImage(file="image/star.png"),
]

#キャンバス上に背景描写
#cvs.create_image(456, 384, image=bg)
cvs.create_image(278, 344, image=bg)
cvs.create_image(760, 474, image=woman)
cvs.create_image(740, 140, image=fukidashi)

#メイン処理呼び出し
game_main()

#画面継続描写
root.mainloop()