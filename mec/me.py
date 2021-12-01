import imp
import pyautogui
import asyncio
pyautogui.alert('경고!') # 경고창 띄움. 메세지박스. #확인 버튼만 존재

vars = pyautogui.confirm('확인 또는 취소를 눌러보세요~~~') # 확인 또는 취소 버튼을 누를 수 있는 메시지 박스를 띄움. '확인'을 클릭하면 vars 에 'OK' 리턴, '취소'를 클릭하면 vars 에 'Cancel' 리턴

vars = pyautogui.prompt('문자를 적어보세요~') 
async def main():
    while True:
        pyautogui.hotkey('ctrl', 'v')  #단축키 누르기
        pyautogui.hotkey('enter')
        asyncio.sleep(1)
    