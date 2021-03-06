from PyQt5.QtWidgets import QFileDialog

previous_file = None
file_pattern = ''


def file_open(form, previous_file: str, file_pattern: str):
    """file open - common method to get file name"""
    file, _ = QFileDialog.getOpenFileName(form,
        "Open file",
        "",
        "{};;All files (*.*)".format(file_pattern),
        # options=QFileDialog.DontUseNativeDialog
    )

    if file not in (previous_file, ''):
        return file
    else:
        return previous_file


def file_save(form, previous_file: str, file_pattern: str):
    """file save - common method to get file name"""
    file, _ = QFileDialog.getSaveFileName(
        form,
        "save file",
        "",
        "{};;All files (*.*)".format(file_pattern),
        # options=QFileDialog.DontUseNativeDialog
    )

    if file not in (previous_file, ''):
        return file
    else:
        return previous_file
