$(document).ready(function() {

    const _validImageFileExtensions = ["jpg", "jpeg", "gif", "png"]

    // Обработка формы смены фото профиля
    $('.profile-photo-form input[type="file"]').change(function(e) {

        const file = $(this).get(0).files[0]
        const filename = file.name

        // if (file.size > 1024) {
        //     return alert('Максимальный размер загружаемого файла: 1k');
        // }
        
        if (_validImageFileExtensions.includes(filename.split('.').pop())) {
            // Правильное расширение файла

            var formData = new FormData($(this).closest('form').get(0));

            // add assoc key values, this will be posts values
            formData.append("filename", filename);
            formData.append("file", file);

            $.ajax({
                type: 'POST',
                url: window.imgChangeURL, // искать объявление в account/profile/detail.html
                enctype: 'multipart/form-data',
                data: formData,
                processData: false,
                contentType: false,
                success(res) {
                    if (res.error) {
                        console.log('Ошибка запроса')
                    } else {
                        $('.profile-photo').attr('src', res.url)
                    }
                }
            })
        } else {
            // Неправильное расширение файла
            $(this).val('')
            alert('Файл должен иметь одно из разширений: "jpg", "jpeg", "gif", "png".')
        }
    })
})