import wx
import os
import csv
import wx.grid as gridlib
# import serial
#import serial.tools.list_ports

# 从 test 模块中导入 MainFrame 类
from app import MyFrame
from demo_setColorByuser import read_custom_colors, init_ColourDialog, save_custom_colors
import re
import json
import shutil




# 定义一个全局变量来保存当前打开的文件路径
file_path = "data.csv"
custom_colors_txt = "custom_colors.txt"
user_keywords_color = "user_keywords_color.txt"

# 用于设置全选或者取消全选
set_all_flag = "√"
# 第四列的字体颜色和背景颜色 [ [0,0,0],[255,255,255]], [[0,0,0],[255,255,255]], ..., ...]
loaded_user_keywords_color_data = []
# 生成颜色标记脚本的路径，给Notepad++的python脚本使用
# pyscrip_for_notepad_path = "C:\Users\cn_zh\AppData\Roaming\Notepad++\plugins\config\PythonScript\scripts\color_map_from_tool.txt"
# pyscrip_for_notepad_path = r"C:\Users\cn_zh\AppData\Roaming\Notepad++\plugins\config\PythonScript\scripts\color_map_from_tool.txt"
pyscrip_for_notepad_path = None




class NewWindow(MyFrame):
    def __init__(self, parent):
        super(NewWindow, self).__init__(parent)

        # 设置标题
        self.SetTitle("Notepad++ Notebook ")
        title_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        # 使用 SetSize 方法来重新设置窗口大小
        self.SetSize(wx.Size(1150, 600))

        # 自定义列标签
        self.m_grid.SetColLabelValue(0, "匹配项")
        self.m_grid.SetColLabelValue(1, "关键字")
        self.m_grid.SetColLabelValue(2, "描述")
        self.m_grid.SetColLabelValue(3, "颜色")
        self.m_grid.SetColLabelValue(4, "标签")

        # 设置行号列宽度
        self.m_grid.SetRowLabelSize(60)  # 这里设置为100像素，你可以根据需要调整宽度

        # 设置第一列的宽度
        # self.m_grid.SetColSize(0, 100)  # 这里设置为100像素，你可以根据需要调整宽度

        # 设置第一列的单元格内容居中显示
        for row in range(self.m_grid.GetNumberRows()):
            self.m_grid.SetCellAlignment(row, 0, wx.ALIGN_CENTER, wx.ALIGN_CENTER)
            # 增加第五列居中
            self.m_grid.SetCellAlignment(row, 4, wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        # 第一列双击切换
        # 设置第一列的单元格为只读
        for row in range(self.m_grid.GetNumberRows()):
            self.m_grid.SetReadOnly(row, 0, True)
        self.m_grid.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.on_cell_double_click)


        # 从文件加载数据到表格
        self.load_data_from_file()

        # 创建一个定时器，设置间隔为1分钟（60,000毫秒）
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(60000)  # 启动定时器

        # 第四列背景颜色与字体颜色设置
        self.cell_font_background_colour(user_keywords_color)

    

########## 以上是按键绑定与相关事件处理 ##########



        # Connect Events
        self.Bind( wx.EVT_MENU, self.m_menuItem_openOnMenuSelection, id = self.m_menuItem_open.GetId() )
        self.Bind( wx.EVT_MENU, self.m_menuItem_saveOnMenuSelection, id = self.m_menuItem_save.GetId() )
        self.m_button_update.Bind( wx.EVT_BUTTON, self.m_button_updateOnButtonClick )
        self.m_button_copy.Bind( wx.EVT_BUTTON, self.m_button_copyOnButtonClick )
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyShortcut)         # 绑定键盘快捷键 Ctrl + S
        self.m_button_setAllTo0.Bind( wx.EVT_BUTTON, self.m_button_setAllTo0OnButtonClick )
        # 绑定右击事件
        self.m_grid.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.on_cell_right_click)
        self.Bind( wx.EVT_MENU, self.m_menuItem_setNotepadPathOnMenuSelection, id = self.m_menuItem_setNotepadPath.GetId() )





    # Virtual event handlers, overide them in your derived class
    # 设置notepad++的路径
    def m_menuItem_setNotepadPathOnMenuSelection( self, event ):
        global pyscrip_for_notepad_path
        current_path = self.select_folder_path()
        if(current_path != None):
            pyscrip_for_notepad_path = os.path.join(current_path, 'color_map_from_tool.txt')

            # 设置成功后 copy 脚本到notepad++
            shutil.copy("setcolorByTool.py", os.path.join(current_path, 'setcolorByTool.py'))
            # shutil.copy("notepad_plugin.pyc", os.path.join(current_path, 'notepad_plugin.pyc'))

            notepad_path = "notepad_path.txt"
            with open(notepad_path, 'w') as file:
                file.write(pyscrip_for_notepad_path)
                print("notepad_path.txt", pyscrip_for_notepad_path)
		# event.Skip()

    def m_menuItem_openOnMenuSelection( self, event ):
        self.open_new_file()
        # event.Skip()
    def m_menuItem_saveOnMenuSelection( self, event ):
        self.save_to_specified_csv()
        # event.Skip()
    def m_button_updateOnButtonClick( self, event ):
        self.output_data_by_col()
        self.color_map_for_notepad()         # 保存数据到notepad
        # event.Skip()
    def m_button_copyOnButtonClick( self, event ):
        self.copy_data_to_clipboard()
        # event.Skip()
    def OnKeyShortcut(self, event):
        # 捕捉键盘事件，判断是否按下 Ctrl + S
        if event.GetKeyCode() == ord('S') and event.ControlDown():
            self.save_to_current_csv()
            self.print_operation_info()
            # 保存第四列字体颜色和背景颜色
            self.save_cell_background_colour(custom_colors_txt)
        else:
            event.Skip()
    # 把所有选择设置为0
    def m_button_setAllTo0OnButtonClick( self, event ):
        global set_all_flag
        for row in range(self.m_grid.GetNumberRows()):                          # 后续出现问题，可能是定行200行导致的
            self.m_grid.SetCellValue(row, 0, set_all_flag)                 # 设置表格数据为0
            self.set_cell_to_default(row, 0, set_all_flag)                 # 设置背景颜色为默认
                                                                                # 设置背景颜色与字体颜色
        if(set_all_flag == "√"):
            set_all_flag = "×"
        else:
            set_all_flag = "√"
        # event.Skip()

    # 单元格第4列 -- 颜色设置
    def on_cell_right_click(self, event):
        row = event.GetRow()
        col = event.GetCol()

        # 处理字体颜色，背景色
        if col == 3:        # 第四列
            # 创建右击菜单
            menu = wx.Menu()

            # 添加选项
            foreground_color_option = menu.Append(wx.ID_ANY, "字体颜色")
            background_color_option = menu.Append(wx.ID_ANY, "背景颜色")

            # 绑定菜单项的事件处理，将参数传递给处理函数
            self.Bind(wx.EVT_MENU, lambda event, row=row, col=col: self.on_foreground_color_select(event, row, col), foreground_color_option)
            self.Bind(wx.EVT_MENU, lambda event, row=row, col=col: self.on_background_color_select(event, row, col), background_color_option)

            # 弹出菜单
            self.PopupMenu(menu)

        # 处理标签
        if col == 4:        # 第五列

            label_text = self.m_grid.GetCellValue(row, col)
            print("label_text = ", label_text)
            # 创建右击菜单
            menu = wx.Menu()

            # 添加选项
            label_setAllTo_1 = menu.Append(wx.ID_ANY, "Set all to √")
            label_setAllTo_0 = menu.Append(wx.ID_ANY, "Set all to ×")

            # 绑定菜单项的事件处理，将参数传递给处理函数
            self.Bind(wx.EVT_MENU, lambda event, row=row, col=col, label_text=label_text: self.on_label_setAllTo_0(event, row, col, label_text), label_setAllTo_0)
            self.Bind(wx.EVT_MENU, lambda event, row=row, col=col, label_text=label_text: self.on_label_setAllTo_1(event, row, col, label_text), label_setAllTo_1)

            # 弹出菜单
            self.PopupMenu(menu)



########## 以上是按键绑定与相关事件处理 ##########

    def on_foreground_color_select(self, event, row, col):
        global loaded_user_keywords_color_data

        print("字体颜色 row = ", row, " col = ", col)

        dlg = wx.ColourDialog(self)
        color_data = dlg.GetColourData()
        # 透明度相关
        color_data.SetChooseFull(True)
        
        # 初始化自定义颜色设置对话框
        init_ColourDialog(color_data)
        
        if dlg.ShowModal() == wx.ID_OK:
            color_data = dlg.GetColourData()
            color = color_data.GetColour()

            # 设置单元格字体的颜色
            self.m_grid.SetCellTextColour(row, col, color)
            self.m_grid.SetCellValue(row, col, " font & background")
            
            # 保存数据到文本
            color_list = list(color[:3])
            print("on_foreground_color_select ", color_list)
            loaded_user_keywords_color_data[row][0] = color_list



            # 保存数据到自定义栏(自定义颜色选择列表)
            save_custom_colors(color_data, custom_colors_txt)

        dlg.Destroy()

    
    def on_background_color_select(self, event, row, col):
        print("背景颜色 row = ", row, " col = ", col)

        dlg = wx.ColourDialog(self)
        color_data = dlg.GetColourData()
        # 透明度相关
        color_data.SetChooseFull(True)
        
        # 初始化自定义颜色设置对话框
        init_ColourDialog(color_data)
        
        if dlg.ShowModal() == wx.ID_OK:
            color_data = dlg.GetColourData()
            color = color_data.GetColour()

            # 设置单元格背景的颜色
            self.m_grid.SetCellBackgroundColour(row, col, color)
            self.m_grid.SetCellValue(row, col, " font & background")

            # 保存数据到文本
            color_list = list(color[:3])
            print("on_foreground_color_select ", color_list)
            loaded_user_keywords_color_data[row][1] = color_list


            # 保存数据到自定义栏
            save_custom_colors(color_data, custom_colors_txt)

        dlg.Destroy()

    def on_label_setAllTo_0(self, event, row, col, label_text):
        print("on_label_setAllTo_0 row = ", row, " col = ", col)
        for row in range(self.m_grid.GetNumberRows()):                          # 后续出现问题，可能是定行200行导致的
            if(self.m_grid.GetCellValue(row, col) == label_text):
                self.m_grid.SetCellValue(row, 0, "×")                 # 设置表格数据为0
                self.set_cell_to_default(row, 0, "×")                 # 设置背景颜色为默认

    def on_label_setAllTo_1(self, event, row, col, label_text):
        print("on_label_setAllTo_1 row = ", row, " col = ", col)
        for row in range(self.m_grid.GetNumberRows()):                          # 后续出现问题，可能是定行200行导致的
            if(self.m_grid.GetCellValue(row, col) == label_text):
                self.m_grid.SetCellValue(row, 0, "√")                 # 设置表格数据为0
                self.set_cell_to_default(row, 0, "√")                 # 设置背景颜色为默认





    def copy_data_to_clipboard(self):
        # 创建一个字符串，你想要复制到剪贴板的内容
        text_to_copy = self.m_textCtrl.GetValue()

        # 创建一个 wx.ClipData 对象并设置要复制的文本
        clipdata = wx.TextDataObject(text_to_copy)

        # 获取剪贴板
        clipboard = wx.Clipboard.Get()

        # 将数据复制到剪贴板
        clipboard.SetData(clipdata)

        # 释放剪贴板
        # clipboard.Close()
        print("复制数据成功")


    # 定时保存数据
    def OnTimer(self, event):
        # 定时器事件处理函数，在这里定义你想要执行的任务
        self.save_to_current_csv()
        global file_path
        print("自动保存数据，任务执行中...", file_path)

        # 保存第四列字体颜色和背景颜色
        self.save_cell_background_colour(custom_colors_txt)

        # 添加你的任务逻辑 OnTimer END


    # 模拟弹窗显示
    def print_operation_info(self):
        self.SetTitle("Notepad++ Notebook                                                     保存成功！")
        wx.CallLater(2000, self.SetTitle, "Notepad++ Notebook ")

    # 保存数据到当前文件
    def save_to_current_csv(self):
        try:
            global file_path
            with open(file_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                for row in range(self.m_grid.GetNumberRows()):
                    row_data = [self.m_grid.GetCellValue(row, col) for col in range(self.m_grid.GetNumberCols())]
                    csvwriter.writerow(row_data)
                
                print("ctrl + s , 保存数据成功", file_path)
        except Exception as e:
            wx.LogError(f"Error saving CSV file: {str(e)}")


    # 选择一个文件夹路径
    def select_folder_path(self):
        folder_dialog = wx.DirDialog(self, "Select a folder")
        if folder_dialog.ShowModal() == wx.ID_CANCEL:
            return None

        folder_path = folder_dialog.GetPath()
        folder_dialog.Destroy()

        return folder_path


    # 保存数据到指定文件
    def save_to_specified_csv(self):
        file_dialog = wx.FileDialog(self, "Save CSV file", wildcard="CSV files (*.csv)|*.csv", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        
        if file_dialog.ShowModal() == wx.ID_CANCEL:
            return

        file_path = file_dialog.GetPath()
        file_dialog.Destroy()

        try:
            with open(file_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                for row in range(self.m_grid.GetNumberRows()):
                    row_data = [self.m_grid.GetCellValue(row, col) for col in range(self.m_grid.GetNumberCols())]
                    csvwriter.writerow(row_data)

                print("save_to_specified_csv , 保存数据成功", file_path)
        except Exception as e:
            wx.LogError(f"Error saving CSV file: {str(e)}")



    # 第一列 0 1 切换
    def on_cell_double_click(self, event):
        row = event.GetRow()
        col = event.GetCol()
        if col == 0:
            current_value = self.m_grid.GetCellValue(row, col)
            new_value = "√" if current_value == "×" else "×"
            self.m_grid.SetCellValue(row, col, new_value)
        
            # 设置背景颜色
            self.set_cell_to_default(row, col, new_value)


    def set_cell_to_default(self, row, col, value):
        if value == "×":
            self.m_grid.SetCellBackgroundColour(row, col, wx.Colour(255, 255, 255)) 
            self.m_grid.SetCellBackgroundColour(row, col + 1, wx.Colour(255, 255, 255))  
            self.m_grid.SetCellBackgroundColour(row, col + 2, wx.Colour(255, 255, 255))  
            # self.m_grid.SetCellBackgroundColour(row, col + 3, wx.Colour(255, 255, 255))
            self.m_grid.SetCellBackgroundColour(row, col + 4, wx.Colour(255, 255, 255))
        else:
            self.m_grid.SetCellBackgroundColour(row, col, wx.Colour(232, 252, 225))
            self.m_grid.SetCellBackgroundColour(row, col + 1, wx.Colour(232, 252, 225))
            self.m_grid.SetCellBackgroundColour(row, col + 2, wx.Colour(232, 252, 225))
            # self.m_grid.SetCellBackgroundColour(row, col + 3, wx.Colour(232, 252, 225))
            self.m_grid.SetCellBackgroundColour(row, col + 4, wx.Colour(232, 252, 225))

    # 加载文件
    def load_data_from_file(self):
        global file_path
        try:
            with open(file_path, 'r', newline='') as csvfile:
            # with open('data.csv', 'r', newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                for row_num, row in enumerate(csvreader):
                    for col_num, value in enumerate(row):
                        
                        if row_num < self.m_grid.GetNumberRows() and col_num < self.m_grid.GetNumberCols():
                            self.m_grid.SetCellValue(row_num, col_num, value)

                self.cell_background_colour()
        except FileNotFoundError:
            # 如果文件不存在，什么都不做
            wx.LogError("File not found.")


    # 打印目标字符串到显示窗口
    # 根据第一列的数据打印第二列
    def output_data_by_col(self):
        result = ""
        # 假设表格的第一列是列0，第二列是列1
        for row in range(self.m_grid.GetNumberRows()):
            value_in_first_column = self.m_grid.GetCellValue(row, 0)
            if value_in_first_column == "√":
                value_in_second_column = self.m_grid.GetCellValue(row, 1)

                result += value_in_second_column + "|"
                print(f"Row {row}: {value_in_second_column}")

        # 去掉最后一个 " | " 分隔符
        result = result.rstrip("|")
        print(result)

        # 转译正则表达式中的特殊字符
        # escaped_string = re.escape(result)
        escaped_string = re.sub(r"([.*+?^$[\](){}])", r"\\\1", result)
        print(escaped_string)

        # 去除连续的 |||
        escaped_modified_string = re.sub(r'\|+', '|', escaped_string)
        print(escaped_modified_string)

        # 去除第一行的“|”
        if escaped_modified_string.startswith("|"):
            modified_string = escaped_modified_string[1:]
        else:
            modified_string = escaped_modified_string
        print(modified_string)


        self.m_textCtrl.SetValue(modified_string)


    # 打开一个新的文件
    def open_new_file(self):
        with wx.FileDialog(self, "Open CSV file", wildcard="CSV files (*.csv)|*.csv", style=wx.FD_OPEN) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            global file_path
            file_path = fileDialog.GetPath()
            self.load_data_from_file()
            print("打开文件成功", file_path)



    # 初始化第一列背景颜色
    def cell_background_colour(self):
        for row in range(200):
            value = self.m_grid.GetCellValue(row, 0)  # 获取第一列的值
            self.set_cell_to_default(row, 0, value)


    def refresh_font_background_colour(self):
        global loaded_user_keywords_color_data
        col = 3     # 第四列
        for row in range(self.m_grid.GetNumberRows()): 
            self.m_grid.SetCellTextColour(row, col, loaded_user_keywords_color_data[row][0])
            self.m_grid.SetCellBackgroundColour(row, col, loaded_user_keywords_color_data[row][1])
            if(self.m_grid.GetCellValue(row, col) == ""):
                print("Set cell text to -- font & background")
                self.m_grid.SetCellValue(row, col, " font & background")

    # 保存第四列字体和背景颜色到文本
    def save_cell_background_colour(self, custom_colors_txt):
        global user_keywords_color
        global loaded_user_keywords_color_data
        # print("save_cell_background_colour", loaded_user_keywords_color_data)

        with open(user_keywords_color, 'w') as csvfile:
            json_data = json.dumps(loaded_user_keywords_color_data)
            csvfile.write(json_data)
            print("save_cell_background_colour 保存成功")

    # 初始化第四列字体和背景颜色
    def cell_font_background_colour(self, custom_colors_txt):
        global loaded_user_keywords_color_data
        if os.path.exists(custom_colors_txt) and os.path.getsize(custom_colors_txt) > 0:
            try:
                # 从文件中读取颜色数据
                with open(custom_colors_txt, "r") as file:
                    loaded_user_keywords_color_data = json.load(file)

            except FileNotFoundError:
                print("读取数据错误，", custom_colors_txt)
        else:
            return None

        self.refresh_font_background_colour()
        # 打印数据自检
        # print("cell_font_background_colour", loaded_user_keywords_color_data)
        # length = len(loaded_user_keywords_color_data)
        # print(f"loaded_user_keywords_color_data 列表的长度为: {length}")
    
    def color_map_for_notepad(self):
        # notepad 路径
        global pyscrip_for_notepad_path
        global loaded_user_keywords_color_data
        pyscrip_for_notepad_data = []

        for row in range(self.m_grid.GetNumberRows()):
            if(self.m_grid.GetCellValue(row, 0) == "√") and (self.m_grid.GetCellValue(row, 1) != ""):
                pyscrip_for_notepad_data.append((self.m_grid.GetCellValue(row, 1), loaded_user_keywords_color_data[row]))

        # print("color_map_for_notepad ", pyscrip_for_notepad_data)

        with open(pyscrip_for_notepad_path, 'w') as csvfile:
            json_data = json.dumps(pyscrip_for_notepad_data)
            csvfile.write(json_data)




# class NewWindow(MyFrame): END





def environmentInit():
    # 检查当前路径下是否存在data.csv文件
    file_path = "data.csv"
    if not os.path.isfile(file_path):
        # 文件不存在，创建一个新的data.csv文件
        with open(file_path, 'w') as csvfile:
            # csvfile.write("Header1,Header2,Header3\n")  # 写入表格的列标题，根据需要修改

            for _ in range(200):
                csvfile.write("×\n")

    # 关键字颜色与背景颜色
    global user_keywords_color
    user_keywords_color = "user_keywords_color.txt"
    if not os.path.isfile(user_keywords_color):

        # 文件不存在，创建一个新的文件
        with open(user_keywords_color, 'w') as csvfile:
            # csvfile.write("Header1,Header2,Header3\n")  # 写入表格的列标题，根据需要修改

            user_keywords_color_data = []
            for _ in range(200):
                user_keywords_color_data.append([(0, 0, 0), (255, 255, 255)])
            
            json_data = json.dumps(user_keywords_color_data)
            csvfile.write(json_data)
    
    # 读取notepad++的路径，刷新
    global pyscrip_for_notepad_path
    notepad_path = "notepad_path.txt"
    if not os.path.isfile(notepad_path):
        # 文件不存在，创建一个新的文件
        with open(notepad_path, 'w') as csvfile:
            print("notepad_path 创建")
            pass
    else:
        with open(notepad_path, 'r') as file:
            pyscrip_for_notepad_path = file.read()

    print("notepad_path", pyscrip_for_notepad_path)



if __name__ == '__main__':
    environmentInit()
    # 初始化自定义颜色
    read_custom_colors(custom_colors_txt)

    app = wx.App()
    nwid = NewWindow(None)
    nwid.Show()
    app.MainLoop()