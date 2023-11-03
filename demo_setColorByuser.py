import wx
import json
import os



custom_colors_txt = "custom_colors.txt"
loaded_color_data = []



def init_custom_colors(custom_colors_txt):
    # 创建一个wx.Colour对象
    custom_colors = [wx.Colour(255, 0, 0), wx.Colour(0, 255, 0), wx.Colour(0, 0, 255)]

    # 将颜色转化为RGB元组并保存到文件
    color_data = [color.Get() for color in custom_colors]

    print("init_custom_colors", color_data)

    # 将颜色数据保存到文件
    with open(custom_colors_txt, "w") as file:
        json.dump(color_data, file)

def read_custom_colors(custom_colors_txt):
    global loaded_color_data
    if os.path.exists(custom_colors_txt) and os.path.getsize(custom_colors_txt) > 0:
        try:
            # 从文件中读取颜色数据
            with open(custom_colors_txt, "r") as file:
                loaded_color_data = json.load(file)

        except FileNotFoundError:
            init_custom_colors(custom_colors_txt)
            with open(custom_colors_txt, "r") as file:
                loaded_color_data = json.load(file)
    else:
        return []

    # 打印数据自检
    # print("read_custom_colors", loaded_color_data)
    # length = len(loaded_color_data)
    # print(f"loaded_color_data 列表的长度为: {length}")

# 初始化颜色设置对话框
def init_ColourDialog(color_data):
    global loaded_color_data

    # 设置初始选择颜色，例如红色 (255, 0, 0)
    # initial_color = wx.Colour(0, 255, 0)
    # color_data.SetColour(initial_color)

    for index, color in enumerate(loaded_color_data):
        color_data.SetCustomColour(index, color)
        print(color)

# 获取用户选择的自定义颜色并保存
def save_custom_colors(color_data, custom_colors_txt):
    global loaded_color_data
    custom_colors = []

    for i in range(16):
        selected_custom_color = color_data.GetCustomColour(i)  # 假设用户选择了第一个自定义颜色
        custom_colors.append(selected_custom_color)  # 更新自定义颜色列表
    
    # 将获取的数据转换成列表
    custom_color_data = [color.Get() for color in custom_colors]
    color_lists = [list(color) for color in custom_color_data]

    # print("color_lists", color_lists)
    # print("loaded_color_data", loaded_color_data)

    if color_lists != loaded_color_data:
        loaded_color_data = color_lists
        # 将颜色数据保存到文件
        with open(custom_colors_txt, "w") as file:
            json.dump(custom_color_data, file)



class MyFrame(wx.Frame):
    def __init__(self):
        super(MyFrame, self).__init__(None, wx.ID_ANY, "设置背景颜色示例", size=(400, 300))
        
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.Colour(255, 0, 0))  # 初始背景颜色为红色
        
        # 创建按钮，用于打开颜色选择对话框
        color_button = wx.Button(self.panel, label="设置背景颜色")
        color_button.Bind(wx.EVT_BUTTON, self.OnColorButtonClick)
        
        self.Show(True)
        

    # 示例
    def OnColorButtonClick(self, event):
        dlg = wx.ColourDialog(self)
        color_data = dlg.GetColourData()
        # 透明度相关
        color_data.SetChooseFull(True)
        
        # 初始化自定义颜色设置对话框
        init_ColourDialog(color_data)
        
        if dlg.ShowModal() == wx.ID_OK:
            color_data = dlg.GetColourData()
            color = color_data.GetColour()
            self.panel.SetBackgroundColour(color)
            self.panel.Refresh()                        # 刷新

            # 保存数据到自定义栏
            save_custom_colors(color_data, custom_colors_txt)
            # print(color_data)
            # print(color)
        dlg.Destroy()


if __name__ == '__main__':
    # 初始化自定义颜色
    read_custom_colors(custom_colors_txt)
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
