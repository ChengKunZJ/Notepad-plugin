import wx
import wx.grid as gridlib
from demo_setColorByuser import read_custom_colors, init_ColourDialog, save_custom_colors



custom_colors_txt = "custom_colors.txt"



class MyGrid(wx.Frame):
    def __init__(self):
        super(MyGrid, self).__init__(None, title="Color Picker in Grid", size=(400, 300))

        self.grid = gridlib.Grid(self)
        self.grid.CreateGrid(5, 5)

        # 绑定右击事件
        self.grid.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.on_right_click)

        self.Show()

    def on_right_click(self, event):
        row = event.GetRow()
        col = event.GetCol()

        print("row = ", row, "col = ", col)
        if col != 4:
            # event.Skip()
            return
        print("row = ", row, "col = ", col)

        # 创建右击菜单
        menu = wx.Menu()

        # 添加选项
        foreground_color_option = menu.Append(wx.ID_ANY, "字体颜色")
        background_color_option = menu.Append(wx.ID_ANY, "背景颜色")

        # 绑定菜单选择事件
        # self.Bind(wx.EVT_MENU, self.on_foreground_color_select, foreground_color_option)
        # self.Bind(wx.EVT_MENU, self.on_background_color_select, background_color_option)

         # 绑定菜单项的事件处理，将参数传递给处理函数
        self.Bind(wx.EVT_MENU, lambda event, row=row, col=col: self.on_background_color_select(event, row, col), background_color_option)
        self.Bind(wx.EVT_MENU, lambda event, row=row, col=col: self.on_foreground_color_select(event, row, col), foreground_color_option)

        
        # 弹出菜单
        self.PopupMenu(menu)

    def on_foreground_color_select(self, event, row, col):
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

            # 设置单元格的颜色
            self.grid.SetCellTextColour(row, col, color)
            self.grid.SetCellValue(row, col, "Test")


            # 保存数据到自定义栏
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

            # 设置单元格的颜色
            self.grid.SetCellBackgroundColour(row, col, color)
            self.grid.SetCellValue(row, col, "Test")


            # 保存数据到自定义栏
            save_custom_colors(color_data, custom_colors_txt)

        dlg.Destroy()



if __name__ == "__main__":
    # DEMO initial
    read_custom_colors(custom_colors_txt)
    app = wx.App(False)
    frame = MyGrid()
    app.MainLoop()

