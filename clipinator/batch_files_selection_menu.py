from InquirerPy import prompt


def show_batch_files_selection_menu(batch_files, menu_msg="Select batch file to process:"):
    options = [
        {
            'type': 'list',
            'name': 'batch_file',
            'message': menu_msg,
            'choices': batch_files,
        }
    ]

    return prompt(options)['batch_file']
