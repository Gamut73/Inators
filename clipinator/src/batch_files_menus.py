from InquirerPy import prompt


def show_batch_files_selection_menu(batch_files, menu_msg):
    options = [
        {
            'type': 'list',
            'name': 'batch_file',
            'message': menu_msg,
            'choices': batch_files,
        }
    ]

    return prompt(options)['batch_file']


def show_batch_files_checklist_menu(batch_files, menu_msg):
    options = [
        {
            'type': 'checkbox',
            'name': 'batch_files_to_delete',
            'message': menu_msg,
            'choices': batch_files,
        }
    ]

    return prompt(options)['batch_files_to_delete']
