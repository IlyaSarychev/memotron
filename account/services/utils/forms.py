'''Модуль для работы с формами'''


def process_form_fields(form, checked=False, textarea_rows=3):
    '''Добавить классы bootstrap для полей формы и изменить виджеты.
    Если checked=True, все чекбоксы будут отмечены. По умолчанию False.'''

    for visible in form.visible_fields():
        if visible.field.widget.__class__.__name__ == 'CheckboxInput':
            visible.is_checkbox = True
            visible.field.widget.attrs['class'] = 'form-check-input'
            if checked:
                visible.field.widget.attrs['checked'] = True
        else:
            visible.field.widget.attrs['class'] = 'form-control'

            if visible.field.widget.__class__.__name__ == 'Textarea':
                visible.field.widget.attrs['rows'] = str(textarea_rows)