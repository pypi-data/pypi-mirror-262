import os, random
_all_data = {}





def show_all():
    """
    Notes: 用于获取当前包中的所有内容类别
    Args: 无
    Returns: 无
    Raises: 无
    See Also: https://yangjianqiang-lianghua.github.io/%E6%88%91%E7%9A%84%E4%B8%9A%E5%8A%A1%EF%BC%8C%E8%A7%A3%E5%8E%8B%E5%8C%85.html
    Example:
        >>> show_all()
        1、 三国
        2、 红楼
    """
    global _all_data
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', '')
    file_list = os.listdir("../data")
    print("我们目前整理了如下类别的内容，您可以将下面的每行内容作为reads()的函数参数传入，就可随机打印出该类别文件下的某一句话。连续使用reads函数可使用鼠标上箭头键。")
    print("例如：reads('三国')")
    print("==========================")
    n = 1
    for filename in file_list:
        print(f"{n}、", filename.replace(".txt", ""))
        with open(f"../data/{filename}", 'r', encoding='utf-8') as file:
            content = file.read().split("\n")[:-1]
        _all_data[str(filename).replace(".txt", "")] = content
        n += 1

def reads(filename):
    """
    Notes: 随机打印指定类别文本中的一句话，连续使用 reads() 函数可使用鼠标中的 上箭头键.
    Args: 参数就是类别名称，可以通过 show_all() 函数获取当前所有类别
    Returns: 无
    Raises: 报错已经设置为：“哎呀出错了，检查下你的输入是不是拼写错了呀！”，请检查输入的参数是否为当前包已有的类别
    See Also: https://yangjianqiang-lianghua.github.io/%E6%88%91%E7%9A%84%E4%B8%9A%E5%8A%A1%EF%BC%8C%E8%A7%A3%E5%8E%8B%E5%8C%85.html
    Example:
        >>> my_function('三国')
        '三国1'
    """
    try:
        print(random.choice(_all_data[filename]))
    except Exception as e:
        print("哎呀出错了，检查下你的输入是不是拼写错了呀！")
show_all()
print(_all_data)
reads("红楼")
