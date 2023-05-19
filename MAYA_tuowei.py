import maya.cmds as cmds
import MASH.api as mapi

# 定义一个函数，用于将创建的模型隐藏
def change_attr():
    # 输入选择模型
    object_list = cmds.ls(sl=1)
    attr_name = 'visibility'
    # 将选择模型的shape节点名称赋给一个变量
    object_shape = cmds.listRelatives(s=1)[0]
    #更改模型的显示属性
    cmds.setAttr("{}.{}".format(object_shape, attr_name), 0)


# 定义一个函数，用于创建面片并创建一个点约束
def creatFjoint():
    # 使用ls命令获取当前选择的物体，并使用long参数返回完整的路径名
    hehe = cmds.ls(selection=True, long=True)
    # 使用len函数获取选择物体的数量
    num_he = len(hehe)
    # 使用select命令清空当前选择
    cmds.select(clear=True)

    # 使用for循环遍历每个选择的物体
    for hei in range(num_he):
        # 使用字符串拼接构造一个新的面片名字，去掉首尾的下划线
        temp_name = "_bone_" + hehe[hei]
        newJNT_tmp = temp_name[1:-1]

        # 一个新的面片模型，并使用name参数指定名字，position参数指定位置
        obj = cmds.polyPlane(w=1, h=1, sx=1, sy=1)

        # 将创建的模型隐藏
        change_attr()

        #重命名后赋给一个新的变量
        newJNT = cmds.rename(newJNT_tmp)

        # 使用select命令清空当前选择，并选择新创建的骨骼关节
        cmds.select(clear=True)
        cmds.select(newJNT)

        # parent -w $newJNT;
        # 使用group命令创建一个组，并使用xform命令设置组的中心点为原点
        cmds.group()
        cmds.xform(objectSpace=True, pivots=(0, 0, 0))

        # 使用rename命令给组重命名，并加上"_grp"后缀
        newGRP = cmds.rename(newJNT + "_grp")

        # 使用select命令清空当前选择，并选择原始物体和新创建的组
        cmds.select(clear=True)
        cmds.select(hehe[hei])
        cmds.select(newGRP, add=True)

        # 使用pointOnPolyConstraint命令创建一个点约束，使组跟随原始物体的位置变化
        cmds.pointOnPolyConstraint(weight=1)

        # 使用select命令清空当前选择
        cmds.select(clear=True)

        return newJNT

# 定义一个函数，用于选择模型并返回模型的shape节点
def xuanze ():

    mod = cmds.ls(selection=True)
    backplate = cmds.listRelatives(s=1)[0]
    return backplate

#定义一个函数，用于创建mash网格并设置mash分布类型为网格，设置mash分布类型为网格，然后创建轨迹节点
def meshset (plate,):
    # 创建生成mash网格
    cube = cmds.polyCube(w=1, h=1,)
    # 将创建的模型隐藏
    change_attr()
    # 选择生成网格创建mash
    cmds.select(cube[0])
    mashNetwork = mapi.Network()
    mashNetwork.createNetwork()

    # 设置mash分布类型为网格
    cmds.setAttr(mashNetwork.distribute + '.arrangement', 4)
    cmds.setAttr(mashNetwork.distribute + '.pointCount', 1)
    cmds.setAttr(mashNetwork.distribute + '.meshType', 4)

    # 将选择模型的输出世界网格连接到mesh的输入网格
    cmds.connectAttr("{0}.worldMesh".format(plate), mashNetwork.distribute + '.inputMesh')

    # 创建轨迹节点
    node = mashNetwork.addNode("MASH_Trails")


# 定义一个run函数，用于运行主体代码
def run():
    mod = creatFjoint()
    cmds.select(mod)
    plate = xuanze()
    meshset(plate)


#定义修改函数
#------------------------------------------------------------------------------------------------   
     
# 定义一个函数，用于修改轨迹节点的宽度参数
def width (name,value):
    cmds.setAttr("{}.trailWidth".format(name), value)

# 定义一个函数，用于修改轨迹节点的长度参数
def lenght (name,value):
    cmds.setAttr("{}.trailLength".format(name), value)

# 定义一个函数，用于修改轨迹节点的曲线采样参数
def samples (name,value):
    cmds.setAttr("{}.curveSamples".format(name), value)

#定义回调函数
#------------------------------------------------------------------------------------------------

# 定义一个更新函数，用于同步输入框和滑块的值，并且调用width函数
def width_update(*args):
    name = cmds.textField(textField, query=True, text=True)
    # 获取输入框的文本
    text = cmds.textField(textFieldwidth, query=True, text=True)
    # 获取滑块的值
    value = cmds.floatSlider(sliderwidth, query=True, value=True)
    # 设置输入框的文本为滑块的值
    cmds.textField(textFieldwidth, edit=True, text=str(value))
    # 调用canshu函数，传入文本和值作为参数
    width (name,value)

# 定义一个反向更新函数，用于根据输入框的值改变滑块的值
def width_reverse_update(*args):
    name = cmds.textField(textField, query=True, text=True)
    # 获取输入框的文本
    text = cmds.textField(textFieldwidth, query=True, text=True)
    # 尝试将文本转换为浮点数
    value = float(text)
    # 设置滑块的值为文本对应的数值
    cmds.floatSlider(sliderwidth, edit=True, value=value)
    # 调用canshu函数，传入文本和值作为参数
    width (name,value)
#------------------------------------------------------------------------------------------------------------------------


# 定义一个更新函数，用于同步输入框和滑块的值，并且调用lenght函数
def lenght_update(*args):
    name = cmds.textField(textField, query=True, text=True)
    # 获取输入框的文本
    text = cmds.textField(textFieldlenght, query=True, text=True)
    # 获取滑块的值
    value = cmds.floatSlider(sliderlenght, query=True, value=True)
    # 设置输入框的文本为滑块的值
    cmds.textField(textFieldlenght, edit=True, text=str(value))
    # 调用canshu函数，传入文本和值作为参数
    lenght (name,value)

# 定义一个反向更新函数，用于根据输入框的值改变滑块的值
def lenght_reverse_update(*args):
    name = cmds.textField(textField, query=True, text=True)
    # 获取输入框的文本
    text = cmds.textField(textFieldlenght, query=True, text=True)
    # 尝试将文本转换为浮点数
    value = float(text)
    # 设置滑块的值为文本对应的数值
    cmds.floatSlider(sliderlenght, edit=True, value=value)
    # 调用canshu函数，传入文本和值作为参数
    lenght (name,value)
#----------------------------------------------------------------------------------------------------------------------------

# 定义一个更新函数，用于同步输入框和滑块的值，并且调用samples函数
def samples_update(*args):
    name = cmds.textField(textField, query=True, text=True)
    # 获取输入框的文本
    text = cmds.textField(textFieldsamples, query=True, text=True)
    # 获取滑块的值
    value = cmds.floatSlider(slidersamples, query=True, value=True)
    # 设置输入框的文本为滑块的值
    cmds.textField(textFieldsamples, edit=True, text=str(value))
    # 调用canshu函数，传入文本和值作为参数
    samples (name,value)

# 定义一个反向更新函数，用于根据输入框的值改变滑块的值
def samples_reverse_update(*args):
    name = cmds.textField(textField, query=True, text=True)
    # 获取输入框的文本
    text = cmds.textField(textFieldsamples, query=True, text=True)
    # 尝试将文本转换为浮点数
    value = float(text)
    # 设置滑块的值为文本对应的数值
    cmds.floatSlider(slidersamples, edit=True, value=value)
    # 调用canshu函数，传入文本和值作为参数
    samples (name,value)

#----------------------------------------------------------------------------------------------
#界面功能

# 创建一个窗口，标题为“一键拖尾工具”
window = cmds.window(title="一键拖尾工具", widthHeight=(300, 150))

# 创建一个垂直布局
cmds.columnLayout()

# 创建一个文本标签，显示提示信息
cmds.text(label="选中模型的一个点，然后运行代码")

# 创建一个按钮，运行拖尾代码主体
cmds.button(label="运行", command=lambda x: run( ))

# 创建一个文本标签，显示提示信息
cmds.text(label="输入需要改变的轨迹节点名称")

# 创建一个输入框
textField = cmds.textField(placeholderText="输入轨迹节点名称")

# 创建一个文本标签，显示提示信息
cmds.text(label="修改轨迹宽度")
#-----------------------------------------------------------------------------------------------------------------------------

# 创建一个输入框，设置默认文本为0.0，添加回车命令为反向更新函数
textFieldwidth = cmds.textField(text="4", enterCommand=width_reverse_update)

# 创建一个滑块，设置最小值为0.0，最大值为10.0，步长为0.1，初始值为0.0，添加拖动命令为更新函数
sliderwidth = cmds.floatSlider(min=0, max=10, value=4, step=0.1, changeCommand=width_update, dragCommand=width_update)
#------------------------------------------------------------------------------------------------------------------------------

# 创建一个文本标签，显示提示信息
cmds.text(label="修改轨迹长度")

# 创建一个输入框，设置默认文本为20，添加回车命令为反向更新函数
textFieldlenght = cmds.textField(text="20", enterCommand=lenght_reverse_update)

# 创建一个滑块，设置最小值为0.0，最大值为50.0，步长为0.1，初始值为20，添加拖动命令为更新函数
sliderlenght = cmds.floatSlider(min=0, max=50, value=20, step=0.1, changeCommand=lenght_update, dragCommand=lenght_update)
#------------------------------------------------------------------------------------------------------------------------------

# 创建一个文本标签，显示提示信息
cmds.text(label="修改轨迹采样")

# 创建一个输入框，设置默认文本为6，添加回车命令为反向更新函数
textFieldsamples = cmds.textField(text="6", enterCommand=samples_reverse_update)

# 创建一个滑块，设置最小值为0.0，最大值为20.0，步长为0.1，初始值为6，添加拖动命令为更新函数
slidersamples = cmds.floatSlider(min=0, max=20, value=6, step=0.1, changeCommand=samples_update, dragCommand=samples_update)


# 显示窗口
cmds.showWindow(window)