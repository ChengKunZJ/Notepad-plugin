# -*- coding: utf-8 -*-

# 导入了re模块，该模块用于处理正则表达式，以及一些全局变量的定义。
import re
from Npp import editor,LEXER,notepad,NOTIFICATION,SCINTILLANOTIFICATION,console
import os
import json
import codecs



# 设置全局颜色映射
color_map_global = []
colour_style_index = 1


# 获取当前脚本所在的路径
current_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_path, 'color_map_from_tool.txt')
# print("绝对路径:", file_path)



# 从color_map_from_tool.txt中读取关键字和颜色的映射
def read_colour_map(custom_colors_txt):
    global color_map_global
    global colour_style_index
    
    colour_style_index = 1
    
    # print("read_colour_map", custom_colors_txt)
    if os.path.exists(custom_colors_txt) and os.path.getsize(custom_colors_txt) > 0:
        
        # 从文件中读取颜色数据
        with open(custom_colors_txt, "r") as file:
            colour_map_data = json.load(file)
            # print("read_colour_map", color_map_data)

    else:
        return None
    
    # 打印关键字，字体颜色，背景颜色用于检查数据是否正常
    for colour_map_list in colour_map_data:
        keyword = colour_map_list[0]
        # fg_colour = colour_map_list[1][0]
        # bg_colour = colour_map_list[1][1]
        # print("keyword = ", keyword, " fg_colour = ", fg_colour, " bg_colour = ", bg_colour)
        
        
        colour_flag = 0
        for color_map_global_list in color_map_global:
            # 如果颜色标签已经存在，直接调用
            if(color_map_global_list[1] == colour_map_list[1]):
                colour_data = [keyword, colour_map_list[1], color_map_global_list[2]]
                colour_flag = 1
        
        if(colour_flag == 0):
            colour_data = [keyword, colour_map_list[1], colour_style_index]
            colour_style_index += 1
            # colour_style_index的上限待确定，有说31，目前工具最好使用16种就好
            # 等待测试
            
        # 存入新list
        color_map_global.append(colour_data)
    
    # print("test", color_map_global)
    # 检查新存入的数据是否有问题
    for color_map_global_list in color_map_global:
        keyword = color_map_global_list[0]
        fg_colour = color_map_global_list[1][0]
        bg_colour = color_map_global_list[1][1]
        index = color_map_global_list[2]
        # print("keyword = ", keyword, " fg_colour = ", fg_colour, " bg_colour = ", bg_colour, "index = ", index)    
    

def getColor():
    global color_map_global
    # global colour_style_index
    
    for i in range(len(color_map_global)):
        
        # print("color_map_global = ", color_map_global)
        
        foreground_value, background_value = color_map_global[i][1]
        
        fg_colour_tuple = tuple(foreground_value)
        bg_colour_tuple = tuple(background_value)
        
        # print("foreground_value", fg_colour_tuple)
        # print("background_value", bg_colour_tuple)

        editor.styleSetFore(color_map_global[i][2], fg_colour_tuple)
        editor.styleSetBack(color_map_global[i][2], bg_colour_tuple)  # 使用 RGB 元组表示颜色
        
        # print("style_number = ", color_map_global[i][2])


def processLine(line):
    global color_map_global
    
    lline_text = editor.getLine(line)                      # 获取当前行的文本内容
    
    for byte_str, color_list, num in color_map_global:
        
        keyword = byte_str.encode('utf-8')
        
        if keyword in lline_text:

            p = editor.positionFromLine(line)
            # 创建一个正则表达式模式
            pattern = re.compile(re.escape(keyword))
            # 获取匹配的起始和结束位置
            matches = [(match.start(), match.end()) for match in pattern.finditer(lline_text)]

            # 遍历匹配并设置样式
            for start, end in matches:
                editor.startStyling(p + start, num)
                editor.setStyling(int(end - start), num)

            
            # 第一版实现，只能匹配关键字，不能匹配带空格的句子
            
            # w = re.split('[ ()\[\]\{\}\-\+=]', lline_text)          # 拆分当前行为列表
            
            # # 获取指定行 line 的起始位置并将其存储在名为 p 的变量中。这是样式标记操作的开始位置。
            # p = editor.positionFromLine(line)
            
            # for ow in w:
                # # print(ow)
                # if ow.strip() == keyword:   
                    # editor.startStyling(p, num)           # 1为关键字，0为默认文本
                    # editor.setStyling(len(ow), num)
                
                # p += len(ow) + 1
                # if w[-1] == ow:
                    # p -= 1
                    

def readAll(args = 0):
    # 读取颜色设置
    read_colour_map(file_path)
    
    editor.setLexer(LEXER.CONTAINER)        # 特定语法分析器
    
    getColor()                              # 初始化关键字的颜色
    
    # 遍历所有行
    for i in range(editor.getLineCount()):
        processLine(i)                      # 设置该行的颜色
    
    print("It's OK")
    
# kill(args) 函数用于停止脚本的执行，这通常是在双击事件发生时执行的。
def kill(args):
    console.write("killed\n")
    notepad.clearCallbacks(readAll, [NOTIFICATION.BUFFERACTIVATED])
    editor.clearCallbacks(kill, [SCINTILLANOTIFICATION.DOUBLECLICK])
    return 0

# 清楚所有样式
# editor.styleClearAll()

# 设置为初始文本
text_length = editor.getTextLength()
editor.startStyling(0, 1)
editor.setStyling(text_length, 0)       # 0为默认文本，1为关键字


readAll()


notepad.callback(readAll, [NOTIFICATION.BUFFERACTIVATED])
editor.callback(kill, [SCINTILLANOTIFICATION.DOUBLECLICK])
