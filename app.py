from flask import Flask
app = Flask(__name__) # __name__ 為 python 內建的變數，他會儲存目前程式在哪個模組下執行

@app.route("/") #函式的裝飾 ( Decorator )，以底下函式為基礎，提供附加的功能，這邊 "/" 代表根目錄
def home():
    return "Hello Flask"
    
if __name__ == "__main__": #如果以主程式運行
    app.run() #啟動伺服器