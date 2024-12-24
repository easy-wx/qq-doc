from qq_doc import QQDocAPI


def create_xls_file(filename):
    # 创建一个excel文档
    import xlsxwriter

    # 创建一个新的Excel文件和工作表
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # 向工作表中写入数据
    worksheet.write('A1', 'Hello')
    worksheet.write('A2', 'World')

    # 关闭Excel文件
    workbook.close()


def main():
    client_id = "SET_THIS"
    client_secret = "SET_THIS"

    api = QQDocAPI(client_id, client_secret)

    # Example usage
    # permission_info = api.get_file_permission(file_id)
    # print(permission_info)
    folder_name = "这是一个文件夹"
    folder = api.create_folder_if_not_exist(folder_name)
    print(folder)
    folder_id = folder["ID"]
    dir_list = api.list_folder_contents(folder_id=folder_id)
    for dir_ in dir_list:
        print(dir_)

    xls_file = "example.xlsx"
    create_xls_file(xls_file)

    new_file = api.upload_file(xls_file, folder_id)
    file_id = new_file["ID"]

    print(api.get_file_access(file_id))

    print(api.add_collaborators(file_id, [{"type": "user", "role": "reader", "id": "user_open_id"}]))

    print(api.get_file_access(file_id))

    print(api.set_file_permission(file_id, "publicWrite"))

    print(api.get_file_access(file_id))

    print(api.get_collaborators(file_id))


main()
