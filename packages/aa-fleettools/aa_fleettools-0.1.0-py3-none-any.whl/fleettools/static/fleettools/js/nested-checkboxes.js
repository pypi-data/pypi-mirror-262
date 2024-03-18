$('li :checkbox').on('click', function () {
    var $chk = $(this), $li = $chk.closest('li');
    if ($li.has('ul')) {
        $li.find(':checkbox').not(this).prop({'checked': false, 'disabled': this.checked});
    }
});